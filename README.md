# COVID-19-notice

![python](https://img.shields.io/github/pipenv/locked/python-version/yuto51942/COVID-19-notice)
![last_commit](https://img.shields.io/github/last-commit/yuto51942/COVID-19-notice)

🇯🇵| [🇺🇸](doc/README_en.md)

![title](doc/title.png)

## TL;DR

毎日の日本のCOVID-19情報まとめをLINEに送信する。

## 🔍 データ取得先

[covid19-japan-web-api](https://github.com/ryo-ma/covid19-japan-web-api)

## 💻 環境

- python3.6

## ⚙ 依存関係のインストール

pipenvからインストール

```bash
pip install pipenv

# pipenvの仮想環境上にインストール
pipenv install

# PC上にインストール
pipenv install --system --deploy
```

## LINE notifyの取得

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

## ⚖️ LICENSE

[MIT LICENSE](LICENSE)
