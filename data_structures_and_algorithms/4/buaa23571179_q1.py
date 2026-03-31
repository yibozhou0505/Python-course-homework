import sys
import time
import tracemalloc

# ==========================================
# 核心限制：禁止 import 任何数学库 (如 math, numpy)
# 所有的初等函数和解析逻辑均需纯手工实现！
# 严禁使用 eval() 直接求值！
# ==========================================

PI = 3.141592653589793
E = 2.718281828459045


# --- 1. 底层数学引擎 TODO 区 ---

def my_pow(base, exp):
    """实现 base**exp，其中 exp 为非负整数"""
    if exp < 0:
        raise ValueError("指数必须是非负整数")
    result = 1.0
    for _ in range(exp):
        result *= base
    return result


def my_sin(x):
    """使用泰勒级数实现 sin(x)"""
    # 先把 x 缩到 [-PI, PI]，这样级数收敛更快
    while x > PI:
        x -= 2 * PI
    while x < -PI:
        x += 2 * PI

    term = x
    result = x
    for n in range(1, 15):
        term = -term * x * x / ((2 * n) * (2 * n + 1))
        result += term
    return result


def my_cos(x):
    """使用泰勒级数实现 cos(x)"""
    while x > PI:
        x -= 2 * PI
    while x < -PI:
        x += 2 * PI

    term = 1.0
    result = 1.0
    for n in range(1, 15):
        term = -term * x * x / ((2 * n - 1) * (2 * n))
        result += term
    return result


def my_exp(x):
    """使用泰勒级数实现 e^x"""
    # 负数单独处理：e^(-x)=1/e^x
    if x < 0:
        return 1.0 / my_exp(-x)

    term = 1.0
    result = 1.0
    for n in range(1, 60):
        term = term * x / n
        result += term
        if abs(term) < 1e-15:
            break
    return result


def my_ln(x):
    """使用数值算法（牛顿迭代法）实现 ln(x)"""
    if x <= 0:
        raise ValueError("ln(x) 的 x 必须大于 0")

    # 先把 x 调整到 [0.5, 2] 附近，便于迭代
    k = 0
    while x > 2.0:
        x /= E
        k += 1
    while x < 0.5:
        x *= E
        k -= 1

    # 解方程 exp(y) = x
    y = x - 1.0  # 初值
    for _ in range(30):
        ey = my_exp(y)
        y_new = y - (ey - x) / ey
        if abs(y_new - y) < 1e-12:
            y = y_new
            break
        y = y_new

    return y + k


# --- 2. 表达式解析引擎 TODO 区 ---

def evaluate_expression(expression, x_val, y_val):
    """
    解析数学表达式并计算结果。
    出错时返回：
    - 除0
    - 公式不匹配
    - 运算符不合理
    """
    # 统一写法
    expression = expression.replace("e**(", "exp(").replace("e^(", "exp(")
    expression = expression.replace("**", "^")
    expression = expression.replace(" ", "")

    # ---------- 先做一些简单的合法性检查 ----------
    if expression == "":
        return "公式不匹配"

    # 1. 括号检查
    balance = 0
    for ch in expression:
        if ch == '(':
            balance += 1
        elif ch == ')':
            balance -= 1
            if balance < 0:
                return "公式不匹配"
    if balance != 0:
        return "公式不匹配"

    # 2. 非法字符检查
    allowed = "0123456789.+-*/^()xy"
    i_check = 0
    while i_check < len(expression):
        ch = expression[i_check]
        # 函数名和常量单独放行
        if expression.startswith("sin", i_check):
            i_check += 3
            continue
        if expression.startswith("cos", i_check):
            i_check += 3
            continue
        if expression.startswith("ln", i_check):
            i_check += 2
            continue
        if expression.startswith("exp", i_check):
            i_check += 3
            continue
        if expression.startswith("pi", i_check):
            i_check += 2
            continue
        if ch == 'e':
            i_check += 1
            continue
        if ch in allowed:
            i_check += 1
            continue
        return "运算符不合理"

    i = 0
    n = len(expression)

    def peek():
        nonlocal i
        if i < n:
            return expression[i]
        return ""

    def consume(ch):
        nonlocal i
        if i < n and expression[i] == ch:
            i += 1
            return True
        return False

    def parse_number():
        nonlocal i
        start = i
        dot_count = 0

        while i < n and (expression[i].isdigit() or expression[i] == '.'):
            if expression[i] == '.':
                dot_count += 1
                if dot_count > 1:
                    raise ValueError("bad_number")
            i += 1

        if start == i:
            raise ValueError("bad_formula")

        return float(expression[start:i])

    def parse_expression():
        value = parse_term()
        while True:
            if consume('+'):
                value += parse_term()
            elif consume('-'):
                value -= parse_term()
            else:
                break
        return value

    def parse_term():
        value = parse_unary()
        while True:
            if consume('*'):
                value *= parse_unary()
            elif consume('/'):
                divisor = parse_unary()
                if divisor == 0:
                    raise ZeroDivisionError
                value /= divisor
            else:
                break
        return value

    def parse_unary():
        if consume('+'):
            return parse_unary()
        if consume('-'):
            return -parse_unary()
        return parse_power()

    def parse_power():
        value = parse_primary()
        if consume('^'):
            exp_val = parse_unary()
            exp_int = int(exp_val)
            if exp_val < 0 or abs(exp_val - exp_int) > 1e-9:
                raise ValueError("bad_operator")
            value = my_pow(value, exp_int)
        return value

    def parse_primary():
        nonlocal i

        # 括号
        if consume('('):
            value = parse_expression()
            if not consume(')'):
                raise ValueError("bad_formula")
            return value

        # 函数
        if expression.startswith("sin", i):
            i += 3
            if not consume('('):
                raise ValueError("bad_formula")
            arg = parse_expression()
            if not consume(')'):
                raise ValueError("bad_formula")
            return my_sin(arg)

        if expression.startswith("cos", i):
            i += 3
            if not consume('('):
                raise ValueError("bad_formula")
            arg = parse_expression()
            if not consume(')'):
                raise ValueError("bad_formula")
            return my_cos(arg)

        if expression.startswith("ln", i):
            i += 2
            if not consume('('):
                raise ValueError("bad_formula")
            arg = parse_expression()
            if not consume(')'):
                raise ValueError("bad_formula")
            return my_ln(arg)

        if expression.startswith("exp", i):
            i += 3
            if not consume('('):
                raise ValueError("bad_formula")
            arg = parse_expression()
            if not consume(')'):
                raise ValueError("bad_formula")
            return my_exp(arg)

        # 常量
        if expression.startswith("pi", i):
            i += 2
            return PI

        if expression.startswith("e", i):
            i += 1
            return E

        # 变量
        if consume('x'):
            return x_val
        if consume('y'):
            return y_val

        # 数字
        if peek().isdigit() or peek() == '.':
            return parse_number()

        # 如果当前位置是运算符，说明运算符位置不合理
        if peek() in "+-*/^":
            raise ValueError("bad_operator")

        raise ValueError("bad_formula")

    try:
        result = parse_expression()

        # 说明后面还有没解析完的内容
        if i != n:
            # 剩余部分如果以运算符开头，一般属于运算符不合理
            if expression[i] in "+-*/^":
                return "运算符不合理"
            return "公式不匹配"

        return result

    except ZeroDivisionError:
        return "除0"
    except ValueError as e:
        msg = str(e)
        if msg == "bad_operator":
            return "运算符不合理"
        else:
            return "公式不匹配"
    except:
        return "公式不匹配"
   


# --- 3. 评测系统入口（请勿修改） ---

def main():
    tracemalloc.start()
    start = time.perf_counter()

    input_data = sys.stdin.read().splitlines()
    if len(input_data) < 3:
        return

    expression = input_data[0].strip()
    try:
        x_val = float(input_data[1].strip())
        y_val = float(input_data[2].strip())

        # 调用学生手写的解析器
        result = evaluate_expression(expression, x_val, y_val)

    except Exception as e:
        # 【框架优化】：捕获具体的异常类型，方便学生在本地输出排错
        result = f"Error: {type(e).__name__} -> {str(e)}"

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    with open("output.txt", "w", encoding="utf-8") as f:
        # 确保输出浮点数
        if isinstance(result, float):
            f.write(f"{result:.6f}\n")
        else:
            f.write(f"{result}\n")

        elapsed = end - start
        peak_kb = peak // 1024
        f.write("运行时间: {:.6f} s  内存占用: {} KB\n".format(elapsed, peak_kb))


if __name__ == "__main__":
    main()