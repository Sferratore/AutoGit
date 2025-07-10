import os
from git import Repo
from git import GitCommandError
from dotenv import load_dotenv

load_dotenv()

REPO_PATH = os.getenv("AUTOGIT_REPO_PATH")
COMMIT_MESSAGE = os.getenv("GIT_COMMIT_MESSAGE", "auto: updated readme")
README_PATH = REPO_PATH + "/README.md"
TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

REMOTE_URL = f"https://{TOKEN}@github.com/{GITHUB_USERNAME}/AutoGit.git"

def ensure_https_remote(repo):
    current_url = repo.remotes.origin.url
    if not current_url.startswith("https://"):
        print("Imposto remote origin su HTTPS con token...")
        repo.git.remote("set-url", "origin", REMOTE_URL)

def append_to_readme():
    with open(README_PATH, "a") as f:
        f.write("a\n")

def commit_and_push():
    repo = Repo(REPO_PATH)
    ensure_https_remote(repo)
    repo.git.add('README.md')
    try:
        repo.index.commit(COMMIT_MESSAGE)
    except GitCommandError:
        return
    repo.git.push(REMOTE_URL, 'HEAD:main')

if __name__ == "__main__":
    append_to_readme()
    commit_and_push()