import streamlit as st
import pandas as pd
import random

# Excelから問題を読み込み
df = pd.read_excel("ITパスポート問題集.xlsx")

# データ整形
questions = []
for _, row in df.iterrows():
    qtype = row["type"]
    if qtype == "select":
        choices = [str(row[col]).strip() for col in ["choices1","choices2","choices3","choices4"] if pd.notna(row[col])]
    else:
        choices = []
    answers = [str(row[col]).strip() for col in ["answer1","answer2","answer3","answer4"] if pd.notna(row[col])]
    
    questions.append({
        "type": qtype,
        "question": row["question"],
        "choices": choices,
        "answer": answers
    })

st.title("📘 ITパスポート クイズアプリ")

# セッションで状態管理
if "score" not in st.session_state:
    st.session_state.score = 0
if "qnum" not in st.session_state:
    st.session_state.qnum = 0
if "asked" not in st.session_state:
    st.session_state.asked = random.sample(questions, len(questions))

# 現在の問題
current = st.session_state.asked[st.session_state.qnum]
st.subheader(f"Q{st.session_state.qnum+1}: {current['question']}")

# 選択式 or 記述式
if current["type"] == "select":
    selected = st.multiselect("選択してください", current["choices"])
else:
    selected = [st.text_input("答えを入力してください")]

# 答えチェック
if st.button("答える"):
    correct = set(current["answer"])
    if set(selected) == correct:
        st.success("🎉 正解！")
        st.session_state.score += 1
    else:
        st.error(f"❌ 不正解… 正解は {', '.join(correct)}")

    # 次の問題へ
    if st.session_state.qnum + 1 < len(st.session_state.asked):
        st.session_state.qnum += 1
    else:

        st.info(f"終了！あなたのスコアは {st.session_state.score}/{len(questions)} 点")
