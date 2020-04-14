# 🦠 COVID-19 to LINE

![python](https://img.shields.io/github/pipenv/locked/python-version/yuto51942/COVID-19-notice)
![last_commit](https://img.shields.io/github/last-commit/yuto51942/COVID-19-notice)

🇯🇵| [🇺🇸](doc/README_en.md)

![title](doc/title.png)

## TL;DR

- 00:00に前日のCOVID-19の感染者の情報をLINE notifyに送信する。
- 国内の感染者数合計を1時間おきにWebAPIにアクセスし、更新された場合LINE notifyに送信する。

## 🔍 データ取得先

[covid19-japan-web-api](https://github.com/ryo-ma/covid19-japan-web-api)

## ⚠️ 注意事項

取得しているデータは有志が収集しているものです。\
正確なデータは厚生労働省などの公的機関をご確認ください。

## 💻 環境

- MacOS
- Ubuntu 18.04

Windowsは動作未確認です。

## ⚙ 依存関係のインストール

pipenvからインストール

```bash
pip install pipenv

# pipenvの仮想環境上にインストール
pipenv install

# PC上にインストール
pipenv install --system --deploy
```

## 🔐 LINE notifyの取得

[\[超簡単\]LINE notify を使ってみる](https://qiita.com/iitenkida7/items/576a8226ba6584864d95)

上記の記事を参考にトークンを取得します。

## 🚀 実行

LINE Tokenを取得済みとする。

```bash
# 実行
python src/main.py

# サーバー(Ubuntu)などで
nohup python3 src/main.py --line-token [token] &
```

## ✅ 静的解析

- Pylint
- mypy
- flake8

```bash
pipenv install --dev
pipenv shell
sh ./analysis.sh
```

PRを出す際にはすべてのツールのチェックを成功させてください。

## 🔁 実行するタイミングの変更

現在、`日別統計`は毎日00:00、`現在の感染者数`は毎時00分にLINEにpostするよう設定されています。\
これらを変更する場合は、`src/main.py`の32~36行目を schedule ライブラリを使用して変更してください。\

例:

```py
# `現在の感染者数`の更新を6時から21時まで1時間毎に
for hour in range(6, 21):
    schedule.every().day.at(f'{hour:02d}:00').do(now_total, line_token=line_token, save_dir=save_dir)

# `日別統計`を6時に
schedule.every().day.at('06:00').do(today_total, line_token=line_token, save_dir=save_dir)
```

WebAPIは2時間毎に更新されるため1時間ごとに実行しても実際にpostされるのは2時間毎となります。

## ⚖️ LICENSE

[MIT LICENSE](LICENSE)
