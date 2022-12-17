import html2text as ht
text_maker = ht.HTML2Text()
text_maker.bypass_tables = False

def html_2_markdown(html: str):
    text = text_maker.handle(html)
    return text

