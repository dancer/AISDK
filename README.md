# aisdk discord bot

[![Python](https://img.shields.io/badge/python-3.13-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Discord](https://img.shields.io/badge/discord.py-latest-7289da?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io)

**real-time monitoring for vercel/ai repository**

[Features](#features) • [Setup](#setup) • [Commands](#commands)

---

## features

<details>
<summary><b>monitoring</b></summary>

- **github** - pull requests, issues with auto reactions
- **npm** - package releases for ai sdk
- **persistence** - survives restarts, catches missed events

</details>

<details>
<summary><b>discord</b></summary>

- **channels** - #prs, #issues, #releases, #ai
- **embeds** - clean formatting with image support
- **reactions** - auto reactions for closed/merged items
- **ai channel** - enforces "ai" only messages

</details>

---

## setup

```bash
# clone
git clone https://github.com/dancer/aisdk.git && cd aisdk

# install
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# configure
cp .env.example .env
# add tokens and channel ids

# run
python main.py
```

<details>
<summary><b>environment</b></summary>

```env
DISCORD_TOKEN=your_bot_token
GITHUB_TOKEN=your_github_token
OWNER_ID=your_discord_id
CHANNEL_PRS=channel_id
CHANNEL_ISSUES=channel_id
CHANNEL_RELEASES=channel_id
CHANNEL_AI=channel_id
```

</details>

---

## commands

| command | description | access |
|---------|-------------|--------|
| `?help` | show help | all |
| `?helpowner` | list all commands | owner |
| `?init` | initialize timestamps | owner |
| `?fetch <id>` | fetch issue/pr | owner |
| `?releases` | latest github release | owner |
| `?npmlatest` | latest npm release | owner |
| `?npmall` | import all npm releases | owner |
| `?issuesall` | import all issues | owner |
| `?prsall` | import all prs | owner |
| `?rules` | display server rules | owner |
| `?welcome` | welcome message | owner |
| `?bugs` | bug reporting guide | owner |

---

**built for the ai sdk community**

[![GitHub](https://img.shields.io/github/stars/dancer/aisdk?style=social)](https://github.com/dancer/aisdk)