import sys
import numpy as np

row_cnt = int(sys.argv[1])
col_cnt = int(sys.argv[2])
floor_cnt = int(sys.argv[3])
ele_cnt = row_cnt * col_cnt * floor_cnt

# 题目数组记录每盏灯被哪几盏灯影响（被第n盏灯影响，该行第n列=1，否则=0），最后达到结果需要变动多少次
# 如第1行1, 1, 1, 0, 1, 0, 0, 0, 3，意味着第1盏灯被第1、2、3、5盏灯影响，最后达到结果需要变动3次
# 本程序生成题目数组questions的模板（不包括最后一列，最后一列请对比题目和目标图形填充
# 如题目第1盏灯是红色，目标图形中是绿色，因为红变绿需要变动3次，所以该行请填3到第1行）
questions = np.zeros([ele_cnt, ele_cnt], int)
cnt_per_floor = row_cnt * col_cnt
for k in range(floor_cnt):
    for i in range(row_cnt):
        for j in range(col_cnt):
            # 元素序号(由0开始)
            ele_idx = k * cnt_per_floor + i * col_cnt + j
            questions[ele_idx, ele_idx] = 1
            # 行、列、高取-1、0、1，获取受当前元素影响的元素
            for delta in range(-1, 2, 2):
                adjacent_i = i + delta
                if 0 <= adjacent_i < row_cnt:
                    adjacent_idx = k * cnt_per_floor + adjacent_i * col_cnt + j
                    questions[ele_idx, adjacent_idx] = 1

                adjacent_j = j + delta
                if 0 <= adjacent_j < col_cnt:
                    adjacent_idx = k * cnt_per_floor + i * col_cnt + adjacent_j
                    questions[ele_idx, adjacent_idx] = 1
                adjacent_k = k + delta
                if 0 <= adjacent_k < floor_cnt:
                    adjacent_idx = adjacent_k * cnt_per_floor + i * col_cnt + j
                    questions[ele_idx, adjacent_idx] = 1


np.savetxt("question-templates/{0}-{1}-{2}.csv".format(row_cnt, col_cnt, floor_cnt), questions, '%d', delimiter=',')
