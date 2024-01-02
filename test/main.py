# -*- coding: utf-8 -*-
"""
@Time ： 2023/12/29 13:45
@Auth ： Lid
@File ：main.py
@IDE ：PyCharm
"""
import imp
import gc
import os
import sys
import time

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
import diff_match_repo as dmp_module

# Force a module reload.  Allows one to edit the DMP module and rerun the test
# without leaving the Python interpreter.
imp.reload(dmp_module)


def main():
    """
    输出俩个文档的差异点
     差异点所在的行号、具体的字符串下标
    """
    text1 = open("speedtest1.txt", "r", encoding="utf8").read()
    text2 = open("speedtest2.txt", "r", encoding="utf8").read()

    dmp = dmp_module.diff_match_patch()
    dmp.Diff_Timeout = 0.0

    # Execute one reverse diff as a warmup.
    res1 = dmp.diff_main(text1, text2, False)

    dmp.diff_main(text2, text1, False)
    gc.collect()

    start_time = time.time()
    res2 = dmp.diff_main(text2, text1, False)
    end_time = time.time()
    print("Elapsed time: %f" % (end_time - start_time))

    # 解析JSON
    json_result = get_diff_info(res1, res2)

    print("分析之后的结果: ", json_result)


def get_diff_info(res1, res2):
    """
    这里的行计数是从0开始
    下标索引也是从0开始
    维护一行完整字符的内容
    (1) 行号的确定  主要依赖于\n 维护没俩个换行符之间的内容
    (2) 下标的确定  主要维护 俩个列表的转换  初始列表拿取前半行text
         迭代新列表缓存 后半行 text
    """
    print("输入: ", res1)
    diff_info_lsit = list()
    hang_con = 0
    tuple_con = 0
    wz_row_text = list()
    wz_hang_dict = dict()
    for ite1, ite2 in zip(res1, res2):

        # 这是相同判别符的情况下
        diff_item_dict = dict()
        if ite1[0] == ite2[0]:
            # 相同的 遍历元素
            if ite1[0] == 0:
                huan_con_1 = ite1[1].count("\n")
                huan_con_2 = ite2[1].count("\n")
                # 情况1 就是没有差异点元素的情况 也没有换行符的情况
                # 下标  无换行符
                if huan_con_1 == huan_con_2 and huan_con_1 == 0:
                    wz_row_text.append(ite1[1])
                    # wz_hang_dict["行完整内容"] = wz_hang_text
                # 情况2 没有差异点元素的情况 但是有换行符的情况  需要更新行号
                else:
                    hang_con += huan_con_1
                    split_ite_list = ite1[1].split("\n")
                    chu_ind = tuple_con
                    new_wz_row_text = list()
                    if huan_con_1 == 1:
                        chu_ind = tuple_con
                        tuple_con += huan_con_1
                        for ind in range(chu_ind, tuple_con):
                            wz_hang_dict[str(ind)] = "".join(wz_row_text) + split_ite_list[0]
                            new_wz_row_text.append(split_ite_list[-1])
                            wz_row_text = new_wz_row_text
                    else:
                        tuple_con += huan_con_1
                        for ind in range(chu_ind, tuple_con):
                            new_wz_row_text = list()
                            if ind == chu_ind:
                                wz_hang_dict[str(ind)] = "".join(wz_row_text) + split_ite_list[0]
                            elif ind == tuple_con - 1:
                                new_wz_row_text.append(split_ite_list[-1])
                            else:
                                print("new 列表：", new_wz_row_text)
                                print("old 列表： ", wz_row_text)
                                wz_hang_dict[ind] = new_wz_row_text[ind - chu_ind]
                                wz_row_text = new_wz_row_text
            elif ite1[0] == 1:
                pass
            else:
                # 判别符 为 -1 自有text
                # 这块 是修改类型 所做的处理
                start_ind = len("".join(wz_row_text))
                diff_item_dict["start_ind"] = start_ind
                diff_item_dict["start_row"] = hang_con
                diff_item_dict["mod_text"] = (ite1[1], ite2[1])
                diff_item_dict["diff_type"] = "修改"
                # 没有换行符的情型
                if ite1[1].count("\n") == 0:
                    diff_item_dict["end_row"] = hang_con
                    diff_item_dict["end_ind"] = start_ind + len(ite1[1])
                    # 接着维护 下标的定位逻辑
                    wz_row_text.append(ite1[1])
                else:
                    # 有换行符存在的情况应该做的处理
                    hang_con += ite1.count("\n")
                    diff_item_dict["end_row"] = hang_con
                    diff_item_dict["end_ind"] = len(ite1[1].split("\n")[-1])

                    # 维护下标
                    huan_con_1 = ite1[1].count("\n")
                    split_ite_list = ite1[1].split("\n")
                    new_wz_row_text = list()
                    chu_ind = tuple_con
                    if huan_con_1 == 1:
                        tuple_con += huan_con_1
                        for ind in range(chu_ind, tuple_con):
                            wz_hang_dict[str(ind)] = "".join(wz_row_text) + split_ite_list[0]
                            new_wz_row_text.append(split_ite_list[-1])
                            wz_row_text = new_wz_row_text
                    else:
                        tuple_con += huan_con_1
                        for ind in range(chu_ind, tuple_con):
                            if ind == chu_ind:
                                wz_hang_dict[str(ind)] = "".join(wz_row_text) + split_ite_list[0]
                            elif ind == tuple_con - 1:
                                new_wz_row_text.append(split_ite_list[-1])
                                wz_row_text = new_wz_row_text
                            else:
                                pass
                                #print("new 列表：", new_wz_row_text)
                                #print("old 列表： ", wz_row_text)
                                #wz_hang_dict[ind] = new_wz_row_text[ind - chu_ind]
                                #wz_row_text = new_wz_row_text
                    # 这个情况就有可能主文档增或者减
                diff_info_lsit.append(diff_item_dict)
        else:
            # 这个情况是 增加或者减少text
            # 主文档 增加
            if ite1[0] == -1 and ite2[0] == 1:
                start_ind = len("".join(wz_row_text))
                diff_item_dict["start_ind"] = start_ind
                diff_item_dict["start_row"] = hang_con
                diff_item_dict["diff_type"] = "增加"  # 减 或者修改
                diff_item_dict["add_text"] = (ite1[1],)
                if ite1[1].count("\n") == 0:
                    diff_item_dict["end_row"] = hang_con
                    diff_item_dict["end_ind"] = start_ind + len(ite1[1])
                    # 维护 下标
                    wz_row_text.append(ite1[1])
                else:
                    diff_item_dict["end_row"] = hang_con
                    diff_item_dict["end_ind"] = len(ite1[1].split("\n")[-1])
                    huan_con_1 = ite1[1].count("\n")
                    split_ite_list = ite1[1].split("\n")
                    new_wz_row_text = list()
                    chu_ind = tuple_con
                    if huan_con_1 == 1:
                        tuple_con += huan_con_1
                        for ind in range(chu_ind, tuple_con):
                            wz_hang_dict[str(ind)] = "".join(wz_row_text) + split_ite_list[0]
                            new_wz_row_text.append(split_ite_list[-1])
                            wz_row_text = new_wz_row_text
                    else:
                        tuple_con += huan_con_1
                        for ind in range(chu_ind, tuple_con):
                            if ind == chu_ind:
                                wz_hang_dict[str(ind)] = "".join(wz_row_text) + split_ite_list[0]
                            elif ind == tuple_con - 1:
                                new_wz_row_text.append(split_ite_list[-1])
                                wz_row_text = new_wz_row_text
                            else:
                                pass
                                #print("new 列表：", new_wz_row_text)
                                #print("old 列表： ", wz_row_text)
                                #wz_hang_dict[ind] = new_wz_row_text[ind - chu_ind]
                                #wz_row_text = new_wz_row_text

                diff_info_lsit.append(diff_item_dict)
            # 主文档减少  这块的下标不需要维护
            else:
                start_ind = len("".join(wz_row_text))
                diff_item_dict["start_ind"] = start_ind
                diff_item_dict["start_row"] = hang_con
                diff_item_dict["les_text"] = (ite1[1],)
                diff_item_dict["diff_type"] = "缺失"
                if ite1[1].count("\n") == 0:
                    diff_item_dict["end_row"] = hang_con
                    diff_item_dict["end_ind"] = start_ind
                else:
                    diff_item_dict["end_row"] = hang_con + ite1[1].count("\n")
                    diff_item_dict["end_ind"] = start_ind
                diff_info_lsit.append(diff_item_dict)
    return diff_info_lsit


if __name__ == "__main__":
    main()
