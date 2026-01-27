import os
import zipfile
from bs4 import BeautifulSoup as BS
import datetime
import sys

#print(sys.getrecursionlimit())
sys.setrecursionlimit(1000000)

def parse_post(post):
    story = {}
    #story['name'] = bs.title.string.split(':', maxsplit=1)[-1].strip()
    #story['date'] = datetime.date(*map(lambda sn, offset: offset + int(sn), reversed(bs.find(class_='date-header').string.split('.')), (2000, 0 ,0)))
    story['name'] = ''.join(title.strings).strip() if (title := post.find('h3', class_='post-title entry-title')) else 'NO_NAME'
    text = post.find('div', class_='post-body entry-content')
    story['text'] = '\n'.join(str(k) for k in text.contents)
    story['plaintext'] = ' '.join(text.stripped_strings)
    footer = post.find('div', class_='post-footer')
    #story['autor'] = footer.find('span', class_='post-author vcard').span.string
    story['time'] = datetime.datetime.fromisoformat(footer.find('a', class_='timestamp-link').abbr['title'])
    story['labels'] = [k.string for k in footer.find('span', class_='post-labels').find_all('a')]
    return story

def parse_dir(path):
    storybook = []
    for file in os.listdir(path):
        filepath = os.path.join(path, file)
        if os.path.isfile(filepath):
            if os.path.splitext(file)[1] == '.html':
                with open(filepath, 'rb') as f:
                    print(filepath)
                    storybook.extend(parse_post(k) for k in BS(f, 'html.parser').find('div', class_='blog-posts hfeed').find_all('div', class_='date-outer'))
        else:
            storybook.extend(parse_dir(filepath))
    return storybook

def parse_zip(zip_path):
    storybook = []
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for file_info in zf.filelist:
            if file_info.filename.endswith('.html'):
                with zf.open(file_info.filename) as f:
                    print(file_info.filename)
                    try:
                        blog_posts = BS(f, 'html.parser').find('div', class_='blog-posts hfeed')
                        if blog_posts:
                            storybook.extend(parse_post(k) for k in blog_posts.find_all('div', class_='date-outer'))
                    except Exception as e:
                        print(f'Error parsing {file_info.filename}: {e}')
    return storybook

if __name__ == '__main__':
    storybook = parse_zip('src/aryonstory.blogspot.com.zip')
    print(f'Parsed {len(storybook)} stories.')
