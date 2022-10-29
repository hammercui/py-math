from readmdict import MDX  # pip install readmdict

words_file = '200dic.txt'
# step1 
# 本机词典库根目录
root_path = "/home/hammer/Documents/词典词库"


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


def query_dic(headwords, items, queryWord: str, ignore_line_start=0, ignore_line_end=0):
    # 查词，返回单词和html文件
    try:
        wordIndex = headwords.index(queryWord.encode())
        word, html = items[wordIndex]
        word, html = word.decode(), html.decode()
        print(f'word {word}')
        print(f'html {html}')
        # markdown = html2text.html2text(html)
        # lines = markdown.splitlines()
        # res = ''
        # for i, line in enumerate(lines):
        #     if i < ignore_line_start:
        #         continue
        #     if len(lines) - i < ignore_line_end + 1:
        #         continue
        #     if line == '':
        #         continue
        #     res += f"{line}\n"
        # return res.rstrip()
    except Exception as e:
        raise e


if __name__ == '__main__':
    try:
        # 1小词典
        headwords, items = load_dic_content('/The Little Dict big')
        query_dic(headwords, items, "can")
    except Exception as e:
        print(f'err: {e}')
