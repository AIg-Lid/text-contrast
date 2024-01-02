# -*- coding: utf-8 -*-
import imp
import gc
import os
import sys
import time
from src.util import get_diff_info
from src.util import exchange_img_to_txt

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
import diff_match_repo as dmp_module
imp.reload(dmp_module)


def main():
    pdf_path_1 = "123.pdf"
    pdf_path_2 = "123-2.pdf"
    text1 = exchange_img_to_txt(pdf_path_1)
    text2 = exchange_img_to_txt(pdf_path_2)
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


if __name__ == '__main__':

    main()







