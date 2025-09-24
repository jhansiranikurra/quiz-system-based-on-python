import time

# Data storage in memory only
questions = {}
user_scores = {}   # {username: [ {score, tech, time}, ... ]}
user_info = {}     # {username: mobile}

# Admin credentials
admin_id = "abc@123"
admin_password = "abc@123"


# ---------------- Main Menu ----------------
def start():
    while True:
        print("\n--- Quiz System ---")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Exit")
        choice = input("Choose option: ")
        if choice == "1":
            admin_login()
        elif choice == "2":
            user_login()
        elif choice == "3":
            print("Thank you!")
            break
        else:
            print("Invalid choice.")


# ---------------- Admin ----------------
def admin_login():
    aid = input("Enter Admin ID: ")
    pwd = input("Enter Admin Password: ")
    if aid == admin_id and pwd == admin_password:
        print("Admin logged in.")
        admin_menu()
    else:
        print("Wrong credentials.")


def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Question")
        print("2. View Questions")
        print("3. Modify Question")
        print("4. Delete Question")
        print("5. View Users")
        print("6. Top 3 Scores")
        print("7. Logout")
        choice = input("Enter choice: ")
        if choice == "1":
            add_question()
        elif choice == "2":
            view_questions()
        elif choice == "3":
            modify_question()
        elif choice == "4":
            delete_question()
        elif choice == "5":
            view_users()
        elif choice == "6":
            top_scores()
        elif choice == "7":
            break
        else:
            print("Invalid choice.")


def add_question():
    qno = input("Question Number: ")
    if qno in questions:
        print("This question number already exists.")
        return
    tech = input("Technology: ")
    ques = input("Question: ")
    opt1 = input("Option A: ")
    opt2 = input("Option B: ")
    opt3 = input("Option C: ")
    opt4 = input("Option D: ")
    ans = input("Correct Answer (A/B/C/D): ").upper()
    questions[qno] = {
        "tech": tech,
        "question": ques,
        "options": [opt1, opt2, opt3, opt4],
        "answer": ans
    }
    print("Added successfully.")


def view_questions():
    if not questions:
        print("No questions.")
        return
    for qno, q in questions.items():
        print(f"\nQ{qno} ({q['tech']}): {q['question']}")
        print("A.", q["options"][0])
        print("B.", q["options"][1])
        print("C.", q["options"][2])
        print("D.", q["options"][3])
        print("Answer:", q["answer"])


def modify_question():
    qno = input("Question number to modify: ")
    if qno in questions:
        q = questions[qno]
        new_q = input(f"New question (leave blank to keep: {q['question']}): ")
        new_a = input(f"New Option A (leave blank to keep: {q['options'][0]}): ")
        new_b = input(f"New Option B (leave blank to keep: {q['options'][1]}): ")
        new_c = input(f"New Option C (leave blank to keep: {q['options'][2]}): ")
        new_d = input(f"New Option D (leave blank to keep: {q['options'][3]}): ")
        new_ans = input(f"New answer (A/B/C/D, leave blank to keep: {q['answer']}): ").upper()

        if new_q: q["question"] = new_q
        if new_a: q["options"][0] = new_a
        if new_b: q["options"][1] = new_b
        if new_c: q["options"][2] = new_c
        if new_d: q["options"][3] = new_d
        if new_ans: q["answer"] = new_ans
        print("Question updated.")
    else:
        print("Question not found.")


def delete_question():
    qno = input("Question number to delete: ")
    if qno in questions:
        del questions[qno]
        print("Deleted.")
    else:
        print("Not found.")


def view_users():
    if not user_scores:
        print("No users yet.")
        return
    for user in user_scores:
        print("\nName:", user)
        print("Mobile:", user_info.get(user, "N/A"))
        for attempt in user_scores[user]:
            print(f"   Tech: {attempt['tech']}, Score: {attempt['score']}, Time: {attempt['time']}")


def top_scores():
    if not user_scores:
        print("No scores yet.")
        return
    all_scores = []
    for user, attempts in user_scores.items():
        for attempt in attempts:
            all_scores.append((user, attempt["score"]))
    sorted_users = sorted(all_scores, key=lambda x: x[1], reverse=True)

    print("\n--- Top 3 Scores ---")
    for idx, (user, score) in enumerate(sorted_users[:3], start=1):
        print(f"{idx}. {user} - {score}")


# ---------------- User ----------------
def user_login():
    name = input("Enter your name: ")
    while True:
        mobile = input("Mobile number (start with 9/8/7/6): ")
        if mobile.isdigit() and len(mobile) == 10 and mobile[0] in ['9', '8', '7', '6']:
            user_info[name] = mobile
            print("Welcome,", name)
            take_quiz(name)
            break
        else:
            print("Invalid mobile number.")


def take_quiz(username):
    if not questions:
        print("No questions available.")
        return

    available_techs = {q["tech"] for q in questions.values()}
    print("\nAvailable Technologies:", ", ".join(available_techs))
    tech = input("Choose Technology: ")

    score = 0
    found = False
    start_time = time.time()

    for qno, q in questions.items():
        if q["tech"].lower() == tech.lower():
            found = True
            print(f"\nQ{qno}: {q['question']}")
            print("A.", q["options"][0])
            print("B.", q["options"][1])
            print("C.", q["options"][2])
            print("D.", q["options"][3])
            ans = input("Your answer (A/B/C/D or Q to quit): ").upper()
            if ans == "Q":
                print("Quiz exited.")
                return
            if ans == q["answer"]:
                score += 1

    end_time = time.time()
    if found:
        time_taken = end_time - start_time
        time_str = f"{int(time_taken // 60)} min {int(time_taken % 60)} sec"
        print(f"\nYour Score: {score}")
        print(f"Time taken: {time_str}")

        attempt = {"score": score, "tech": tech, "time": time_str}
        user_scores.setdefault(username, []).append(attempt)
    else:
        print("No questions for that technology.")


# ---------------- Start Program ----------------
start()



