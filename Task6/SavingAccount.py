import Account
class SavingAccount(Account.Account):
    interest_rate = 3
    def __init__(self, accountno, name, balance):
        super().__init__(accountno, name, balance)
        self.interest_rate = SavingAccount.interest_rate
    