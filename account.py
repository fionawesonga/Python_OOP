# Add the following methods to the Account class
# Deposit: method to deposit funds, store the deposit and return a message with the new balance to the customer. It should only accept positive amounts.
# Withdraw: method to withdraw funds, store the withdrawal and return a message with the new balance to the customer. An account cannot be overdrawn.
# Transfer Funds: Method to transfer funds from one account to an instance of another account.
# Get Balance: Method to calculate an account balance from deposits and withdrawals.
# Request Loan: Method to request a loan amount.
# Repay Loan: Method to repay a loan with a given amount.
# View Account Details: Method to display the account owner's details and current balance.
# Change Account Owner: Method to update the account owner's name.
# Account Statement: Method to generate a statement of all transactions in an account. (Print using a for loop).
# Interest Calculation: Method to calculate and apply an interest to the balance. Use 5% interest. 
# Freeze/Unfreeze Account: Methods to freeze and unfreeze the account for security reasons.
# Set Minimum Balance: Method to enforce a minimum balance requirement. You cannot withdraw if your balance is less than this amount.Close Account: Method to close the account and set all balances to zero and empty all transactions.

# Create a new class Transaction to store all transactions with attributes for date and time, narration, amount, transaction type etc.

# The Account class should have a new attribute called transactions which will store every transaction that happens in the account

# Each transaction should be stored as an instance of the Transaction

# The get balance method should use the transactions list to compute the current balance

# Add encapsulation to the Account class to have sensitive attributes like balance and account number only accessible via given class methods. 

from datetime import datetime

class Transaction:
    def __init__(self, narration, amount, transaction_type):
        self.date_time = datetime.now()
        self.narration = narration
        self.amount = amount
        self.transaction_type = transaction_type  

    def __str__(self):
        return f"{self.date_time} | {self.transaction_type.title()} | {self.narration} | Amount: {self.amount}"


class Account:
    account_counter = 1 

    def __init__(self, owner, minimum_balance=0):
        self.owner = owner
        self.__balance = 0
        self.__account_number = f"AC{Account.account_counter}"
        Account.account_counter += 1
        self.minimum_balance = minimum_balance
        self.loan = 0
        self.frozen = False
        self.closed = False
        self.transactions = []

    def deposit(self, amount):
        if self.closed or self.frozen:
            return "Inactive Account."
        if amount <= 0:
            return "Amount to deposit must be positive."
        self.__balance += amount
        self.transactions.append(Transaction("Deposit", amount, "deposit"))
        return f"Deposited {amount}. New balance is {self.__balance}."

    def withdraw(self, amount):
        if self.closed or self.frozen:
            return "Inactive Account."
        if amount <= 0:
            return "Amount to be withdrawn must be positive."
        if self.__balance - amount < self.minimum_balance:
            return f"Cannot withdraw. A minimum balance of {self.minimum_balance} must be maintained."
        self.__balance -= amount
        self.transactions.append(Transaction("Withdrawal", amount, "withdrawal"))
        return f"Withdrew {amount}. New balance is {self.__balance}."

    def transfer_funds(self, amount, recipient_account):
        if self.closed or self.frozen:
            return "Inactive Account."
        if not isinstance(recipient_account, Account):
            return "Invalid recipient."
        withdraw_result = self.withdraw(amount)
        if "Withdrew" in withdraw_result:
            recipient_account.deposit(amount)
            self.transactions.append(Transaction(f"Transfer to {recipient_account.owner}", amount, "transfer"))
            return f"Transferred {amount} to {recipient_account.owner}."
        return withdraw_result

    def get_balance(self):
        balance = 0
        for transaction in self.transactions:
            if transaction.transaction_type in ["deposit", "loan"]:
                balance += transaction.amount
            elif transaction.transaction_type in ["withdrawal", "repayment", "transfer"]:
                balance -= transaction.amount
            elif transaction.transaction_type == "interest":
                balance += transaction.amount
        self.__balance = balance
        return self.__balance

    def request_loan(self, amount):
        if self.closed or self.frozen:
            return "Inactive Account."
        if amount <= 0:
            return "Amount to be borrowed must be positive."
        self.loan += amount
        self.__balance += amount
        self.transactions.append(Transaction("Loan approved", amount, "loan"))
        return f"You have been offered a loan of {amount}. Your new balance is {self.__balance}."

    def repay_loan(self, amount):
        if self.closed or self.frozen:
            return "Inactive Account."
        if amount <= 0:
            return "Amount to be repaid must be positive."
        if self.loan == 0:
            return "You have no loan to repay."
        if amount > self.__balance:
            return "Your balance is not enough to repay the loan."
        payment = min(amount, self.loan)
        self.loan -= payment
        self.__balance -= payment
        self.transactions.append(Transaction("Loan repayment", payment, "repayment"))
        return f"Repaid {payment} of loan. Remaining loan: {self.loan}. New balance: {self.__balance}."

    def view_account_details(self):
        return f"Owner: {self.owner}, Balance: {self.__balance}, Loan: {self.loan}, Account Number: {self.__account_number}"

    def change_account_owner(self, new_owner):
        if self.closed:
            return "Account is closed."
        self.owner = new_owner
        return f"Account owner changed to {new_owner}."

    def account_statement(self):
        if self.closed:
            return "Account is closed."
        print("Account Statement:")
        for transaction in self.transactions:
            print(transaction)

    def apply_interest(self):
        if self.closed or self.frozen:
            return "Inactive Account."
        interest = self.__balance * 0.05
        self.__balance += interest
        self.transactions.append(Transaction("Interest applied", interest, "interest"))
        return f"Interest of {interest} applied. New balance is {self.__balance}."

    def freeze_account(self):
        self.frozen = True
        return "Your account has been frozen."

    def unfreeze_account(self):
        self.frozen = False
        return "Your account has been unfrozen."

    def set_minimum_balance(self, amount):
        if amount < 0:
            return "The minimum balance cannot be negative."
        self.minimum_balance = amount
        return f"Minimum balance is now {amount}."

    def close_account(self):
        self.closed = True
        self.__balance = 0
        self.loan = 0
        self.transactions.clear()
        return "Your account has been closed."

    def get_account_number(self):
        return self.__account_number

    def get_raw_balance(self):
        return self.__balance


acc1 = Account("Fiona", minimum_balance=100)
acc2 = Account("Jabal")
print(acc1.deposit(6000))
print(acc1.request_loan(8000))
print(acc1.apply_interest())