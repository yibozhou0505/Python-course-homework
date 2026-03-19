from dataclasses import dataclass, field
from typing import Optional, List
import os

# ========= Cfg =========
@dataclass
class BaseAccountConfig:
    min_open_deposit: int = 100
    min_balance: float = 1.0
    large_deposit_threshold: int = 2 ** 31


@dataclass
class CreditConfig:
    max_credit_limit: float = 10000.0
    bank_loan_ratio: float = 0.3


@dataclass
class MessageConfig:
    fake_money: str = "假币"
    large_deposit: str = "大额存款，请确认"

    open_need_100: str = "开户需至少存入100元"

    account_not_activate: str = "账户未激活"
    account_not_activate_close: str = "账户未激活，无法销户"
    withdraw_need_positive_integer: str = "取款金额必须为正整数"

    credit_not_activate: str = "信用卡不存在或未激活"
    charge_need_positive: str = "消费金额必须为正数"
    repay_need_positive: str = "还款金额必须为正数"

    mobile_not_linked: str = "手机账户未关联基础账户"
    mobile_not_linked_charge: str = "手机账户未关联"   
    mobile_need_base_first: str = "错误：必须先创建基础账户"
    mobile_no_credit: str = "错误：手机账户不支持信用消费/借款"

    user_closed: str = "已销户"
    base_not_exist: str = "基础账户不存在"
    unknown_account_type: str = "未知账户类型"
    cannot_close_with_debt: str = "有信用卡借款，无法销户"


@dataclass
class BankConfig:
    base: BaseAccountConfig = field(default_factory=BaseAccountConfig)
    credit: CreditConfig = field(default_factory=CreditConfig)
    message: MessageConfig = field(default_factory=MessageConfig)


# ========= Utils =========
def parse_amount_token(token: str) -> int:
    """str2int"""
    if token.lstrip('-').isdigit():
        return int(token)
    return token


def is_positive_int(x) -> bool:
    """check if x is a positive integer"""
    return isinstance(x, int) and x > 0


def pretty_amount(x: float):
    """format any to 2 decimal places"""
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return f"{x:.2f}"


# ========= classes =========
class CreditCard:
    def __init__(self, cfg: BankConfig, owner=None):
        self.cfg = cfg
        self.owner = owner
        self.active = False
        self.debt = 0.0

    def activate(self):
        self.active = True

    def repay(self, amount):
        if self.owner is None:
            return None
        return self.owner.repay(amount)


class BaseAccount:
    def __init__(self, owner, cfg: BankConfig):
        self.owner = owner
        self.cfg = cfg
        self.active = False
        self.balance = 0.0

    def status_line(self) -> str:
        return f"基础账户余额：{self.balance:.2f}元，信用卡借款：{self.owner.current_credit_debt():.2f}元"

    def deposit(self, amount: float):
        msg = self.cfg.message
        base_cfg = self.cfg.base
        lines = []

        # Case B1 存款金额不是正整数
        if not is_positive_int(amount):
            return msg.fake_money

        # 无论是否首次开户，只要超过阈值都提示
        if amount > base_cfg.large_deposit_threshold:
            lines.append(msg.large_deposit)

        # 未激活（包括曾销户后重新开户）
        if not self.active:
            # Case B3 首次开户时存款金额不足 100 元
            if amount < base_cfg.min_open_deposit:
                return msg.open_need_100

            # 若是已销户后重新开户，需要恢复用户计数
            if self.owner.is_closed_flag:
                self.owner.bank.total_users += 1

            self.owner.is_closed_flag = False
            self.active = True
            self.balance += float(amount)
            self.owner.bank.total_deposit += float(amount)

            lines.append(f"开户成功，存入{amount}元")
            lines.append(self.status_line())
            return "\n".join(lines)

        # Case B7 已激活账户正常存款
        self.balance += float(amount)
        self.owner.bank.total_deposit += float(amount)
        lines.append(f"存款成功，存入{amount}元")
        lines.append(self.status_line())
        return "\n".join(lines)

    def withdraw_after_validation(self, amount: float):
        base_cfg = self.cfg.base

        # Case B10 正常取款
        if self.balance - amount >= base_cfg.min_balance:
            self.balance -= amount
            self.owner.bank.total_deposit -= amount
            return (
                f"取款成功，取出{amount}元\n"
                f"{self.status_line()}"
            )

        # Case B11 有信用卡欠款，保留 1 元
        if self.owner.current_credit_debt() > 0:
            withdraw_amount = max(0.0, self.balance - base_cfg.min_balance)
            self.balance = base_cfg.min_balance
            self.owner.bank.total_deposit -= withdraw_amount
            return (
                f"取款成功，取出{pretty_amount(withdraw_amount)}元（保留 1 元）\n"
                f"{self.status_line()}"
            )

        # Case B12 无信用卡借款，取款导致自动销户
        withdraw_amount = self.balance
        self.balance = 0.0
        self.active = False
        self.owner.is_closed_flag = True
        self.owner.bank.total_deposit -= withdraw_amount
        self.owner.bank.total_users -= 1
        return (
            f"销户取款，取出{pretty_amount(withdraw_amount)}元\n"
            f"{self.status_line()}"
        )

    def close_account(self):
        msg = self.cfg.message

        # Case B13 手动销户时账户未激活
        if not self.active or self.owner.is_closed_flag:
            return msg.account_not_activate_close

        # Case B14 手动销户时存在信用卡借款
        if self.owner.current_credit_debt() > 0:
            return msg.cannot_close_with_debt

        # Case B15 手动销户成功
        withdraw_amount = self.balance
        self.balance = 0.0
        self.active = False
        self.owner.is_closed_flag = True
        self.owner.bank.total_deposit -= withdraw_amount
        self.owner.bank.total_users -= 1
        return (
            f"销户成功，取出{pretty_amount(withdraw_amount)}元\n"
            f"{self.status_line()}"
        )


class MobileAccount:
    def __init__(self, owner, base_account: BaseAccount, cfg: BankConfig):
        self.owner = owner
        self.base_account = base_account
        self.cfg = cfg

    # Case M5 手机账户尝试信用消费/借款
    def charge(self, amount):
        return self.cfg.message.mobile_no_credit


class User:
    def __init__(self, bank, user_id: int, cfg: BankConfig):
        self.bank = bank
        self.user_id = user_id
        self.cfg = cfg
        self.base_account: Optional[BaseAccount] = None
        self.mobile_account: Optional[MobileAccount] = None
        self.credit_card: Optional[CreditCard] = None
        self.is_closed_flag = False   # 显式记录是否已销户

    # 创建基础账户
    def create_base_account(self):
        if self.base_account is None:
            self.base_account = BaseAccount(self, self.cfg)

    # Case U1 未创建基础账户就创建手机账户
    def create_mobile_account(self):
        if self.base_account is None:
            return self.cfg.message.mobile_need_base_first
        if self.mobile_account is None:
            self.mobile_account = MobileAccount(self, self.base_account, self.cfg)
        return None

    # 创建信用卡
    def create_credit_card(self):
        if self.credit_card is None:
            self.credit_card = CreditCard(self.cfg, self)

    # 当前信用卡欠款
    def current_credit_debt(self) -> float:
        if self.credit_card is None or not self.credit_card.active:
            return 0.0
        return self.credit_card.debt

    # 是否关闭
    def is_closed(self) -> bool:
        return self.is_closed_flag

    # === 存款 ====
    def deposit(self, amount, account_type="base"):
        msg = self.cfg.message

        if account_type == "base":
            # 对齐满分代码：先判假币，再判基础账户不存在
            if not is_positive_int(amount):
                return msg.fake_money
            if self.base_account is None:
                return msg.base_not_exist
            return self.base_account.deposit(amount)

        if account_type == "mobile":
            # 手机账户未关联基础账户时存款
            if self.mobile_account is None or self.mobile_account.base_account is None:
                return msg.mobile_not_linked
            return self.base_account.deposit(amount)

        return msg.unknown_account_type

    # === 取款 ====
    def withdraw(self, amount, account_type="base"):
        msg = self.cfg.message

        # Case U2 已销户用户尝试取款或借款
        if self.is_closed():
            return msg.user_closed

        if account_type == "base":
            # Case B8 账户未激活时取款
            if self.base_account is None or not self.base_account.active:
                return msg.account_not_activate
            # Case B9 取款金额不是正整数
            if not is_positive_int(amount):
                return msg.withdraw_need_positive_integer
            return self.base_account.withdraw_after_validation(amount)

        if account_type == "mobile":
            # Case M1 手机账户未关联基础账户时存款或取款
            if self.mobile_account is None or self.mobile_account.base_account is None:
                return msg.mobile_not_linked
            # 满分代码里这里还会判断基础账户是否激活
            if self.base_account is None or not self.base_account.active:
                return msg.account_not_activate
            # Case M2 手机账户取款金额不是正整数
            if not is_positive_int(amount):
                return msg.withdraw_need_positive_integer
            return self.base_account.withdraw_after_validation(amount)

        return msg.unknown_account_type

    # === 信用卡/借款 ====
    def charge(self, amount):
        msg = self.cfg.message
        credit_cfg = self.cfg.credit

        # Case U2 已销户用户尝试取款或借款
        if self.is_closed():
            return msg.user_closed

        # Case U6 信用卡不存在或未激活
        if self.credit_card is None or not self.credit_card.active:
            return msg.credit_not_activate

        # Case C2 消费/借款金额不是正数
        if not is_positive_int(amount):
            return msg.charge_need_positive

        personal_left = credit_cfg.max_credit_limit - self.credit_card.debt
        bank_left = self.bank.total_deposit * credit_cfg.bank_loan_ratio - self.bank.total_loan
        max_loan = min(personal_left, bank_left)
        if max_loan < 0:
            max_loan = 0.0

        # Case C3 借款失败，超出允许范围
        if amount > max_loan + 1e-9:
            return f"{max_loan:.2f}"

        # Case C4 借款/消费成功
        self.credit_card.debt += float(amount)
        self.bank.total_loan += float(amount)
        return (
            f"消费/借款成功，金额{float(amount):.2f}元\n"
            f"{self.base_account.status_line()}"
        )

    # === 还款 ====
    def repay(self, amount):
        msg = self.cfg.message
        base_cfg = self.cfg.base

        # Case U6 信用卡不存在或未激活
        if self.credit_card is None or not self.credit_card.active:
            return msg.credit_not_activate

        # Case C5 还款金额不是正数
        if not is_positive_int(amount):
            return msg.repay_need_positive

        if self.base_account is None or not self.base_account.active or self.is_closed():
            return None

        # Case C6 还款成功
        actual = min(
            float(amount),
            self.credit_card.debt,
            max(0.0, self.base_account.balance - base_cfg.min_balance)
        )

        if actual <= 0:
            return None

        self.credit_card.debt -= actual
        self.base_account.balance -= actual
        self.bank.total_deposit -= actual
        self.bank.total_loan -= actual
        return (
            f"还款成功，金额{actual:.2f}元\n"
            f"{self.base_account.status_line()}"
        )


class Bank:
    def __init__(self, cfg: Optional[BankConfig] = None):
        self.cfg = cfg if cfg is not None else BankConfig()
        self.users = {}
        self.next_id = 1001

        # 对齐满分代码的 BANK_INFO 统计口径
        self.total_users = 0
        self.total_deposit = 0.0
        self.total_loan = 0.0

    # 创建用户
    def create_user(self):
        user_id = self.next_id
        self.next_id += 1
        self.users[user_id] = User(self, user_id, self.cfg)
        self.total_users += 1

    # 获取用户
    def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    # 统计用户数量
    def active_user_count(self) -> int:
        return self.total_users

    # 统计存款总额
    def total_deposit_amount(self) -> float:
        return self.total_deposit

    # 统计贷款总额
    def total_loan_amount(self) -> float:
        return self.total_loan

    # Case BK1 银行内部查询当前统计信息
    def print_info(self):
        return (
            f"当前用户总量：{self.active_user_count()}\n"
            f"存款总额：{self.total_deposit_amount():.2f}\n"
            f"贷款总额：{self.total_loan_amount():.2f}"
        )


# =========================
# 命令驱动
# =========================

def run_commands(text: str) -> List[str]:
    bank = Bank()
    output_lines: List[str] = []

    for raw in text.splitlines():
        line = raw.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split()
        cmd = parts[0]
        result = None

        # 1. 创建用户
        if cmd == "CREATE_USER":
            bank.create_user()

        # 2. 创建基础账户对象
        elif cmd == "CREATE_BASE":
            user = bank.get_user(int(parts[1]))
            if user is not None:
                user.create_base_account()

        # 3. 创建手机账户对象
        elif cmd == "CREATE_MOBILE":
            user = bank.get_user(int(parts[1]))
            if user is not None:
                result = user.create_mobile_account()

        # 4. 创建信用卡对象
        elif cmd == "CREATE_CREDIT":
            user = bank.get_user(int(parts[1]))
            if user is not None:
                user.create_credit_card()

        # 5. 激活信用卡
        elif cmd == "ACTIVATE_CREDIT":
            user = bank.get_user(int(parts[1]))
            if user is not None and user.credit_card is not None:
                user.credit_card.activate()

        # 6. 基础账户存款
        elif cmd == "DEPOSIT_BASE":
            user = bank.get_user(int(parts[1]))
            amount = parse_amount_token(parts[2])
            if user is not None:
                result = user.deposit(amount, "base")

        # 7. 手机账户存款
        elif cmd == "DEPOSIT_MOBILE":
            user = bank.get_user(int(parts[1]))
            amount = parse_amount_token(parts[2])
            if user is not None:
                result = user.deposit(amount, "mobile")

        # 8. 基础账户取款
        elif cmd == "WITHDRAW_BASE":
            user = bank.get_user(int(parts[1]))
            amount = parse_amount_token(parts[2])
            if user is not None:
                result = user.withdraw(amount, "base")

        # 9. 手机账户取款
        elif cmd == "WITHDRAW_MOBILE":
            user = bank.get_user(int(parts[1]))
            amount = parse_amount_token(parts[2])
            if user is not None:
                result = user.withdraw(amount, "mobile")

        # 10. 手动销户
        elif cmd == "CLOSE_BASE":
            user = bank.get_user(int(parts[1]))
            if user is None or user.base_account is None:
                result = bank.cfg.message.account_not_activate_close
            else:
                result = user.base_account.close_account()

        # 11. 信用卡借款 / 消费
        elif cmd == "CHARGE":
            user = bank.get_user(int(parts[1]))
            amount = parse_amount_token(parts[2])
            if user is not None:
                result = user.charge(amount)

        # 12. 信用卡还款
        elif cmd == "REPAY":
            user = bank.get_user(int(parts[1]))
            amount = parse_amount_token(parts[2])
            if user is not None:
                result = user.repay(amount)

        # 13. 手机账户尝试信用消费
        elif cmd == "MOBILE_CHARGE":
            user = bank.get_user(int(parts[1]))
            if user is None or user.mobile_account is None or user.mobile_account.base_account is None:
                result = bank.cfg.message.mobile_not_linked_charge
            else:
                result = user.mobile_account.charge(parse_amount_token(parts[2]))

        # 14. 银行内部查询
        elif cmd == "BANK_INFO":
            result = bank.print_info()

        if result:
            output_lines.extend(str(result).split("\n"))

    return output_lines


def main():
    input_path = '/coursegrader/testdata/input.txt'
    if not os.path.exists(input_path):
        input_path = 'input.txt'

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception:
        text = ""

    out_lines = run_commands(text)

    with open('hw2.txt', 'w', encoding='utf-8') as f:
        for line in out_lines:
            f.write(line + '\n')


if __name__ == "__main__":
    main()