import accNoExp
import accSafariBook
import requests
import re
import urllib
import json
import os
import sys


# testfile.retrieve("https://www.safaribooksonline.com/library/view/secrets-of-the/9781617292859/cover.jpg",
#                   "./img/cover.jpg")


def get_session():
    acc = accNoExp.get()
    s = accSafariBook.login(acc['username'], acc['password'])
    return s

reload(sys)
sys.setdefaultencoding('utf-8')
s = get_session()


###########################################

def get_id_book(url):
    for id_book in url.split('/'):
        if re.match('^\d+$', id_book):
            return id_book


def get_chapters_url(id):
    url = "https://www.safaribooksonline.com/api/v1/book/" + str(id)
    chapters = json.loads(s.get(url).content)['chapters']
    return chapters


def get_json_chapter(url):
    return json.loads(s.get(url).content)


def get_content_chapter(json_):
    content = s.get(json_['content']).content
    return content


def modify_source_chapter(source, images):
    for image in images:
        source = re.sub(r'src="' + image + '"', 'src="imgs/' + image + '"', source)
    source = re.sub(r'.xhtml', '.html', source)
    return source


def save_one_chap(url):
    if not os.path.exists("./imgs"):
        os.makedirs("./imgs")
    json_ = get_json_chapter(url)

    # save_image
    images = json_['images']
    if len(images) > 0:
        base_url = json_['asset_base_url']
        for image in images:
            urllib.urlretrieve(base_url + image, './imgs/' + image)

    # save_html
    file_name = re.sub(r'.xhtml', '.html', json_['full_path'])
    source_ = get_content_chapter(json_)
    if len(images) > 0:
        source_ = modify_source_chapter(source_, images)
    f = open(file_name, 'w')
    f.write(source_)
    f.close()


idx = get_id_book("https://www.safaribooksonline.com/api/v1/book/9781617292859/chapter/kindle_split_001.html")
chaps = get_chapters_url(idx)
for chap in chaps:
    save_one_chap(chap)
