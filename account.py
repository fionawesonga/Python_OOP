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
class Account:
    def __init__(self, owner, minimum_balance=0):
        self.owner = owner
        self.deposits = []
        self.withdrawals = []
        self.loan = 0
        self.balance = 0
        self.frozen = False
        self.minimum_balance = minimum_balance
        self.closed = False
        self.transactions = []
    def deposit(self, amount):
        if self.closed or self.frozen:
            return "Inactive Account."
        if amount <= 0:
            return "Amount to deposit must be positive."
        self.deposits.append(amount)
        self.transactions.append(f"Deposited: {amount}")
        self.balance += amount
        return f"Deposited {amount}. New balance is {self.balance}."
    def withdraw(self, amount):
        if self.closed or self.frozen:
            return "Inactive Account."
        if amount <= 0:
            return "Amount to be withdrawn must be positive."
        if self.balance - amount < self.minimum_balance:
            return f"Cannot withdraw. Minimum balance of {self.minimum_balance} must be maintained."
        self.withdrawals.append(amount)
        self.transactions.append(f"Withdrew: {amount}")
        self.balance -= amount
        return f"Withdrew {amount}. New balance is {self.balance}."
    def transfer_funds(self, amount, recipient_account):
        if self.closed or self.frozen:
            return "Inactive Account."
        if not isinstance(recipient_account, Account):
            return "Invalid recipient."
        withdraw_result = self.withdraw(amount)
        if "Withdrew" in withdraw_result:
            recipient_account.deposit(amount)
            self.transactions.append(f"Transferred {amount} to {recipient_account.owner}")
            return f"Transferred {amount} to {recipient_account.owner}."
        return withdraw_result
    def get_balance(self):
        return self.balance
    def request_loan(self, amount):
        if self.closed or self.frozen:
            return "Inactive Account."
        if amount <= 0:
            return "Amount to be borrowed must  be positive."
        self.loan += amount
        self.balance += amount
        self.transactions.append(f"Loan requested and approved: {amount}")
        return f"A loan of {amount} has been  approved. The new balance is {self.balance}."
    def repay_loan(self, amount):
        if self.closed or self.frozen:
            return "Inactive Account."
        if amount <= 0:
            return "Amount to be repayed must be positive."
        if amount > self.balance:
            return "Your balance is  not enough to repay the loan."
        if self.loan == 0:
            return "You have no loan to repay."
        payment = min(amount, self.loan)
        self.loan -= payment
        self.balance -= payment
        self.transactions.append(f"Loan repaid is: {payment}")
        return f"Repaid {payment} of loan. Remaining loan: {self.loan}. New balance: {self.balance}."
    def view_account_details(self):
        return f"Owner: {self.owner}, Balance: {self.balance}, Loan: {self.loan}"
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
        interest = self.balance * 0.05
        self.balance += interest
        self.transactions.append(f"Interest applied: {interest}")
        return f"Interest of {interest} applied. New balance is {self.balance}."
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
        return f"Minimum balance is {amount}."
    def close_account(self):
        self.closed = True
        self.balance = 0
        self.loan = 0
        self.transactions.clear()
        self.deposits.clear()
        self.withdrawals.clear()
        return "Your Account has been closed."