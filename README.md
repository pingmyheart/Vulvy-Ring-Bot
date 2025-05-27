# VULVY-RING-BOT

*All-in-One Telegram Contraceptive Notification Bot*

![Last Commit](https://img.shields.io/github/last-commit/pingmyheart/Vulvy-Ring-Bot)
![Repo Size](https://img.shields.io/github/repo-size/pingmyheart/Vulvy-Ring-Bot)
![Issues](https://img.shields.io/github/issues/pingmyheart/Vulvy-Ring-Bot)
![Pull Requests](https://img.shields.io/github/issues-pr/pingmyheart/Vulvy-Ring-Bot)
![License](https://img.shields.io/github/license/pingmyheart/Vulvy-Ring-Bot)
![Top Language](https://img.shields.io/github/languages/top/pingmyheart/Vulvy-Ring-Bot)
![Language Count](https://img.shields.io/github/languages/count/pingmyheart/Vulvy-Ring-Bot)

## 🚀 Overview

**Vulvy-Ring-Bot** is a privacy-first, multilingual Telegram bot designed to help users manage contraceptive ring cycles
with timely notifications, calendar integration, and personalized settings.

## ✨ Features

- 📅 **Cycle Calendar:** Visualize your ring schedule and upcoming events.
- ⏰ **Smart Reminders:** Get notified for insertion, removal, and replacement.
- 🌍 **Multilingual:** Supports English, Italian, Spanish, French, and German.
- 🔒 **Privacy-First:** No unnecessary data collection.
- 🛠️ **Easy Configuration:** Intuitive commands and interactive setup.
- 📍 **Timezone Awareness:** Accurate reminders based on your location.

## 🛠️ Getting Started

### Prerequisites

- Python 3.8+
- MongoDB (for persistent storage)
- [pip](https://pip.pypa.io/en/stable/)
- Telegram Bot Token from [@BotFather](https://t.me/botfather)

### Installation

#### Native Installation

1. Clone the repository

```bash
git clone https://github.com/pingmyheart/Vulvy-Ring-Bot.git
cd Vulvy-Ring-Bot
pip install -r requirements.txt
```

2. Set up environment variables

```bash
export MONGODB_USERNAME=root
export MONGODB_PASSWORD=root
export MONGODB_HOST=localhost
export MONGODB_DB=VulvyRing

export TG_BOT_TOKEN=XXXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

#### Docker Installation

1. Pull the docker image

```bash
docker pull pingmyheart/vulvy-ring-bot:${VERSION}
```

2. Run the container

```yaml
services:
  mongodb:
    image: mongo:latest
    environment:
      - MONGO_INITDB_ROOT_USERNAME=root
      - MONGO_INITDB_ROOT_PASSWORD=root
    volumes:
      - mongodb_data:/data/db
  vulvy-ring-bot:
    image: pingmyheart/vulvy-ring-bot:${VERSION}
    environment:
      - MONGODB_USERNAME=root
      - MONGODB_PASSWORD=root
      - MONGODB_HOST=mongodb
      - MONGODB_DB=VulvyRing
      - TG_BOT_TOKEN=XXXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```