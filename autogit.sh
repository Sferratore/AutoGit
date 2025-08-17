cat > autogit.sh <<'EOF'
#!/usr/bin/env bash
set -e
cd "$HOME/Desktop/AutoGit"
git pull
source .venv/bin/activate
python3 main.py
EOF
chmod +x autogit.sh
./autogit.sh