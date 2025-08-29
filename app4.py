import streamlit as st
import pandas as pd
import random

# Excelファイルを読み込み
df = pd.read_excel("IT_passport_quiz.xlsx")

# データを整形
questions = []
for _, row in df.iterrows():
    qtype = row["type"]
    if qtype == "select":
        choices = [str(row[col]).strip() for col in ["choices1","choices2","choices3","choices4"] if pd.notna(row[col])]
    else:
        choices = []
    answers = [str(row[col]).strip() for col in ["answer1","answer2","answer3","answer4"] if pd.notna(row[col])]
    reference = str(row["参考"]).strip() if pd.notna(row["参考"]) else ""
    
    questions.append({
        "type": qtype,
        "question": row["question"],
        "choices": choices,
        "answer": answers,
        "reference": reference
    })

# セッション状態を初期化
if "score" not in st.session_state:
    st.session_state.score = 0
if "qnum" not in st.session_state:
    st.session_state.qnum = 0
if "asked" not in st.session_state:
    st.session_state.asked = random.sample(questions, min(20, len(questions)))
if "answered" not in st.session_state:
    st.session_state.answered = False

st.title("📘 ITパスポート クイズアプリ（20問ランダム出題）")

# 全問終了チェック
if st.session_state.qnum >= len(st.session_state.asked):
    st.success(f"🎉 終了！ あなたのスコアは {st.session_state.score}/{len(st.session_state.asked)} 点")
    if st.button("最初からやり直す"):
        st.session_state.score = 0
        st.session_state.qnum = 0
        st.session_state.asked = random.sample(questions, min(20, len(questions)))
        st.session_state.answered = False
    st.stop()

# 現在の問題を取得
current = st.session_state.asked[st.session_state.qnum]
st.subheader(f"Q{st.session_state.qnum+1}: {current['question']}")

# 選択 or 記述
if current["type"] == "select":
    selected = []
    for choice in current["choices"]:
        if st.checkbox(choice, key=f"{st.session_state.qnum}_{choice}"):
            selected.append(choice)
else:
    user_input = st.text_input("答えを入力してください", key=f"input_{st.session_state.qnum}")
    selected = [user_input] if user_input else []

# 答えるボタン
if not st.session_state.answered:
    if st.button("答える"):
        correct = set(current["answer"])
        if current["type"] == "input":
            # 入力式は「どれか1つ正解すればOK」
            if any(ans in selected for ans in correct):
                st.success("🎉 正解！")
                st.session_state.score += 1
            else:
                st.error(f"❌ 不正解… 正解は {', '.join(correct)}")
        else:
            # select形式は完全一致のみ正解
            if set(selected) == correct:
                st.success("🎉 正解！")
                st.session_state.score += 1
            else:
                st.error(f"❌ 不正解… 正解は {', '.join(correct)}")

        if current["reference"]:
            st.info(f"参考: {current['reference']}")
        
        st.session_state.answered = True

# 次の問題へ
if st.session_state.answered:
    if st.button("次の問題へ"):
        st.session_state.qnum += 1
        st.session_state.answered = False
        st.rerun()
