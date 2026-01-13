import os
import datetime
import json
import pickle
from parse import parse_dir

def attrs2str(story):
    return f'{story["name"]:<120}; {story["autor"] if story["autor"] else "<UNKNOWN AUTOR>":<20}; {story["time"].strftime("%d. %m. %Y")}; {story["labels"]}'

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

def load(source_dir = 'src', temp_file = 'parsed.json', force = False, update_temp = True):
    parse_src = force or not os.path.exists(temp_file)
    if parse_src:
        print('Parsing from source...')
        storybook = parse_dir(source_dir)
        print(f'{len(storybook)} stories parsed')
        if update_temp:
            if os.path.splitext(temp_file)[1] == '.json':
                print(f'Saving text to {temp_file}...')
                with open(temp_file, 'w', encoding='utf8') as f:
                    json.dump(storybook, f, default=str)
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
        for i, u in enumerate(uniques):
            if s['plaintext'] == u['plaintext']:
                if s['name'] != u['name']:
                    print(f'Two texts with different name:\n\t{attrs2str(s)}\n\t{attrs2str(u)}')
                    print('text1:')
                    print('\n'.join(s['text']))
                    print('text2:')
                    print('\n'.join(u['text']))
                if not u['autor']:
                    u['autor'] = s['autor']
                for l in s['labels']:
                    if l not in u['labels']:
                        u['labels'].append(l)
                break
        else:
            if s['plaintext']:
                uniques.append(s)
    return uniques
