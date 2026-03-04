def make_dic(list):
    dic = {}
    for i in list:
        if i in dic:
            dic[i] += 1
        else:
            dic[i] = 1
    return dic

def find_prodiure(dic1, dic2):
    prodiure = 0
    for key in dic1:
        if key in dic2:
            prodiure += dic1[key] * dic2[key]
    return prodiure


if __name__ == '__main__':
    num1 = list(map(int, input().split()))
    num2 = list(map(int, input().split()))

    num1_dic = make_dic(num1)
    num2_dic = make_dic(num2)

    print(find_prodiure(num1_dic, num2_dic))
