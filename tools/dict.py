import os

from readmdict import MDX  # pip install readmdict
from mk import html_2_markdown

words_file = '200dic.txt'
# step1 
# 本机词典库根目录
root_path = "/home/hammer/Documents/词典词库"
root_path = "D:\\DicRes"

def load_dic_content(dic_name):
    """
     mdx字典文本，返回字列表和内容列表
    :param dic_name:
    :return:
    """
    # 遍历文件
    full_path = root_path + dic_name
    headwords = [*MDX(full_path)]  # 单词名列表
    items = [*MDX(full_path).items()]  # 释义html源码列表
    if len(headwords) == len(items):
        print(f'Dictionary Load Success, Length：{len(headwords)}')
    else:
        print(f'Dictionary Load Fail {len(headwords)}，{len(items)}')
        raise Exception("words and headwords.len != items.len")
    return headwords, items


def assemble_mk(word, *args):
    _mk_template = f"""#dic

## {word}
??
***
{args[0]}
***
![](https://ssl.gstatic.com/dictionary/static/sounds/oxford/{word}--_gb_1.mp3#play&loop)"""
    return _mk_template


def query_dic(headwords, items, queryWord: str, ignore_line_start=0, ignore_line_end=0):
    """
    查词，返回单词和markdown文件
    :param headwords:
    :param items:
    :param queryWord:
    :param ignore_line_start:
    :param ignore_line_end:
    :return:
    """
    try:
        wordIndex = headwords.index(queryWord.encode())
        word, html = items[wordIndex]
        word, html = word.decode(), html.decode()
        # print(f'word {word}')
        # print(f'html {html}')
        # html转markdown
        _mk = html_2_markdown(html)
        return word, _mk
    except Exception as e:
        print(f'query_dic,{e}')
        return "", ""


if __name__ == '__main__':
    try:
        _output = os.path.split(os.path.realpath(__file__))[0]

        # 1小词典
        # headwords, items = load_dic_content('/The Little Dict big/TLD.mdx')
        headwords, items = load_dic_content('\\TheLittleDictbig/TLD.mdx')
        # 2加载词源
        _input_path = _output+'/2023核心词.txt'
        with open(_input_path, "r", encoding="utf-8") as inp_txt:
            for line in inp_txt.readlines():
                line = line.strip('\n')
                # 3查询单词 获得markdown
                _word, _mk = query_dic(headwords, items, line)
                if _word == "":
                    continue
                # 4生成词典文本
                _template = assemble_mk(_word, _mk)
                # 5保存
                _output_path = _output + f'/output/{_word}.md'
                with open(_output_path, "w", encoding="utf-8") as wordFile:
                    wordFile.write(_template)
                    print(f'{_word} success!')



    except Exception as e:
        print(e)
