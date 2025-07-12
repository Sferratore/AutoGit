import os
import subprocess
from dotenv import load_dotenv

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
            content = f.read()
    except FileNotFoundError:
        content = ""

    # Add "I" in a new row
    content += "I"

    # Substitute IIII with V inside the document
    while "IIIII" in content:
        content = content.replace("IIII", "V")

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

if __name__ == "__main__":
    append_to_readme()
    commit()
    safe_push()
