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

Windows has not been tested.

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

## ✅ Static analysis

- Pylint
- mypy
- flake8

```bash
pipenv install --dev
pipenv shell
sh ./analysis.sh
```

Make sure you check all the tools successfully when you publish your PR.

## 🔁 Changing the timing of execution

Currently, the `日別統計` are set to post to the LINE every day at 00:00 and the `現在の感染者数` is set to post to the LINE every hour at 00:00.\
If you want to change them, modify lines 35-38 of `src/main.py` using the schedule library.\

Example:

```py
# Update the `現在の感染者数` every hour from 06:00 to 21:00.
for hour in range(6, 21):
    schedule.every().day.at(f'{hour:02d}:00').do(now_total, line_token=line_token, save_dir=save_dir)

# Update the `日別統計` to 06:00.
schedule.every().day.at('06:00').do(today_total, line_token=line_token, save_dir=save_dir)
```

The WebAPI is updated every two hours, so even if you run it every hour, it will actually post every two hours.

## ⚖️ LICENSE

[MIT LICENSE](../LICENSE)
