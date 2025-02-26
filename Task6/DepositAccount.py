import Account

class DepositAccount(Account.Account):
    interest_rate = 4.5
    def __init__(self,accountno,name,balance):
        super().__init__(accountno,name,balance)
        self.interest_rate  = DepositAccount.interest_rate
    
    def withdraw(self, amount):
        print("you can not withdraw fom your deposit account")