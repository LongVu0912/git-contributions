import subprocess
import re
from collections import defaultdict

def get_all_contributors():
    result = subprocess.run(['git', 'shortlog', '-s', '-n', '-e'],
                            stdout=subprocess.PIPE,
                            text=True,
                            encoding='utf-8')
    contributors = result.stdout.strip().split('\n')
    return contributors

def extract_names_and_emails(contributors):
    email_name_map = {}
    email_pattern = re.compile(r'^\s*\d+\s+(.*?)\s+<(.+?)>$')
    for contributor in contributors:
        match = email_pattern.search(contributor)
        if match:
            name = match.group(1).strip()
            email = match.group(2).strip()
            email_name_map[email] = name
    return email_name_map

def get_contributions(author_email):
    result = subprocess.run(['git', 'log', '--author=' + author_email, '--pretty=format:', '--numstat'],
                            stdout=subprocess.PIPE,
                            text=True,
                            encoding='utf-8')
    contributions = defaultdict(int)
    lines = result.stdout.splitlines()
    for line in lines:
        if '\t' in line:
            added, deleted, _ = line.split('\t', 2)
            if added.isdigit() and deleted.isdigit():
                contributions[author_email] += int(added) + int(deleted)
    return contributions

contributors = get_all_contributors()
email_name_map = extract_names_and_emails(contributors)

for email, name in email_name_map.items():
    contributions = get_contributions(email)
    print(f'+ \033[94m{name}\033[0m (\033[92m{email}\033[0m): {contributions[email]} lines')