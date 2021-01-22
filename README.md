# Word Assistant
 一个辅助记忆单词的小程序

# 使用方法
## 操作步骤

1. 将程序与单词库文件 “ trans_data.xlsx " 放在同一个文件夹下，运行时程序自动读取文件内容

2. 运行程序，选择单词类别（Excel文件中的sheet名），另有4种特殊类别：全部单词、真·全部单词、全部句子、真·全部句子

   ### > 全部单词

   全部单词并不包含所有库中的单词，它忽略了带有忽略标记的单词sheet，而包含其他有单词标记的sheet中的所有单词

   ### > 真 · 全部单词

   真 · 全部单词包含所有库中的单词，它不忽略了带有忽略标记的单词sheet

   ### > 全部句子

   全部句子并不包含所有库中的句子，它忽略了带有忽略标记的句子sheet，而包含其他有句子标记的sheet中的所有句子

   ### > 真·全部句子

   真 · 全部句子包含所有库中的句子，它不忽略了带有忽略标记的句子sheet

3. 选择 “英译汉” 或 “汉译英” 选项
   该选项选择依据英文记忆对应的中文意思还是依据中文记忆对应的英文翻译。
   当选择 “英译汉” 时，右上角的显示框内会显示英文，而需要在下方的输入框内输入对应的中文。
   当选择 “汉译英” 时，右上角的显示框内会显示中文，而需要在下方的输入框内输入对应的英文。

4. 选择好记忆选项后，单击 “start” 按钮开始。
## 操作说明
   在开始后，程序会将Excel表格里对应的sheet中的单词或句子乱序排列并按乱序排列后的顺序从第一个开始。可以看到有两个选项：记忆模式和有道词典。
   ### 1. 记忆模式
   程序有两种模式：普通模式和记忆模式。普通模式在切换单词后不会立即显示结果，而记忆模式在切换单词后会立即显示结果。
   ### 2. 有道词典
   此功能需要联网。在普通模式按下 “check” 键或在记忆模式切换单词后，程序会联网并在有道词典查询并在结果最后显示查询结果。不同的是，在记忆模式下，会查询右上角的显示内容以辅助记忆，而在普通模式下，仅当用户输入的答案错误时，到有道词典查询用户输入内容。
   ### 3. 查询功能
   在普通模式下，当用户输入的答案错误时，程序会在所有单词库中查找用户输入的内容，并将查询结果与其所在的类名（sheet名）和序号显示在结果中。
   ### 4. check，next，last
   三个按键分别代表确认、下一个和上一个。为操作方便，三个按键均有键盘上对应的快捷键，分别为回车、键盘下、键盘上。
# Excel文件格式
   为了程序方便读取，Excel文件需按一定的格式编写。
## 1. 内容
   每个sheet需有4列：第一列是从1开始的序号，第二列为 “eng”，英文；第三列为 “ch”，中文；第四列为 “detail”，英文的详细解释。列名不得有误。其中2、3两列用于判断用户输入的正确性以及在右上角显示框中显示原始文本。
## 2. sheet名
   sheet名应包含一些标记方便程序识别。在开头加上 “-” 为忽略标记（可选）；在末端加上 "-w" 为单词标记，代表这一页都是单词；在末端加上 "-s" 为句子标记，代表这一页都是句子。末尾没有 “-w” 或 “-s” 标记的程序一律不读。

