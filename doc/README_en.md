# 🦠 COVID-19 to LINE

![python](https://img.shields.io/github/pipenv/locked/python-version/yuto51942/COVID-19-notice)
![last_commit](https://img.shields.io/github/last-commit/yuto51942/COVID-19-notice)

[🇯🇵](../README.md)| 🇺🇸

![title](title.png)

## TL;DR

- At 00:00, the information on the COVID-19 infected person of the previous day will be sent to LINE notify.
- The total number of infected people in the country is accessed on the WebAPI every hour and sent to LINE notify when it is updated.

## 🔍 Data source

[covid19-japan-web-api](https://github.com/ryo-ma/covid19-japan-web-api)

## ⚠️ Notes

The data was collected by volunteers.\
Please check the Ministry of Health, Labor and Welfare and other public organizations for accurate data.

## 💻 Environment

- MacOS
- Ubuntu 18.04

## ⚙ Installing dependencies

Install from pipenv

```bash
pip install pipenv

# Install on virtual environment of pipenv
pipenv install

# Install on PC
pipenv install --system --deploy
```

## 🔐 Get LINE notify

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
