# COVID-19-notice

![python](https://img.shields.io/github/pipenv/locked/python-version/yuto51942/COVID-19-notice)
![last_commit](https://img.shields.io/github/last-commit/yuto51942/COVID-19-notice)

[🇯🇵](../README.md)| 🇺🇸

![title](title.png)

## TL;DR

Send daily Japanese COVID-19 information summary to LINE.

## ⚙ Installing dependencies

Install from pipenv

```bash
pip install pipenv

# Install on virtual environment of pipenv
pipenv install

# Install on PC
pipenv install --system --deploy
```

## Get LINE notify

[\[超簡単\]LINE notify を使ってみる](https://qiita.com/iitenkida7/items/576a8226ba6584864d95)

Get the token referring to the above article.

## 🚀 Run

It is assumed that LINE Token has been acquired.

```bash
# Run
python src/main.py

# Run on sever(Ubuntu).
nohup python3 src/main.py --line-token [token] &
```

## ⚖️ LICENSE

[MIT LICENSE](../LICENSE)
