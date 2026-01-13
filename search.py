import re
import pprint
from load import get_uniques, attrs2str

# for i, story in enumerate(storybook, 1):
#    if any(k in story['labels'] for k in ('Velikonoce', 'Darina', 'advoracek')):
#        print(f"{story['time']}: {story['name']}\t{story['labels']}")
   #

def print_content(storybook = None):
    if storybook is None:
        storybook = get_uniques()
    for i, story in enumerate(storybook, 1):
        print(f"{i:4}: {story['name']:_<80} {story['time'].strftime('%d.%m.%y')} {story['labels']}")

def get_lists(attrs = ('name', 'autor', 'time', 'labels'), only_idxs = False, storybook = None):
    def add_index(src, attr, dct, idx):
        if src[attr] in dct:
            dct[src[attr]].append(idx)
        else:
            dct[src[attr]] = [idx]
    res = {k: {} for k in attrs}
    if storybook is None:
        storybook = get_uniques()
        res['storybook'] = storybook
    for i, s in enumerate(storybook):
        for attr in attrs:
            if attr == 'labels':
                for l in s[attr]:
                    add_index((l,), 0, attr, i if only_idxs else s)
            else:
                add_index(s, attr, res[attr], i if only_idxs else s)
    return res
        
def print_lists(attrs = ('name', 'autor', 'time', 'labels'), storybook = None):
    attrs = get_lists(storybook, attrs, only_idxs=True)
    pp = pprint.PrettyPrinter(indent=4)
    for attr in attrs:
        if attr == 'storybook':
            continue
        print(f'{attr}:')
        pp.pprint(attrs[attr])
        print()

def search_fulltext(pattern, attrs = ('plaintext', 'name', 'labels'), case_sensitive = False, storybook = None):
    if storybook is None:
        storybook = get_uniques()
    print('Results for', pattern, ':')
    res = []
    r = re.compile(pattern, 0 if case_sensitive else re.IGNORECASE)
    for s in storybook:
        for attr in attrs:
            if attr == 'labels':
                if any(filter(r.match, s[attr])):
                    res.append(s)
            else:
                if r.match(s[attr]):
                    res.append(s)
    for s in sorted(res, key=lambda story: story['name']):
       print(attrs2str(s))

search_fulltext('velikonoce')
