import sqlite3
from pathlib import Path
import streamlit as st

# DB作成
DB_PATH = Path("data/songs.db")
DB_PATH.parent.mkdir(exist_ok=True)

# DBとの接続
@st.cache_resource
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("""
    CREATE TABLE IF NOT EXISTS songs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    );
    """)
    return conn

def add_song(conn, title, artist):
    with conn:
        conn.execute("INSERT INTO songs(title, artist) VALUES(?,?)",
                    (title.strip(), artist.strip()))

# データ入力フォーム作成
def render_form(conn):
    # 追加フォーム
    form = st.form("add_song", clear_on_submit=True)
    title = form.text_input("曲名*", placeholder="例：キセキ")
    artist = form.text_input("アーティスト", placeholder="例：Greeeen")
    submitted = form.form_submit_button("追加")

    if submitted:
        if not title.strip():
            st.error("曲名は必須です。")
        else:
            add_song(conn, title,artist)
            st.success("追加が完了しました。")

# 登録したデータを一覧表示
def render_table(conn):
    # DBからデータを読み込み
    rows = conn.execute(
        "SELECT id, title, artist FROM songs ORDER BY id DESC"
    ).fetchall()
    st.subheader("登録済み")
    if not rows:
        st.info("登録されている曲はありません。")
    else:
        st.table([dict(r) for r in rows])

def main():
    # UIの初期設定
    st.set_page_config(page_title="Songs Manager", layout="centered")
    st.title("Songs Manager")
    conn = get_conn()

    # ページの内容
    render_form(conn)
    st.divider()
    render_table(conn)


if __name__ == "__main__":
    main()