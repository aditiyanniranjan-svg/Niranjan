import json
import os
from datetime import datetime

DATA_FILE = "bank_data.json"


class BankingSystem:
    def __init__(self):
        self.accounts = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                self.accounts = json.load(file)

    def save_data(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.accounts, file, indent=4)

    def create_account(self):
        print("\n--- Create Account ---")
        account_no = input("Enter account number: ")

        if account_no in self.accounts:
            print("Account already exists!")
            return

        name = input("Enter account holder name: ")
        pin = input("Create 4-digit PIN: ")

        if len(pin) != 4 or not pin.isdigit():
            print("Invalid PIN. PIN must contain 4 digits.")
            return

        self.accounts[account_no] = {
            "name": name,
            "pin": pin,
            "balance": 0.0,
            "transactions": []
        }

        self.save_data()
        print("Account created successfully!")

    def login(self):
        print("\n--- Login ---")
        account_no = input("Account number: ")
        pin = input("PIN: ")

        if account_no in self.accounts and self.accounts[account_no]["pin"] == pin:
            print(f"\nWelcome, {self.accounts[account_no]['name']}!")
            return account_no

        print("Invalid account number or PIN.")
        return None

    def deposit(self, account_no):
        try:
            amount = float(input("Enter deposit amount: "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                return

            self.accounts[account_no]["balance"] += amount

            self.accounts[account_no]["transactions"].append({
                "type": "Deposit",
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            self.save_data()
            print(f"₹{amount:.2f} deposited successfully.")

        except ValueError:
            print("Invalid amount.")

    def withdraw(self, account_no):
        try:
            amount = float(input("Enter withdrawal amount: "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                return

            if amount > self.accounts[account_no]["balance"]:
                print("Insufficient balance!")
                return

            self.accounts[account_no]["balance"] -= amount

            self.accounts[account_no]["transactions"].append({
                "type": "Withdrawal",
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            self.save_data()
            print(f"₹{amount:.2f} withdrawn successfully.")

        except ValueError:
            print("Invalid amount.")

    def check_balance(self, account_no):
        balance = self.accounts[account_no]["balance"]
        print(f"\nCurrent Balance: ₹{balance:.2f}")

    def transfer(self, account_no):
        receiver = input("Enter receiver account number: ")

        if receiver not in self.accounts:
            print("Receiver account does not exist.")
            return

        if receiver == account_no:
            print("You cannot transfer money to your own account.")
            return

        try:
            amount = float(input("Enter transfer amount: "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                return

            if amount > self.accounts[account_no]["balance"]:
                print("Insufficient balance!")
                return

            self.accounts[account_no]["balance"] -= amount
            self.accounts[receiver]["balance"] += amount

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.accounts[account_no]["transactions"].append({
                "type": "Transfer Sent",
                "amount": amount,
                "to": receiver,
                "date": date
            })

            self.accounts[receiver]["transactions"].append({
                "type": "Transfer Received",
                "amount": amount,
                "from": account_no,
                "date": date
            })

            self.save_data()
            print(f"₹{amount:.2f} transferred successfully.")

        except ValueError:
            print("Invalid amount.")

    def transaction_history(self, account_no):
        print("\n--- Transaction History ---")

        transactions = self.accounts[account_no]["transactions"]

        if not transactions:
            print("No transactions found.")
            return

        for i, transaction in enumerate(transactions, 1):
            print(f"\nTransaction {i}")
            print(f"Type   : {transaction['type']}")
            print(f"Amount : ₹{transaction['amount']:.2f}")
            print(f"Date   : {transaction['date']}")

            if "to" in transaction:
                print(f"To     : {transaction['to']}")

            if "from" in transaction:
                print(f"From   : {transaction['from']}")

    def account_menu(self, account_no):
        while True:
            print("\n========== BANK MENU ==========")
            print("1. Deposit Money")
            print("2. Withdraw Money")
            print("3. Check Balance")
            print("4. Transfer Money")
            print("5. Transaction History")
            print("6. Logout")
            print("================================")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.deposit(account_no)

            elif choice == "2":
                self.withdraw(account_no)

            elif choice == "3":
                self.check_balance(account_no)

            elif choice == "4":
                self.transfer(account_no)

            elif choice == "5":
                self.transaction_history(account_no)

            elif choice == "6":
                print("Logged out successfully.")
                break

            else:
                print("Invalid choice!")


def main():
    bank = BankingSystem()

    while True:
        print("\n")
        print("================================")
        print("       PYTHON BANKING SYSTEM")
        print("================================")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        print("================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            bank.create_account()

        elif choice == "2":
            account_no = bank.login()

            if account_no:
                bank.account_menu(account_no)

        elif choice == "3":
            print("Thank you for using the Banking System!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()