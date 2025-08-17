# AutoGit

**AutoGit** automatically executes commits and pushes on its own GitHub repository, updating the `README.md` file according to the logic implemented in the script.

---

## 🚀 Installation

### 1. Fork the repository
Create a fork of this repository on your GitHub account.

### 2. Clone the repository locally
```bash
git clone https://github.com/<your-username>/AutoGit.git
cd AutoGit
```

### 3. Create and activate the virtual environment with Pipenv
If you don't have `pipenv` yet, install it:
```bash
pip install pipenv
```
Then install the project dependencies:
```bash
pipenv install
```
> This command reads `Pipfile.lock` and recreates the environment with the correct versions.

---

## ⚙️ Configuration

### 4. Create the `.env` file
In the project folder, create a `.env` file with the following content:

```env
AUTOGIT_REPO_PATH=./
GIT_COMMIT_MESSAGE=auto: updated commithist
GITHUB_TOKEN=your_personal_access_token
GITHUB_USERNAME=your_github_username
```

**Notes:**
- `GITHUB_TOKEN`: must be a Personal Access Token (PAT) with **Read/Write** permissions on the repository.
- `AUTOGIT_REPO_PATH`: path to the local repository folder (you can leave `./` if the `.env` file is in the repo root).

---

## ▶️ Execution

### 5. Local test
Run the AutoGit batch script to test:

### 6. Schedule for daily operation
If it works correctly, schedule it to run daily on your PC using:
- **Windows**: Task Scheduler
- **Linux/macOS**: cron jobs
