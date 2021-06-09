import math
import numpy as np
from functools import *


# 交换矩阵某两行函数
def swap(a, b):
    for i in range(len(a)):
        t = a[i]
        a[i] = b[i]
        b[i] = t


# 打印矩阵
def print_matrix(info, eless):
    print(info)
    for i in range(eless.shape[0]):
        print("{0} [".format(i), end="")
        for j in range(col_cnt):
            print("%d" % eless[i][j], end=" ")
            # 输出矩阵元素m[i][j]
            if j == col_cnt - 1:
                print("]")


# 矩阵的阶梯化处理函数
def eliminate_row(row_idx):
    global elementss, row_cnt, col_cnt
    # 主元为0不执行操作
    if elementss[row_idx][row_idx] == 0:
        return

    for i in range(row_idx + 1, row_cnt):
        if elementss[i][row_idx] == 0:
            continue

        # 求最小公倍数以在整数域中消元
        # 如果i行的主元列和row_idx行的主元列符号相同，i行需要减row_idx行的元素，否则加row_idx行的元素
        if (elementss[row_idx][row_idx] > 0 and elementss[i][row_idx] > 0) or \
            (elementss[row_idx][row_idx] < 0 and elementss[i][row_idx] < 0):
            sign_factor = -1
        else:
            sign_factor = 1

        row_ele = abs(elementss[row_idx][row_idx])
        i_ele = abs(elementss[i][row_idx])
        lcm = row_ele / math.gcd(int(row_ele), int(i_ele)) * i_ele
        row_mul = int(lcm / row_ele)
        i_mul = int(lcm / i_ele)
        # 对这一行的所有数进行操作，其中和主元同一列的那个数会归零
        for j in range(col_cnt):
            elementss[i][j] = (elementss[i][j] * i_mul + elementss[row_idx][j] * row_mul * sign_factor) % 4

    eliminated_elementss[row_idx] = elementss.copy()


def verify_sols(row_idx):
    global elementss, eliminated_elementss, var_cnt, var_cnt
    eless = eliminated_elementss[row_idx]
    start_row_idx = 0 if row_idx == -1 else row_idx
    return reduce(lambda x, y: x and y,
                  sols[start_row_idx: var_cnt].dot(eless[start_row_idx: var_cnt, start_row_idx: var_cnt].T) % 4
                  == eless[start_row_idx: var_cnt, -1:].T[0], True)


def get_sols(row_idx):
    global elementss, row_cnt, col_cnt, sols
    if row_idx == -1:
        return verify_sols(-1)

    tmp = elementss[row_idx][col_cnt - 1]
    for ii in range(row_idx + 1, col_cnt - 1):
        if elementss[row_idx][ii] != 0:
            tmp -= elementss[row_idx][ii] * sols[ii]
            tmp = tmp % 4

    # 如果主元=2，余数=0或2时，要特殊处理
    if elementss[row_idx][row_idx] == 2 and (tmp == 0 or tmp == 2):
        # 余数=0时，解可能=0 2
        if tmp == 0:
            sols[row_idx] = 0
            # 先检查是否符合row_idx行及之前的行阶梯化后的矩阵
            if verify_sols(row_idx):
                res = get_sols(row_idx - 1)
                if res:
                    return True

            sols[row_idx] = 2
            if verify_sols(row_idx):
                return get_sols(row_idx - 1)

            return False

        # 余数=2时，解可能=1 3
        else:
            sols[row_idx] = 1
            # 先检查是否符合row_idx行及之前的行阶梯化后的矩阵
            if verify_sols(row_idx):
                res = get_sols(row_idx - 1)
                if res:
                    return True

            sols[row_idx] = 3
            if verify_sols(row_idx):
                return get_sols(row_idx - 1)

            return False

    else:
        for ii in range(4):
            if ii * elementss[row_idx][row_idx] % 4 == tmp:
                sols[row_idx] = ii
                return get_sols(row_idx - 1)

        return False


def eliminate_matrix():
    global elementss, row_cnt, col_cnt, sols, var_cnt
    while var_cnt < row_cnt:
        # 遍历未作为过主元的行，选取第i个元素绝对值最大那行，作为主元所在行
        # 对比过程排除2是为了尽量避免主元=2。因为如果主元=2，余数=0或2时，要枚举验证答案，耗时长
        max_e = abs(elementss[var_cnt][var_cnt])
        max_mul_i = var_cnt
        main_2_i = var_cnt
        for k in range(var_cnt + 1, row_cnt):
            abs_e = abs(elementss[k][var_cnt])
            if abs_e != 2:
                if abs_e > max_e:
                    max_e = abs_e
                    max_mul_i = k
            else:
                main_2_i = k

        if max_e == 0:
            max_mul_i = main_2_i

        if max_mul_i != var_cnt:
            swap(elementss[var_cnt], elementss[max_mul_i])

        # 进行阶梯化操作
        eliminate_row(var_cnt)
        var_cnt += 1

    if not get_sols(var_cnt - 1):
        sols = np.array([], dtype=int)


question_start_idx = 10005
question_cnt = 1
for question_num in range(question_start_idx, question_start_idx + question_cnt):
    # questions/{0}.csv是题目数组，记录每盏灯被哪几盏灯影响（被第n盏灯影响，该行第n列=1，否则=0），最后达到结果需要变动多少次
    # 如第1行1, 1, 1, 0, 1, 0, 0, 0, 3，意味着第1盏灯被第1、2、3、5盏灯影响，最后达到结果需要变动3次
    elementss = np.loadtxt("questions/{0}.csv".format(question_num), delimiter=",")
    eliminated_elementss = {}
    eliminated_elementss[-1] = elementss.copy()
    row_cnt = elementss.shape[0]
    col_cnt = elementss.shape[1]
    sols = np.zeros(row_cnt, dtype=int)
    var_cnt = 0
    eliminate_matrix()
    print_matrix("化简后的系数矩阵为：", elementss)
    print("解：", sols)
    actions = []
    if len(sols) == 0:
        actions.append("此题无解")
    else:
        step_idx = 0
        # 根据灯数推出图中的行数、列数
        pic_row_cnt = 2
        pic_col_cnt = 2
        if row_cnt == 12:
            pic_col_cnt = 3
        elif row_cnt == 18 or row_cnt == 27:
            pic_row_cnt = 3
            pic_col_cnt = 3
        elif row_cnt == 36:
            pic_row_cnt = 3
            pic_col_cnt = 4
        elif row_cnt == 48 or row_cnt == 64:
            pic_row_cnt = 4
            pic_col_cnt = 4
        elif row_cnt == 80:
            pic_row_cnt = 4
            pic_col_cnt = 5
        elif row_cnt == 100:
            pic_row_cnt = 5
            pic_col_cnt = 5
        elif row_cnt == 120:
            pic_row_cnt = 5
            pic_col_cnt = 6
        elif row_cnt == 144:
            pic_row_cnt = 6
            pic_col_cnt = 6

        cnt_per_floor = pic_row_cnt * pic_col_cnt
        pre_floor_num = 1
        pre_row_num = 1
        for i in range(len(sols)):
            if sols[i] != 0:
                step_idx += 1
                floor_num = int(i / cnt_per_floor) + 1
                num_in_floor = i % cnt_per_floor
                row_num, col_num = divmod(num_in_floor, pic_col_cnt)
                row_num += 1
                col_num += 1
                if pre_floor_num != floor_num or pre_row_num != row_num:
                    if pre_floor_num != floor_num:
                        pre_floor_num = floor_num

                    if pre_row_num != row_num:
                        pre_row_num = row_num

                    actions.append("\r")

                actions.append("{:0>2d}.点击第{}层第{}行第{}列的灯{}次"
                               .format(step_idx, floor_num, row_num, col_num, sols[i]))

    with open("answers/{0}.txt".format(question_num), "w", encoding="utf-8") as answer_file:
        answer_file.write("{0}".format("\r".join(actions)))
