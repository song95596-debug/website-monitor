import requests
import hashlib
import os
from datetime import datetime

MONITOR_URL = "https://cie.huanghuai.edu.cn/index.htm"
RECORD_FILE = "record.md"
HASH_FILE = ".last_hash.txt"


def get_page_hash(url):
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        content = resp.text
        h = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return h
    except Exception as e:
        print(f"抓取出错: {e}")
        return None


def read_last_hash():
    try:
        with open(HASH_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def save_hash(h):
    with open(HASH_FILE, "w", encoding="utf-8") as f:
        f.write(h)


def append_log(text):
    with open(RECORD_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    now = datetime.now().strftime("%Y‑%m‑%d %H:%M:%S")
    current_hash = get_page_hash(MONITOR_URL)
    changed = False

    if current_hash is None:
        changed = False
    else:
        old_hash = read_last_hash()
        if old_hash is None:
            append_log(f"\n- [{now}] ✅首次采集，保存初始页面指纹")
            changed = True
        else:
            if old_hash != current_hash:
                append_log(f"\n- [{now}] 🔔检测到网页发生更新！ url:{MONITOR_URL}")
                changed = True
        save_hash(current_hash)

    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"changed={'true' if changed else 'false'}\n")
