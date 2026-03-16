from buaa23571179_bank import Bank

bank = Bank()

bank.create_user()
u = bank.get_user(1001)
print(u.create_mobile_account())      # 应该：错误：必须先创建基础账户
u.create_base_account()
print(u.deposit(50, "base"))          # 应该：开户需至少存入100元
print(u.deposit(100, "base"))         # 应该两行
print(bank.print_info())              # 应该三行