"""
Gmail Routine - 未読メールのチェックと一覧表示
環境変数で認証情報を管理します。.env.example を参照してください。
"""

import os
import base64
import json
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

GMAIL_CLIENT_ID = os.environ["GMAIL_CLIENT_ID"]
GMAIL_CLIENT_SECRET = os.environ["GMAIL_CLIENT_SECRET"]
GMAIL_REFRESH_TOKEN = os.environ["GMAIL_REFRESH_TOKEN"]
GMAIL_USER_EMAIL = os.environ.get("GMAIL_USER_EMAIL", "me")

TOKEN_URL = "https://oauth2.googleapis.com/token"
GMAIL_API_BASE = "https://gmail.googleapis.com/gmail/v1"


def get_access_token() -> str:
    resp = requests.post(TOKEN_URL, data={
        "client_id": GMAIL_CLIENT_ID,
        "client_secret": GMAIL_CLIENT_SECRET,
        "refresh_token": GMAIL_REFRESH_TOKEN,
        "grant_type": "refresh_token",
    })
    resp.raise_for_status()
    return resp.json()["access_token"]


def list_unread_messages(access_token: str, max_results: int = 10) -> list[dict]:
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": "is:unread", "maxResults": max_results, "userId": GMAIL_USER_EMAIL}
    resp = requests.get(
        f"{GMAIL_API_BASE}/users/{GMAIL_USER_EMAIL}/messages",
        headers=headers, params=params,
    )
    resp.raise_for_status()
    return resp.json().get("messages", [])


def get_message_summary(access_token: str, message_id: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(
        f"{GMAIL_API_BASE}/users/{GMAIL_USER_EMAIL}/messages/{message_id}",
        headers=headers,
        params={"format": "metadata", "metadataHeaders": ["Subject", "From", "Date"]},
    )
    resp.raise_for_status()
    data = resp.json()
    headers_list = data.get("payload", {}).get("headers", [])
    header_map = {h["name"]: h["value"] for h in headers_list}
    return {
        "id": message_id,
        "subject": header_map.get("Subject", "(件名なし)"),
        "from": header_map.get("From", ""),
        "date": header_map.get("Date", ""),
        "snippet": data.get("snippet", ""),
    }


def run():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Gmailチェック開始")
    access_token = get_access_token()
    messages = list_unread_messages(access_token)
    if not messages:
        print("未読メールはありません。")
        return
    print(f"未読メール: {len(messages)} 件\n")
    for msg in messages:
        summary = get_message_summary(access_token, msg["id"])
        print(f"From   : {summary['from']}")
        print(f"Subject: {summary['subject']}")
        print(f"Date   : {summary['date']}")
        print(f"Snippet: {summary['snippet'][:80]}...")
        print("-" * 60)

if __name__ == "__main__":
    run()
