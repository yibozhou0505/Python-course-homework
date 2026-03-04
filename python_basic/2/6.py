# 输入一个数组
nums = [1, 3, -1, -3, 5, 3, 6, 7]
# 定义滑动窗口大小
window_size = 3
# 定义一个列表存储滑动窗口的最大值
max_values = []
# 遍历数组，计算滑动窗口的最大值并存储到列表中
for i in range(len(nums) - window_size + 1):
    window = nums[i: i + window_size]
    max_val = max(window)
    max_values.append(max_val)
# 输出滑动窗口的最大值列表
print(max_values)