import streamlit as st
import pandas as pd
import random

# Excel読み込み
df = pd.read_excel("IT_passport_quiz.xlsx")

# --- サイドバーで大分類・中分類を選択 ---
groups_big = df["group_big"].dropna().unique()
selected_big = st.sidebar.selectbox("大分類を選んでください", groups_big)

groups_small = df[df["group_big"] == selected_big]["group_small"].dropna().unique()
selected_small = st.sidebar.selectbox("中分類を選んでください", groups_small)

# --- フィルタリング ---
df = df[(df["group_big"] == selected_big) & (df["group_small"] == selected_small)]

# --- 初回のみ問題をシャッフル＆10問抽出 ---
if "questions" not in st.session_state or st.session_state.get("selected_big") != selected_big or st.session_state.get("selected_small") != selected_small:
    st.session_state.questions = random.sample(df.to_dict(orient="records"), min(10, len(df)))
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected_big = selected_big
    st.session_state.selected_small = selected_small

questions = st.session_state.questions

# --- 出題 ---
if st.session_state.q_index < len(questions):
    q = questions[st.session_state.q_index]
    st.write(f"**Q{st.session_state.q_index+1}: {q['question']}**")

    if q["type"] == "select":
        choices = [q[c] for c in ["choices1","choices2","choices3","choices4"] if pd.notna(q[c])]
        selected = st.radio("選択肢を選んでください", choices, key=f"q{st.session_state.q_index}")
    else:
        selected = st.text_input("答えを入力してください", key=f"q{st.session_state.q_index}")

    # 答えるボタン
    if st.button("答える", key=f"answer{st.session_state.q_index}") and not st.session_state.answered:
        correct = [str(q[c]).strip() for c in ["answer1","answer2","answer3","answer4"] if pd.notna(q[c])]
        if str(selected).strip() in correct:
            st.success("正解！ 🎉")
            st.session_state.score += 1
        else:
            st.error(f"不正解… 正解は {', '.join(correct)}")
        if "参考" in q and pd.notna(q["参考"]):
            st.info(f"参考: {q['参考']}")
        st.session_state.answered = True

    # 次の問題へ
    if st.session_state.answered:
        if st.button("次の問題へ", key=f"next{st.session_state.q_index}"):
            st.session_state.q_index += 1
            st.session_state.answered = False
            st.rerun()

else:
    st.success(f"終了！あなたの得点は {st.session_state.score}/{len(questions)} 点です。")
    if st.button("最初から挑戦する"):
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.answered = False
        del st.session_state.questions
        st.rerun()

