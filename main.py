import os
import subprocess
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

REPO_PATH = os.getenv("AUTOGIT_REPO_PATH")
COMMIT_MESSAGE = os.getenv("GIT_COMMIT_MESSAGE", "auto: updated readme")
README_PATH = REPO_PATH + "/README.md"
TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

REMOTE_URL = f"https://{TOKEN}@github.com/{GITHUB_USERNAME}/AutoGit.git"

def ensure_https_remote():
    result = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=REPO_PATH, capture_output=True, text=True)
    current_url = result.stdout.strip()
    if not current_url.startswith("https://"):
        print("Imposto remote origin su HTTPS con token...")
        subprocess.run(['git', 'remote', 'set-url', 'origin', REMOTE_URL], cwd=REPO_PATH, check=True)

def append_to_readme():
    # Read README content
    try:
        with open(README_PATH, "r") as f:
            content = f.read().strip()
    except FileNotFoundError:
        content = ""

    # Add "I" next to the previous character with a space if needed
    if content:
        content += " I"
    else:
        content = "I"

    # Substitute every occurrence of "I I I I" with "V"
    while "I I I I I" in content:
        content = content.replace("I I I I", "V")

    # Write README with updated content
    with open(README_PATH, "w") as f:
        f.write(content + "\n")

def commit():
    ensure_https_remote()
    subprocess.run(['git', 'add', 'README.md'], cwd=REPO_PATH, check=True)
    # Commit solo se ci sono modifiche
    result = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=REPO_PATH)
    if result.returncode != 0:
        subprocess.run(['git', 'commit', '-m', COMMIT_MESSAGE], cwd=REPO_PATH, check=True)
    else:
        print("Nessuna modifica da committare.")

def safe_push():
    subprocess.run(['git', 'push', REMOTE_URL, 'HEAD:master'], cwd=REPO_PATH, shell=True, check=True)

def count_commits():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/events"
    headers = {"Authorization": f"token {TOKEN}"}

    response = requests.get(url, headers=headers)
    events = response.json()

    today = datetime.now(timezone.utc).date()

    total_commits_today = 0

    for event in events:
        if event["type"] == "PushEvent":
            created_at = datetime.fromisoformat(event["created_at"].replace("Z", "+00:00")).date()
            if created_at == today:
                total_commits_today += len(event["payload"]["commits"])
    return total_commits_today

if __name__ == "__main__":
    append_to_readme()
    if(count_commits() < 4):
        for i in range(7):
            commit()
    safe_push()
