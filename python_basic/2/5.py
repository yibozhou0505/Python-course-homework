# 从用户输入中读取一整行字符串
input_str = input()
# 将输入的字符串按空格分割成列表
input_list = input_str.split()
# 将字符串列表转换为整数列表
num_list = [int(i) for i in input_list]
# 创建一个空列表用于存储不重复的数字
unique_list = []
# 遍历整数列表，将不在unique_list中的数字添加到其中
for num in num_list:
    if num not in unique_list:
        unique_list.append(num)
# 对unique_list进行排序
unique_list.sort()
# 输出排序后的不重复数字列表
print(unique_list)
