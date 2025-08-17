import streamlit as st
import pandas as pd
import random
import os

# Excelファイルは app.py と同じフォルダに置く
EXCEL_FILE = "IT_passport_quiz.xlsx"
file_path = os.path.join(os.path.dirname(__file__), EXCEL_FILE)

# Excelから問題を読み込み
df = pd.read_excel(file_path)

# データ整形
questions = []
for _, row in df.iterrows():
    qtype = row["type"]
    if qtype == "select":
        choices = [str(row[col]).strip() for col in ["choices1","choices2","choices3","choices4"] if pd.notna(row[col])]
    else:
        choices = []
    answers = [str(row[col]).strip() for col in ["answer1","answer2","answer3","answer4"] if pd.notna(row[col])]
    reference = str(row["参考"]) if "参考" in row else ""
    
    questions.append({
        "type": qtype,
        "question": row["question"],
        "choices": choices,
        "answer": answers,
        "reference": reference
    })

st.title("📘 ITパスポート クイズアプリ")

# セッションで状態管理
if "score" not in st.session_state:
    st.session_state.score = 0
if "qnum" not in st.session_state:
    st.session_state.qnum = 0
if "asked" not in st.session_state:
    st.session_state.asked = random.sample(questions, min(20, len(questions)))
if "answered" not in st.session_state:
    st.session_state.answered = False  # 回答済みかどうか
if "finished" not in st.session_state:
    st.session_state.finished = False  # 全問終了したかどうか

# --- 全問終了後リスタート ---
if st.session_state.finished:
    if st.button("もう一度挑戦する"):
        st.session_state.score = 0
        st.session_state.qnum = 0
        st.session_state.asked = random.sample(questions, min(20, len(questions)))
        st.session_state.answered = False
        st.session_state.finished = False
    else:
        st.stop()  # 全問終了時は他の要素を表示しない

# 現在の問題
current = st.session_state.asked[st.session_state.qnum]
st.subheader(f"Q{st.session_state.qnum+1}: {current['question']}")

# 選択式 or 記述式
if current["type"] == "select":
    # 選択肢のマルチセレクトでは表示の×が重なる問題を避けるため
    selected = st.multiselect("選択してください", current["choices"], default=[])
else:
    selected = [st.text_input("答えを入力してください", value="")]

# 答えチェック
if st.button("答える") and not st.session_state.answered:
    correct = set(current["answer"])
    # 回答判定
    if set(selected) == correct:
        st.success("🎉 正解！")
        st.session_state.score += 1
    else:
        st.error(f"❌ 不正解… 正解は {', '.join(correct)}")
    
    # 参考情報表示
    if current["reference"]:
        st.info(f"💡 参考: {current['reference']}")

    st.session_state.answered = True  # 回答済み

# 次の問題へボタン
if st.session_state.answered:
    if st.button("次の問題へ"):
        if st.session_state.qnum + 1 < len(st.session_state.asked):
            st.session_state.qnum += 1
            st.session_state.answered = False
        else:
            st.session_state.finished = True
            st.info(f"終了！あなたのスコアは {st.session_state.score}/{len(st.session_state.asked)} 点")
