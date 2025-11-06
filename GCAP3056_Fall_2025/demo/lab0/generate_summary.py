import os
from pathlib import Path

INPUT_DIR = Path(__file__).parent.parent.parent / 'teacherNotes' / 'Chronic-Care' / 'DiscussionNotes'
OUTPUT_DIR = Path(__file__).parent / 'output'
OUTPUT_FILE = OUTPUT_DIR / 'summary.md'

import re
import requests
from bs4 import BeautifulSoup

def extract_url_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    urls = re.findall(r'https?://\S+', text)
    return urls[0] if urls else None

def fetch_url_content(url):
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        # Google Docs 頁面內容較複雜，僅抓取 <title> 作為示範
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = soup.title.string if soup.title else 'No title found'
        return f"## {title}\nURL: {url}\n"
    except Exception as e:
        return f"Failed to fetch {url}: {e}\n"

def generate_summary(url_summaries):
    summary = "# Summary of Discussion Notes (from URLs)\n\n"
    for content in url_summaries:
        summary += content + "\n"
    return summary


def main():
    if not INPUT_DIR.exists():
        print(f"Input directory {INPUT_DIR} does not exist.")
        return
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    url_summaries = []
    for fname in sorted(os.listdir(INPUT_DIR)):
        fpath = INPUT_DIR / fname
        if fpath.is_file() and fname.endswith(('.md', '.txt')):
            url = extract_url_from_file(fpath)
            if url:
                url_summaries.append(fetch_url_content(url))
    summary = generate_summary(url_summaries)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"Summary written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
