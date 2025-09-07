# aisdk discord bot

discord bot for monitoring vercel/ai

## setup

```bash
git clone https://github.com/dancer/aisdk.git
cd aisdk

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# add tokens and channel ids

python main.py
```

## commands

- `?help` - show help
- `?fetch <number>` - fetch issue/pr
- `?releases` - latest release
- `?issuesall` - import all issues
- `?prsall` - import all prs

## features

- monitors prs, issues, releases, npm
- auto reactions on close/merge
- persists state across restarts