# Grok Bot Enterprise Workshop Complete Visual Tutorial

[Read the live tutorial](https://az9713.github.io/grokbot-enterprise-tutorial/).

This website is an HTML export of the **Grok Bot Enterprise Workshop Complete Visual Tutorial** Page. It preserves all 175 content blocks in order, the five original workshop screenshots, source links, code examples, architecture diagram, and interactive support-workflow model. Personal references and private Page identifiers have been removed; email addresses are preserved.

## Video source

**[Grok Bot for Enterprise Teams by Santi Garza and Anahita Sahu](https://www.youtube.com/watch?v=jcKcAfJtTlk)** is the original workshop video. The Page identifies its publication date as October 29, 2026 and its duration as 55:15. Santi leads the demonstrations and Anahita moderates and answers questions.

The tutorial distinguishes workshop demonstrations and presenter claims from added explanations and documentation. It is a teaching companion, not a verbatim transcript of the video. Workshop content is retained with privacy edits to the exported tutorial.

## Files

- `index.html`: rendered tutorial, ready for GitHub Pages.
- `styles.css`: responsive dark appearance and print styling.
- `assets/`: original screenshots and interactive HTML, a standalone interactive wrapper, and a rendered architecture diagram.
- `page-source.md`: tutorial Markdown with personal references and private file identifiers removed.
- `page-source.json`: content blocks with local block IDs and original asset hashes for reproducibility.
- `build.py`: static HTML generator; no build step runs in the published website.

## Rebuild and preview

```sh
python -m pip install -r requirements.txt
python build.py
python -m http.server 8000
```

Open `http://localhost:8000`. The generator checks the original asset hashes and confirms that all 175 Page blocks are included. The architecture SVG is a committed rendering of the original Mermaid source, which remains available in the tutorial.

GitHub Pages serves the repository's `main` branch from `/`. Runtime assets are included locally; the site needs no CDN or third-party JavaScript.
