# -*- coding: utf-8 -*-
"""
@Time ： 2023/12/29 13:45
@Auth ： Lid
@File ：txt_diff_test.py
@IDE ：PyCharm
"""
import imp
import gc
import os
import sys
import time
from src.util import get_diff_info
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
import diff_match_repo as dmp_module
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


if __name__ == "__main__":
    main()
