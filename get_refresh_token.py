"""
Gmail リフレッシュトークン取得スクリプト（初回セットアップ時のみ使用）
"""

import os, webbrowser
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ["GMAIL_CLIENT_ID"]
CLIENT_SECRET = os.environ["GMAIL_CLIENT_SECRET"]
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
SCOPE = "https://www.googleapis.com/auth/gmail.readonly"

def main():
    params = {
        "client_id": CLIENT_ID, "redirect_uri": REDIRECT_URI,
        "response_type": "code", "scope": SCOPE,
        "access_type": "offline", "prompt": "consent",
    }
    url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"
    print(f"\n{url}\n")
    webbrowser.open(url)
    code = input("認証コードを貼り付けてください: ").strip()
    resp = requests.post("https://oauth2.googleapis.com/token", data={
        "code": code, "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI, "grant_type": "authorization_code",
    })
    resp.raise_for_status()
    token = resp.json().get("refresh_token")
    print(f"\nGMAIL_REFRESH_TOKEN={token}")

if __name__ == "__main__":
    main()
