# text-contrast

第一部分：

txt文本比对，把两个TXT文件中的文本内容进行比对，调用的是谷歌的diff_match库，把比对的结果二次重构出来。

diff_match库的判别符意义：

0	代表相同的text

-1      代表有的text

1       代表自己没有的text

行号 根据“\n”进行计算

每行的 “增加”， “缺失”， “修改” 字符的下标索引  通过维护字符串的长度计算



第二部分：

后端TXT文本比对已经完成，只要接上前端即可展示差异，PDF比对通过paddleocr翻译成文本然后再走TXT比对流程



代码配置环境即可运行，models文件夹下的模型需要自己去百度官网去下载

感谢谷歌和百度的工作付出，如涉及侵权内容联系我删除，纯属自娱自乐项目



reference

```bash
1. https://github.com/PaddlePaddle/PaddleOCR
2. https://github.com/google/diff-match-patch
```

