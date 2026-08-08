# file-sorting-script
一个能够按文件类型自动分类整理的 Python 小工具，能把文件夹里乱七八糟的文件按类型自动归类。

# 终端运行教程(~/Downloads改为文件夹地址）
# 整理当前目录
python organize.py

# 整理指定文件夹
python organize.py ~/Downloads

# 先预览，看看会怎么移动（不实际执行）
python organize.py ~/Downloads --dry-run

# 如果要用自己的规则文件
python organize.py ~/Downloads --rules my_rules.json
功能特点
支持 8 种默认分类（图片、文档、视频、音频、压缩包、代码、字体、安装包）

不认识的格式自动归到"其他"

重名文件自动加序号，不会覆盖

支持预览模式，先看再决定要不要执行

支持自定义规则，改 rules.json 就行

纯 Python 标准库，不需要装任何第三方包
# 规则文件的规则
编辑 rules.json，格式如下
# {
#    "分类名": [".后缀1", ".后缀2"],
#    "另一个分类": [".后缀3"]
# } 
比如你想把 .torrent 文件单独分一类，就在 rules.json 里加上
"种子": [".torrent"]


