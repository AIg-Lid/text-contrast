# -*- coding: utf-8 -*-
"""Diff Speed Test
Copyright 2018 The diff-match-patch Authors.
https://github.com/google/diff-match-patch

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
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
  text1 = open("speedtest1.txt", "r", encoding="utf8").read()
  text2 = open("speedtest2.txt", "r", encoding="utf8").read()

  dmp = dmp_module.diff_match_patch()
  dmp.Diff_Timeout = 0.0
  diffs_res = dmp.diff_main(text2, text1, False)
  # Execute one reverse diff as a warmup.
  print("文档2和文档1对比： ", diffs_res)
  for item in diffs_res:
    print("差异元素: ", item, "数据类型: ", type(item))


  # start_time = time.time()
  # print("文档1 和 文档2 对比： ", dmp.diff_main(text1, text2, False))
  # end_time = time.time()
  #gc.collect()
  # print("Elapsed time: %f" % (end_time - start_time))

if __name__ == "__main__":
  main()
