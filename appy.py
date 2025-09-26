import streamlit as st
import json
import os

LEDGER_FILE = "ledger.json"

# --- Helper functions ---
def load_ledger():
    if not os.path.exists(LEDGER_FILE):
        # Create default ledger if file doesn't exist
        ledger = {
            "students": {
                "Alice": 0,
                "Bob": 0,
                "Charlie": 0
            },
            "transactions": []
        }
        save_ledger(ledger)
        return ledger
    else:
        with open(LEDGER_FILE, "r") as f:
            return json.load(f)

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def award_coin(student):
    ledger = load_ledger()
    if student in ledger["students"]:
        ledger["students"][student] += 1
        ledger["transactions"].append({"type": "award", "student": student})
        save_ledger(ledger)

def transfer_coin(sender, receiver, amount):
    ledger = load_ledger()
    if ledger["students"][sender] >= amount:
        ledger["students"][sender] -= amount
        ledger["students"][receiver] += amount
        ledger["transactions"].append({
            "type": "transfer",
            "from": sender,
            "to": receiver,
            "amount": amount
        })
        save_ledger(ledger)
        return True
    return False

# --- Streamlit UI ---
st.title("🎓 EduCoin Classroom Cryptocurrency")

ledger = load_ledger()
students = list(ledger["students"].keys())

# Teacher Section
st.header("👩‍🏫 Teacher: Award Coins")
teacher_student = st.selectbox("Select student to award a coin:", students)
if st.button("Award 1 Coin"):
    award_coin(teacher_student)
    st.success(f"1 coin awarded to {teacher_student}")

# Student Section
st.header("🧑‍🎓 Student: Transfer Coins")
sender = st.selectbox("Sender", students, index=0)
receiver = st.selectbox("Receiver", [s for s in students if s != sender])
amount = st.number_input("Amount", min_value=1, step=1)
if st.button("Transfer Coins"):
    if transfer_coin(sender, receiver, amount):
        st.success(f"{amount} coin(s) transferred from {sender} to {receiver}")
    else:
        st.error(f"{sender} does not have enough coins!")

# Leaderboard
st.header("🏆 Leaderboard")
sorted_students = sorted(ledger["students"].items(), key=lambda x: x[1], reverse=True)
for student, balance in sorted_students:
    st.write(f"{student}: {balance} coin(s)")

# Show all transactions
st.header("📜 Transaction History")
for txn in ledger["transactions"]:
    if txn["type"] == "award":
        st.write(f"Awarded 1 coin to {txn['student']}")
    else:
        st.write(f"{txn['amount']} coin(s) transferred from {txn['from']} to {txn['to']}")
