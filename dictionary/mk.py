import html2text as ht
from bs4 import BeautifulSoup

text_maker = ht.HTML2Text()
text_maker.bypass_tables = False

def html_2_markdown(html: str):
    """
    针对小词典 html转makrdown
    :param html:
    :return:
    """
    # todo 使用class选择器 选择class="coca iweb" class="coca2" class="gdc"
    soup = BeautifulSoup(html, 'html.parser')
    # rank
    # _rank = soup.select('.coca')

    _desc = soup.select('.coca2')

    _detail = soup.select('.gdc')

    _filter_html = f"""
    {_desc[0] if len(_desc) > 0 else ''}
    {_detail[0] if len(_detail) > 0 else ''}
    """
    # return _filter_html
    # html转为markdown
    text = text_maker.handle(_filter_html)
    return text

