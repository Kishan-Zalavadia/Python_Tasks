class Account:
    
    balance : int = 0

    def __init__(self,accountno,name,balance):
        self.__account_no = accountno
        self.__name = name
        self.__balance = balance

    def deposit(self,amount):
        if(amount>0):
            self.__balance += amount
            print(f"{amount} Rs Deposite in your account & your new balance {self.__balance}")
        else:
            print("enter valid amount")

    def withdraw(self,amount):
        if(amount<self.__balance):
            self.__balance -= amount
            print(f"{amount} Rs Credited in your account & your new balance {self.__balance}")
        else:
            print("enter valid amount")

    def add_interest(self):
        interest = self.__balance * self.interest_rate / 100
        self.__balance += interest
        print(f"your interest is {interest} and new Balance is {self.__balance}")

    def get_account_no(self):
        return self.__account_no

    def get_balance(self):
        return self.__balance
    
    def get_Accountdetails(self):
        print(f"Account no = {self.__account_no} Account holder Name  = {self.__name} and  Balnce = {self.__balance}")
    