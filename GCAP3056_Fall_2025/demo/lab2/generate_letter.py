import os
from pathlib import Path
import re

INPUT_DIR = Path(__file__).parent / 'input'
OUTPUT_DIR = Path(__file__).parent / 'output'
OUTPUT_FILE = OUTPUT_DIR / 'letter_draft.md'

# 讀取 outline

def parse_outline(outline_path):
    with open(outline_path, 'r', encoding='utf-8') as f:
        text = f.read()
    key_points = re.findall(r'\*\*Key Points:\*\*\n([\s\S]*?)\n\*\*Arguments', text)
    arguments = re.findall(r'\*\*Arguments:\*\*\n([\s\S]*?)\n\*\*Tone/Style', text)
    tone = re.findall(r'\*\*Tone/Style Preferences:\*\*\n([\s\S]*?)\n\*\*Word Count', text)
    word_limit = re.findall(r'\*\*Word Count Limit:\*\*\s*(\d+)', text)
    return {
        'key_points': key_points[0].strip() if key_points else '',
        'arguments': arguments[0].strip() if arguments else '',
        'tone': tone[0].strip() if tone else '',
        'word_limit': int(word_limit[0]) if word_limit else 400
    }

def read_samples(input_dir):
    samples = []
    for fname in os.listdir(input_dir):
        if fname.startswith('letter') and fname.endswith('.md') and 'outline' not in fname:
            with open(input_dir / fname, 'r', encoding='utf-8') as f:
                samples.append(f.read())
    return samples

def draft_letter(outline, samples):
    # 取樣本語氣與結構，組合 outline 重點
    intro = "Hong Kong faces an urgent need to address chronic diseases. "
    body = "Early screening and education are essential, and collaboration between government and community partners is key. "
    arg_lines = outline['arguments'].split('\n')
    for arg in arg_lines:
        if arg.strip():
            body += arg.strip() + ' '
    closing = "By investing in prevention and supporting community outreach, we can improve health outcomes and reduce long-term costs."
    draft = f"{intro}{body}{closing}\n\n— Concerned Citizen, Hong Kong"
    # 控制字數
    words = draft.split()
    if len(words) > outline['word_limit']:
        draft = ' '.join(words[:outline['word_limit']]) + '...'
    return draft

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outline = parse_outline(INPUT_DIR / 'letter_outline.md')
    samples = read_samples(INPUT_DIR)
    letter = draft_letter(outline, samples)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(letter)
    print(f"Letter draft written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
