import tkinter as tk
import random
import pandas as pd

# Excelから問題を読み込み
df = pd.read_excel("C:/Users/owara/OneDrive/デスクトップ/ITパスポート/ITパスポート問題集.xlsx")

# 問題データを整形
questions = []
for _, row in df.iterrows():
    qtype = row["type"]
    if qtype == "select":
        choices = [str(row[col]).strip() for col in ["choices1", "choices2", "choices3", "choices4"] if pd.notna(row[col])]
    else:
        choices = []
    answers = [str(row[col]).strip() for col in ["answer1", "answer2", "answer3", "answer4"] if pd.notna(row[col])]

    questions.append({
        "type": qtype,
        "question": row["question"],
        "choices": choices,
        "answer": answers
    })


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ITパスポートクイズ")

        self.question_label = tk.Label(root, text="", font=("Arial", 16), wraplength=400, justify="left")
        self.question_label.pack(pady=20)

        self.choice_frame = tk.Frame(root)
        self.choice_frame.pack()

        self.vars = []
        self.entry = None

        self.check_button = tk.Button(root, text="答える", font=("Arial", 14), command=self.check_answer)
        self.check_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

        self.next_button = tk.Button(root, text="次の問題", font=("Arial", 14), command=self.next_question)
        self.next_button.pack(pady=10)

        self.next_question()

    def next_question(self):
        # 前の選択肢や入力欄を削除
        for widget in self.choice_frame.winfo_children():
            widget.destroy()
        self.vars = []
        self.entry = None

        # ランダムに問題を選ぶ
        self.current_question = random.choice(questions)
        self.question_label.config(text=self.current_question["question"])

        # 選択式
        if self.current_question["type"] == "select":
            shuffled_choices = random.sample(self.current_question["choices"], len(self.current_question["choices"]))
            for choice in shuffled_choices:
                var = tk.BooleanVar()
                chk = tk.Checkbutton(self.choice_frame, text=choice, variable=var, font=("Arial", 14), anchor="w")
                chk.pack(fill="x", padx=20, pady=2)
                self.vars.append((var, choice))
        else:  # 入力式
            self.entry = tk.Entry(self.choice_frame, font=("Arial", 14))
            self.entry.pack(padx=20, pady=5)

        self.result_label.config(text="")

    def check_answer(self):
        if self.current_question["type"] == "select":
            # 選択肢問題 → 全部一致で正解
            selected = [choice for var, choice in self.vars if var.get()]
            correct = set(self.current_question["answer"])
            if set(selected) == correct:
                self.result_label.config(text="正解！ 🎉", fg="green")
            else:
                self.result_label.config(text=f"不正解… 正解は {', '.join(correct)}", fg="red")

        else:  # 入力問題 → 複数回答候補のどれか一致で正解
            user_answer = self.entry.get().strip()
            correct_answers = [ans.strip() for ans in self.current_question["answer"]]
            if user_answer in correct_answers:
                self.result_label.config(text="正解！ 🎉", fg="green")
            else:
                self.result_label.config(text=f"不正解… 正解は {', '.join(correct_answers)}", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
