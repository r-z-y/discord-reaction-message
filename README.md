# Discord Reaction Message

<div align="center">

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![License](https://img.shields.io/badge/license-MIT-purple)
![Language](https://img.shields.io/badge/language-python-blue)
![Python Version](https://img.shields.io/badge/python-3.6%2B-brightgreen)

</div>

Send messages on Discord using reaction emojis!

## 📋 Overview

Discord Reaction Message is a Python tool that allows you to send messages by adding letter reactions to Discord messages. Instead of typing text directly, the tool adds emoji reactions representing each letter of your message.

## ✨ Features

- Send messages using Discord reactions
- Works in any channel or DM where you have permission to add reactions
- Customizable with your own emoji set

## 🛠️ Installation

### Prerequisites

- Python 3.6+
- Discord account
- Server with permission to add custom emojis (for emoji setup)

### Clone the Repository

```bash
git clone https://github.com/r-z-y/discord-reaction-message/
cd discord-reaction-message
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Emoji Setup

1. Upload the emojis from the [emojis folder](https://github.com/r-z-y/discord-reaction-message/tree/main/emojies) to a Discord server
   - **Important:** Do not change their names (E.g: regional_indicator_a)
   - You need permissions to add emojis to the server

### Token Setup

1. Create or edit `token.txt` in the project root
2. Add your Discord user token to this file
   - If left empty, you'll be prompted to enter it when running the program

### Emoji ID Configuration

1. Create or edit `emoji_ids.txt` in the project root
2. Add your emoji IDs from A to Z in the following format:

```
1372671188144230430
1372670628062167123
1372670625239269416
...
```

To get emoji IDs:
1. Type `\:emoji_name:` in Discord to get the ID
2. The format will be `<:letter_a:1372671188144230430>` - you only need the number

## 🚀 Usage

Run the program:

```bash
python main.py
```

You'll be prompted for:
1. **Channel ID** - Right-click on the channel/DM and select "Copy Channel ID"
2. **Message ID** - Right-click on a message and select "Copy Message ID" (Reactions will start from this message)
3. **Message** - Type the message you want to send using reactions

The program will then add reactions representing each letter of your message to the specified Discord message.

## ⚠️ Limitations

- Special characters and numbers are not supported
- Discord has rate limits for adding reactions - sending very long messages may trigger these limits
- You need the required permission to add reactions in the target channel

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

<div align="center">
Made with ❤️ by <a href="https://github.com/r-z-y">r-z-y</a>
</div>
