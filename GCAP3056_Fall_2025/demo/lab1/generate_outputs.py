import os
from pathlib import Path
import re

INPUT_DIR = Path(__file__).parent / 'input'
OUTPUT_DIR = Path(__file__).parent / 'output'
ISSUES_FILE = OUTPUT_DIR / 'issues_to_address.md'
QUESTIONS_FILE = OUTPUT_DIR / 'questions_for_government.md'

# 解析 Issues
ISSUE_HEADERS = ['### Issues and Gaps', '### Issues', '### Gaps']
QUESTION_HEADERS = ['### Questions for Government', '### Questions']

def extract_section(lines, header_list):
    section = []
    in_section = False
    for line in lines:
        if any(h in line for h in header_list):
            in_section = True
            continue
        if in_section:
            if line.strip().startswith('###') and not any(h in line for h in header_list):
                break
            if line.strip():
                section.append(line.strip())
    return section

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    all_issues = []
    all_questions = []
    for fname in os.listdir(INPUT_DIR):
        if fname.endswith('.md') and fname != 'template_public_info.md':
            with open(INPUT_DIR / fname, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            issues = extract_section(lines, ISSUE_HEADERS)
            questions = extract_section(lines, QUESTION_HEADERS)
            if issues:
                all_issues.append(f'# {fname}\n' + '\n'.join(issues) + '\n')
            if questions:
                all_questions.append(f'# {fname}\n' + '\n'.join(questions) + '\n')
    with open(ISSUES_FILE, 'w', encoding='utf-8') as f:
        f.write('# Issues to Address\n\n' + '\n'.join(all_issues))
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        f.write('# Questions for Government\n\n' + '\n'.join(all_questions))
    print(f"Generated {ISSUES_FILE} and {QUESTIONS_FILE}")

if __name__ == "__main__":
    main()
