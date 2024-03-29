import re

def get_title(page_text):
    ex = '"title":"(.+?)"'
    article_title = re.findall(ex, page_text, re.S)
    for title in article_title:
        if title != 'true' and title != 'false':
            return title.replace("<inf>", "").replace("</inf>", "")


def get_abstract(page_text):
    ex = '"abstract":"(.+?)",'
    article_abstract = re.findall(ex, page_text, re.S)
    for abstract in article_abstract:
        if abstract != 'true' and abstract != 'false':
            return abstract


def get_published(page_text):
    ex = '"publicationTitle":"(.+?)"'
    article_published = re.findall(ex, page_text, re.S)
    for published in article_published:
        if published != 'true' and published != 'false':
            return published


def get_date(page_text):
    ex = '"insertDate":"(.+?)"'
    article_date = re.findall(ex, page_text, re.S)
    for date in article_date:
        if date != 'true' and date != 'false':
            return date


def get_kwd(page_text):
    ex = '"type":"IEEE Keywords","kwd":(.+?)}'
    article_kwd = re.findall(ex, page_text, re.S)
    for kwd in article_kwd:
        if kwd != 'true' and kwd != 'false':
            return kwd.replace('[', '').replace(']', '')
            


