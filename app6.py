import streamlit as st
import pandas as pd
import random

# Excelファイルを読み込む
df = pd.read_excel("quiz.xlsx")

# 変換テーブルの作成
zenkaku_to_hankaku_table = str.maketrans(
    '１２３４５６７８９０ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ',
    '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
)
zenkaku_symbols = '　。、・「」'
hankaku_symbols = ' .,\'\''
symbol_translation_table = str.maketrans(zenkaku_symbols, hankaku_symbols)

# ページ設定
st.title("クイズアプリ")

# セッションステートの初期化
if 'df' not in st.session_state:
    st.session_state.df = df
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = pd.DataFrame()

# 全角・半角・大文字・小文字を区別しない文字列処理
def process_string(s):
    if pd.isna(s):
        return ""
    s_str = str(s)
    processed = s_str.lower().translate(zenkaku_to_hankaku_table).translate(symbol_translation_table).strip()
    return processed

# 大分類と中分類のユニークな値を取得
groups_big = df["group_big"].dropna().unique()
selected_group_big = st.sidebar.selectbox("大分類を選択", [''] + list(groups_big))

groups_middle = []
if selected_group_big:
    groups_middle = df[df["group_big"] == selected_group_big]["group_middle"].dropna().unique()
    selected_group_middle = st.sidebar.selectbox("中分類を選択", [''] + list(groups_middle))
else:
    selected_group_middle = ''

# 選択に応じて問題をフィルタリング
if st.button("問題を絞り込む"):
    filtered_df = df.copy()
    if selected_group_big:
        filtered_df = filtered_df[filtered_df["group_big"] == selected_group_big]
    if selected_group_middle:
        filtered_df = filtered_df[filtered_df["group_middle"] == selected_group_middle]
    
    st.session_state.filtered_df = filtered_df.sample(frac=1).reset_index(drop=True)
    st.session_state.q_index = 0
    st.session_state.answered = False
    st.session_state.score = 0
    st.rerun()

# クイズの開始
if not st.session_state.filtered_df.empty:
    if st.session_state.q_index < len(st.session_state.filtered_df):
        q = st.session_state.filtered_df.loc[st.session_state.q_index]

        st.header(f"第{st.session_state.q_index + 1}問")
        st.write(f"スコア: {st.session_state.score} / {st.session_state.q_index}")
        st.subheader(q["question"])

        if q["type"] == "select":
            choices = [q[c] for c in ["choices1", "choices2", "choices3", "choices4"] if pd.notna(q[c])]
            selected = st.radio("選択肢を選んでください", choices, key=f"q{st.session_state.q_index}")
        else:
            selected = st.text_input("答えを入力してください", key=f"q{st.session_state.q_index}")

        if st.button("答える", key=f"answer{st.session_state.q_index}") and not st.session_state.answered:
            correct = [str(q[c]).strip() for c in ["answer1", "answer2", "answer3", "answer4"] if pd.notna(q[c])]
            
            # ユーザーの回答と正解の文字列を統一された形式に変換
            processed_selected = process_string(selected)
            processed_correct = [process_string(c) for c in correct]

            if processed_selected in processed_correct:
                st.success("正解！ 🎉 ")
                st.session_state.score += 1
            else:
                st.error(f"不正解… 正解は {', '.join(correct)}")
            
            if "参考" in q and pd.notna(q["参考"]):
                st.info(f"参考: {q['参考']}")
            st.session_state.answered = True

        if st.session_state.answered:
            if st.button("次の問題へ", key=f"next{st.session_state.q_index}"):
                st.session_state.q_index += 1
                st.session_state.answered = False
                st.rerun()
    else:
        st.header("クイズ終了！")
        st.write(f"あなたの最終スコアは **{st.session_state.score} / {len(st.session_state.filtered_df)}** です！")
        if st.button("もう一度挑戦する"):
            st.session_state.q_index = 0
            st.session_state.answered = False
            st.session_state.score = 0
            st.session_state.filtered_df = st.session_state.df.sample(frac=1).reset_index(drop=True)
            st.rerun()

else:
    st.info("左側のサイドバーで分類を選択して、「問題を絞り込む」ボタンを押してください。")