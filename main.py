import os
import subprocess
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone
import random

load_dotenv(override=True)

REPO_PATH = os.getenv("AUTOGIT_REPO_PATH")
COMMIT_MESSAGE = os.getenv("GIT_COMMIT_MESSAGE", "auto: updated commithist")
COMMITHIST_PATH = REPO_PATH + "/COMMITHIST.md"
TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

REMOTE_URL = f"https://{TOKEN}@github.com/{GITHUB_USERNAME}/AutoGit.git"

def ensure_https_remote():
    result = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=REPO_PATH, capture_output=True, text=True)
    current_url = result.stdout.strip()
    if not current_url.startswith("https://"):
        print("Imposto remote origin su HTTPS con token...")
        subprocess.run(['git', 'remote', 'set-url', 'origin', REMOTE_URL], cwd=REPO_PATH, check=True)

def append_to_commithist():
    try:
        with open(COMMITHIST_PATH, "r") as f:
            content = f.read().strip()
    except FileNotFoundError:
        content = ""

    if content:
        content += " I"
    else:
        content = "I"

    while "I I I I I" in content:
        content = content.replace("I I I I", "V")

    with open(COMMITHIST_PATH, "w") as f:
        f.write(content + "\n")

def commit():
    ensure_https_remote()
    subprocess.run(['git', 'add', 'COMMITHIST.md'], cwd=REPO_PATH, check=True)
    result = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=REPO_PATH)
    if result.returncode != 0:
        subprocess.run(['git', 'commit', '-m', COMMIT_MESSAGE], cwd=REPO_PATH, check=True)
    else:
        print("Nessuna modifica da committare.")

def safe_push():
    subprocess.run(['git', 'push', REMOTE_URL, 'HEAD:master'], cwd=REPO_PATH, shell=True, check=True)

def count_commits():
    today = datetime.today().strftime('%Y-%m-%d')

    url = f"https://api.github.com/search/commits?q=author:{GITHUB_USERNAME}+author-date:>={today}"

    headers = {
        "Accept": "application/vnd.github.cloak-preview",
        "Authorization": f"token {TOKEN}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    total_commits_today = data['total_count']
    return total_commits_today

if __name__ == "__main__":
    num_commits = random.randint(5, 11)
    if(count_commits() < 4):
        for i in range(num_commits):
            append_to_commithist()
            commit()
            safe_push()

