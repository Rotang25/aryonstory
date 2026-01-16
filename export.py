import os
import json
import base64
from load import get_uniques

def export_to(stories=None, file='web/Aryon.html'):
    """
    Exportuje povídky do jednoho kompaktního HTML souboru.
    
    Args:
        stories: List povídek. Pokud je None, načte se pomocí get_uniques()
        file: Cesta a název výstupního HTML souboru
    """
    # Načti povídky, pokud nejsou poskytnuty
    if stories is None:
        print('Loading stories from get_uniques()...')
        stories = get_uniques()
    
    print(f'Exporting {len(stories)} stories to {file}...')
    
    # Načti index.html
    with open('web/index.html', 'r', encoding='utf8') as f:
        html_content = f.read()
    
    # Načti vue.js
    with open('web/vue.js', 'r', encoding='utf8') as f:
        vue_content = f.read()
    
    # Příprava dat povídek
    stories_json = json.dumps(stories, default=str, ensure_ascii=False, indent=2)
    
    # Zakóduj Vue.js na base64 - to zabezpečí, aby </script> tagy v obsahu nezpůsobily problémy
    vue_content_b64 = base64.b64encode(vue_content.encode('utf-8')).decode('ascii')
    
    # Nahraď linkované skripty inline verzí
    # 1. Nahraď Vue.js script - dekóduj z base64 a vykonaj
    html_content = html_content.replace(
        '<script src="vue.js"></script>',
        f'<script>eval(atob("{vue_content_b64}"))</script>'
    )
    
    # 2. Nahraď aryon.js za inline storiesData
    html_content = html_content.replace(
        '<script src="aryon.js"></script>',
        f'<script>const storiesData = {stories_json};</script>'
    )
    
    # Ulož do souboru
    with open(file, 'w', encoding='utf8') as f:
        f.write(html_content)
    
    print(f'Done! File saved to {file}')

if __name__ == '__main__':
    export_to()
