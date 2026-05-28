import sys
import re
from collections import Counter

# 预编译正则，避免每次调用 get_words 都重新编译
WORD_RE = re.compile(r"[a-z]+")


def get_words(line):
    """
    提取一行中的所有英文单词，并转成小写。
    只把连续 a-z 当成单词。

    line.lower()先把所有字母变成小写
    然后通过re.findall()查找所有正则匹配为pattern的子串,以列表返回
    r是防止有"\"防转义
    [  ] 字符集，匹配括号内的任意字符
    a-z  从a到z的所有小写字母，因为已经调用line.lower()进行小写处理，因此不需要A-Z
    +    量词，匹配前面的字符至少一次，且贪心
    """
    return WORD_RE.findall(line.lower())


def main():
    input_line = sys.stdin.readline  # 读取输入

    l1 = int(input_line())  # 第一篇文章的行数
    count1 = Counter()  # 计数器

    for _ in range(l1):
        count1.update(get_words(input_line()))

    l2 = int(input_line())  # 第二篇文章的行数
    count2 = Counter()  # 计数器

    for _ in range(l2):
        count2.update(get_words(input_line()))

    # 取并集，Python 3.9+ dict_keys 直接支持 | 运算
    all_words = count1.keys() | count2.keys()

    # 1. 计算匹配单词：两篇都出现过，match > 0
    matched = []

    # 2. 计算完全不匹配单词：只出现在其中一篇文章中
    unmatched = []

    for word in all_words:
        c1 = count1[word]
        c2 = count2[word]
        m = c1 if c1 < c2 else c2  # 取最小值
        if m > 0:
            matched.append((word, m))
        else:
            unmatched.append(word)

    # 排序规则：
    # match 越大越靠前；match 相同，单词字典序升序
    matched.sort(key=lambda x: (-x[1], x[0]))

    top10 = matched[:10]  # 取前10个

    if top10:
        top_line = "TOP " + " ".join(f"{w}:{n}" for w, n in top10)
    else:
        top_line = "TOP EMPTY"

    unmatched.sort()  # 按字典序排序

    if unmatched:
        unmatched_line = "UNMATCHED " + " ".join(unmatched)
    else:
        unmatched_line = "UNMATCHED EMPTY"

    sys.stdout.write(top_line + "\n" + unmatched_line)


if __name__ == "__main__":
    main()