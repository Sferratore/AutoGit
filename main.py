import os
from git import Repo
from dotenv import load_dotenv

load_dotenv()

REPO_PATH = os.getenv("AUTOGIT_REPO_PATH")
COMMIT_MESSAGE = os.getenv("GIT_COMMIT_MESSAGE", "auto: updated readme")
README_PATH = os.path.join(REPO_PATH, "README.md")

def append_to_readme():
    with open(README_PATH, "a") as f:
        f.write("a\n")

def commit_and_push():
    repo = Repo(REPO_PATH)
    repo.git.add('README.md')
    repo.index.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    origin.push()

if __name__ == "__main__":
    append_to_readme()
    commit_and_push()