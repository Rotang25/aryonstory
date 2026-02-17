import os
import datetime
import json
import pickle
from parse import parse_dir, parse_zip

def attrs2str(story):
    return f'{story["name"]:<80}; {story["autor"] if story["autor"] else "<UNKNOWN AUTOR>":<20}; {story["time"].strftime("%d. %m. %Y")}; {story["labels"]}'

def load_temp(path):
    if os.path.splitext(path)[1] == '.json':
        with open(path, 'r', encoding='utf8') as f:
            raw = json.load(f)
            for k in raw:
                k['time'] = datetime.datetime.fromisoformat(k['time'])
            return raw
    else:
        with open(path, 'rb') as f:
            return pickle.load(f)

def load(source = 'src/aryonstory.blogspot.com.zip', temp_file = 'parsed.json', force = False, update_temp = True):
    parse_src = force or not os.path.exists(temp_file)
    if parse_src:
        print('Parsing from source...')
        if os.path.isfile(source) and os.path.splitext(source)[1] == '.zip':
            storybook = parse_zip(source)
        else:
            storybook = parse_dir(source)
        print(f'{len(storybook)} stories parsed')
        if update_temp:
            if os.path.splitext(temp_file)[1] == '.json':
                print(f'Saving text to {temp_file}...')
                with open(temp_file, 'w', encoding='utf8') as f:
                    json.dump(storybook, f, default=str, ensure_ascii=False, indent=2)
            else:
                print(f'Saving binary to {temp_file}...')
                with open(temp_file, 'wb') as f:
                    pickle.dump(storybook, f)
            print('Done')
    else:
        print(f'Loading from {temp_file}...')
        storybook = load_temp(temp_file)
        print(f'{len(storybook)} stories loaded')
    return storybook

def get_uniques(storybook = None):
    if storybook is None:
        storybook = load()
    uniques = []
    for s in storybook:
        for u in uniques:
            if s['plaintext'] == u['plaintext']:
                if s['name'] != u['name']:
                    print(f'Two texts with different name:\n\t{attrs2str(s)}\n\t{attrs2str(u)}')
                    print('text1:')
                    print('\n'.join(s['text']))
                    print('text2:')
                    print('\n'.join(u['text']))
                for l in s['labels']:
                    if l not in u['labels']:
                        u['labels'].append(l)
                break
        else:
            if s['plaintext']:
                uniques.append(s)
    for s in uniques:
        del s['plaintext']
    return uniques

def save_to(storybook, path):
    if os.path.splitext(path)[1] == '.js':
        print(f'Saving to {path}...')
        with open(path, 'w', encoding='utf8') as f:
            f.write('const storiesData = ')
            json.dump(storybook, f, default=str, ensure_ascii=False, indent=2)
            f.write(';')
        print('Done')

if __name__ == '__main__':
    stories = load(force=True, update_temp=True)
    uniques = get_uniques(stories)
    print(f'{len(uniques)} unique stories found')
    save_to(uniques, 'web/aryon.js')
