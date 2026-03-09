# Tutorial: Run ClawBio Skills via a Telegram Bot

> **Production bot available**: If you want the full-featured bot with Claude-powered reasoning, medication photo detection, and the RoboTerri persona, see [`bot/roboterri.py`](../bot/roboterri.py) and its [README](../bot/README.md). The tutorial below builds a simpler version from scratch for learning purposes.

This tutorial walks you through building a Telegram bot that runs ClawBio skills. By the end, you'll be able to send a genetic data file to your bot and receive a pharmacogenomics report, equity score, or genome comparison — all running locally on your machine.

**Time**: ~20 minutes | **Difficulty**: Intermediate | **Prerequisites**: Python 3.11+, a Telegram account

---

## Table of Contents

1. [Overview](#1-overview)
2. [Prerequisites](#2-prerequisites)
3. [Clone and Install ClawBio](#3-clone-and-install-clawbio)
4. [Create a Telegram Bot](#4-create-a-telegram-bot)
5. [Get Your Telegram Chat ID](#5-get-your-telegram-chat-id)
6. [Set Up Your API Key](#6-set-up-your-api-key)
7. [Build the Bot](#7-build-the-bot)
8. [Run It](#8-run-it)
9. [Test It](#9-test-it)
10. [Next Steps](#10-next-steps)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Overview

```
You (Telegram)  →  Your bot (your machine)  →  ClawBio skills (local)
      ↑                                              │
      └──────── report + figures ←───────────────────┘
```

The bot you'll build:
- Accepts messages and genetic data files in Telegram
- Routes to the correct ClawBio skill via the CLI
- Runs the analysis **locally** — no genetic data leaves your machine
- Sends back a summary, report, and figures directly in Telegram

---

## 2. Prerequisites

| Requirement | Version | Check |
|---|---|---|
| Python | 3.11+ | `python3 --version` |
| pip | latest | `pip3 install --upgrade pip` |
| Git | any | `git --version` |
| Telegram | account + app | [telegram.org](https://telegram.org) |

### macOS

```bash
brew install python@3.11
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update && sudo apt install python3.11 python3.11-venv python3-pip
```

---

## 3. Clone and Install ClawBio

```bash
git clone https://github.com/ClawBio/ClawBio.git
cd ClawBio
pip3 install -r requirements.txt
```

Verify it works:

```bash
python3 clawbio.py list
python3 clawbio.py run pharmgx --demo
```

You should see a pharmacogenomics report generated in under 1 second.

---

## 4. Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Choose a **name** (e.g., "My ClawBio Agent")
4. Choose a **username** (must end in `bot`, e.g., `my_clawbio_bot`)
5. BotFather replies with your **bot token** — save it securely

> **Security**: Never share your bot token or commit it to Git. Treat it like a password.

### Optional: Set bot commands

Still in the BotFather chat, send `/setcommands`, select your bot, then paste:

```
start - Start the bot
demo - Run a ClawBio demo skill
```

---

## 5. Get Your Telegram Chat ID

Restrict your bot so only you can use it. To find your chat ID:

1. Start a conversation with your new bot (press **Start**)
2. Send any message (e.g., "hello")
3. Open this URL in your browser (replace `YOUR_BOT_TOKEN`):

```
https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
```

4. Look for `"chat":{"id":123456789}` — that number is your **chat ID**

Alternatively, search for **@userinfobot** on Telegram and send `/start`.

---

## 6. Set Up Your API Key

Install the Telegram bot library:

```bash
pip3 install "python-telegram-bot[job-queue]"
```

Create a file called `.env` in the ClawBio directory:

```
TELEGRAM_BOT_TOKEN=your-bot-token-here
TELEGRAM_CHAT_ID=your-chat-id-here
```

Add `.env` to your `.gitignore` so it never gets committed:

```bash
echo ".env" >> .gitignore
```

---

## 7. Build the Bot

Create a file called `telegram_bot.py` in the ClawBio directory:

```python
#!/usr/bin/env python3
"""Minimal Telegram bot that runs ClawBio skills."""

import os
import subprocess
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ALLOWED_CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])
CLAWBIO = Path(__file__).parent / "clawbio.py"


def is_authorised(update: Update) -> bool:
    return update.effective_chat.id == ALLOWED_CHAT_ID


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_authorised(update):
        return
    await update.message.reply_text(
        "ClawBio Telegram Bot\n\n"
        "Commands:\n"
        "  /demo <skill>  — Run a demo (pharmgx, equity, nutrigx, compare)\n"
        "  /list           — List available skills\n\n"
        "Or send a genetic data file (.txt, .csv, .vcf) to analyse it."
    )


async def list_skills(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_authorised(update):
        return
    result = subprocess.run(
        ["python3", str(CLAWBIO), "list"],
        capture_output=True, text=True, timeout=30,
    )
    await update.message.reply_text(f"```\n{result.stdout}\n```", parse_mode="Markdown")


async def demo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_authorised(update):
        return
    skill = ctx.args[0] if ctx.args else "pharmgx"
    await update.message.reply_text(f"Running {skill} demo...")

    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = ["python3", str(CLAWBIO), "run", skill, "--demo", "--output", tmpdir]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode != 0:
            await update.message.reply_text(f"Error:\n```\n{result.stderr[:2000]}\n```", parse_mode="Markdown")
            return

        # Send stdout summary
        if result.stdout.strip():
            for chunk in [result.stdout[i:i+4000] for i in range(0, len(result.stdout), 4000)]:
                await update.message.reply_text(chunk)

        # Send generated files (reports, figures)
        output = Path(tmpdir)
        for md_file in sorted(output.rglob("*.md")):
            await update.message.reply_document(document=open(md_file, "rb"))
        for img_file in sorted(output.rglob("*.png")):
            await update.message.reply_photo(photo=open(img_file, "rb"))


async def handle_file(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Auto-detect genetic file and run the appropriate skill."""
    if not is_authorised(update):
        return
    doc = update.message.document
    if not doc:
        return

    await update.message.reply_text(f"Received {doc.file_name}. Analysing...")

    # Download file
    tg_file = await doc.get_file()
    with tempfile.TemporaryDirectory() as tmpdir:
        local_path = Path(tmpdir) / doc.file_name
        await tg_file.download_to_drive(local_path)

        # Detect skill by extension
        ext = local_path.suffix.lower()
        if ext in (".txt", ".csv"):
            skill = "pharmgx"
        elif ext == ".vcf":
            skill = "equity"
        else:
            await update.message.reply_text(f"Unsupported file type: {ext}")
            return

        out_dir = Path(tmpdir) / "output"
        out_dir.mkdir()
        cmd = ["python3", str(CLAWBIO), "run", skill, "--input", str(local_path), "--output", str(out_dir)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode != 0:
            await update.message.reply_text(f"Error:\n```\n{result.stderr[:2000]}\n```", parse_mode="Markdown")
            return

        if result.stdout.strip():
            for chunk in [result.stdout[i:i+4000] for i in range(0, len(result.stdout), 4000)]:
                await update.message.reply_text(chunk)

        for md_file in sorted(out_dir.rglob("*.md")):
            await update.message.reply_document(document=open(md_file, "rb"))
        for img_file in sorted(out_dir.rglob("*.png")):
            await update.message.reply_photo(photo=open(img_file, "rb"))


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_skills))
    app.add_handler(CommandHandler("demo", demo))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    print("Bot is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
```

This is a self-contained bot (~100 lines) that:
- Restricts access to your chat ID only
- Runs `/demo pharmgx`, `/demo equity`, `/demo compare` etc.
- Auto-detects genetic file types when you send a document
- Sends back reports and figures

---

## 8. Run It

```bash
python3 telegram_bot.py
```

You should see:

```
Bot is running. Press Ctrl+C to stop.
```

### Run in the background (optional)

```bash
# Using nohup
nohup python3 telegram_bot.py > bot.log 2>&1 &

# Or using screen
screen -S clawbio-bot
python3 telegram_bot.py
# Detach: Ctrl+A, then D
# Reattach: screen -r clawbio-bot
```

---

## 9. Test It

Open your Telegram bot and try:

### List skills

```
You: /list
Bot: Available skills:
       pharmgx    Pharmacogenomics reporter ...
       equity     HEIM equity scorer ...
       ...
```

### Run a demo

```
You: /demo pharmgx
Bot: Running pharmgx demo...
     CYP2D6 *4/*4 — Poor Metabolizer → 10 drugs AVOID
     [report.md attached]
     [figures attached]
```

### Send your own genetic data

1. Export your 23andMe raw data (Settings > 23andMe Data > Download Raw Data)
2. Send the `.txt` file to the bot
3. The bot auto-detects the format and runs PharmGx Reporter

```
You: [attach 23andMe_raw_data.txt]
Bot: Received 23andMe_raw_data.txt. Analysing...
     CYP2C19 *1/*2 — Intermediate Metabolizer
     ...
```

---

## 10. Next Steps

- **Add more skills**: Extend `handle_file()` to route `.fastq` to metagenomics, or add keyword detection
- **Add Claude reasoning**: Use the [Anthropic SDK](https://docs.anthropic.com/en/docs/sdks) to add conversational AI around the skill results
- **Build your own skill**: See [CONTRIBUTING.md](../CONTRIBUTING.md) and the [skill template](../templates/SKILL-TEMPLATE.md)
- **Explore the architecture**: See [docs/architecture.md](architecture.md)
- **Watch the demo**: [ClawBio at UK AI Agent Hack](https://www.youtube.com/watch?v=eEEA71qSOmU)

---

## 11. Troubleshooting

### "ModuleNotFoundError: No module named 'telegram'"

```bash
pip3 install "python-telegram-bot[job-queue]"
```

### Bot doesn't respond

- Verify your chat ID matches what's in `.env`
- Check the bot token is correct (no extra spaces or quotes)
- Send `/start` to your bot first

### ClawBio skill fails

Run it standalone to isolate the issue:

```bash
python3 clawbio.py run pharmgx --demo
```

### Permission denied

Make sure `clawbio.py` is executable or invoke it via `python3`:

```bash
python3 clawbio.py run pharmgx --demo
```

---

*ClawBio is a research and educational tool. It is not a medical device and does not provide clinical diagnoses. Consult a healthcare professional before making any medical decisions.*
