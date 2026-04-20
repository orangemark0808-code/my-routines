# my-routines

Gmail未読メールチェックなどの自動化ルーチン集です。

## セットアップ

1. `.env.example` をコピーして `.env` を作成
2. Google Cloud ConsoleでOAuth認証情報を取得
3. `get_refresh_token.py` を実行してリフレッシュトークンを取得
4. `.env` に各値を設定

## 実行

```bash
pip install -r requirements.txt
python check_gmail.py
```
