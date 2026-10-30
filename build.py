"""Render the privacy-scrubbed Page snapshot as a portable static website."""
import hashlib
import html
import json
from pathlib import Path

import markdown
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
source = json.loads((ROOT / 'page-source.json').read_text(encoding='utf-8'))
assets = {item['reference']: item['path'] for item in source['assets']}
rendered = []
navigation = []

for block in source['blocks']:
    text = block['markdown']
    for reference, path in assets.items():
        text = text.replace(reference, path)
    fragment = BeautifulSoup(markdown.markdown(text, extensions=['tables', 'fenced_code', 'sane_lists']), 'html.parser')
    for heading in fragment.select('h1, h2'):
        navigation.append((heading.name, block['id'], heading.get_text()))
    for image in fragment.select('img'):
        if image['src'].endswith('.html'):
            frame = fragment.new_tag('iframe', src='assets/support-workflow-view.html', title=image.get('alt', ''), loading='lazy', sandbox='allow-scripts')
            image.replace_with(frame)
        else:
            image['loading'] = 'lazy'
            image['decoding'] = 'async'
    for table in fragment.select('table'):
        wrapper = fragment.new_tag('div', attrs={'class': 'table-scroll', 'tabindex': '0'})
        table.wrap(wrapper)
    diagram = fragment.select_one('code.language-mermaid')
    if diagram and (ROOT / 'assets/support-architecture.svg').exists():
        pre = diagram.parent
        figure = fragment.new_tag('img', src='assets/support-architecture.svg', alt='Support intake and engineering review architecture', attrs={'class': 'architecture'})
        pre.insert_before(figure)
        details = fragment.new_tag('details')
        summary = fragment.new_tag('summary')
        summary.string = 'Diagram source'
        pre.wrap(details)
        details.insert(0, summary)
    rendered.append(f'<div class="page-block" id="{block["id"]}">{fragment}</div>')

nav = '\n'.join(f'<a class="{level}" href="#{block_id}">{html.escape(label)}</a>' for level, block_id, label in navigation)
title = html.escape(source['title'])
document = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<meta name="description" content="Complete visual tutorial from the Grok Bot Enterprise workshop, with screenshots and an interactive support workflow.">
<title>{title}</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<a class="skip" href="#tutorial">Skip to tutorial</a>
<aside><nav aria-label="Table of contents">{nav}</nav></aside>
<main id="tutorial">
<header><h1>{title}</h1></header>
<article>{''.join(rendered)}</article>
</main>
</body>
</html>
'''
(ROOT / 'index.html').write_text(document, encoding='utf-8', newline='\n')

fragment = (ROOT / 'assets/support-workflow.html').read_text(encoding='utf-8')
embedded = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Support workflow branches and human checkpoints</title><link rel="stylesheet" href="../styles.css"></head><body class="embed">{fragment}</body></html>
'''
(ROOT / 'assets/support-workflow-view.html').write_text(embedded, encoding='utf-8', newline='\n')

for item in source['assets']:
    assert hashlib.sha256((ROOT / item['path']).read_bytes()).hexdigest() == item['sha256'], item['path']
assert (ROOT / 'page-source.md').read_text(encoding='utf-8') == source['markdown']
assert len(BeautifulSoup(document, 'html.parser').select('.page-block')) == len(source['blocks'])
print(f"Rendered all {len(source['blocks'])} Page blocks; verified all six original asset hashes.")
