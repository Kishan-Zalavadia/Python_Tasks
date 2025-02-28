import DepositAccount
import SavingAccount

def createAccount(type):
    account_no  = input("enter Account no = ")
    name = input ("enter Account holder name = ")
    balance = int(input("enter initial balance = "))
    if(type == "Deposit"):
        DepAccount  = DepositAccount.DepositAccount(account_no,name,balance)
        all_accounts.append(DepAccount)
    else:
        SavAccount  = SavingAccount.SavingAccount(account_no,name,balance)
        all_accounts.append(SavAccount)

all_accounts = []

while True:
    print("To create the Saving Account select 1 \nTo create Deposit Account select 2 \nTo add interest in in account using account no select 3\nTo Add Amount in Account using Account no select 4 and for withdraw use 5\nTo quite select 6")
    selection = input("Select any one of this ") 

    if(selection == "1"):
        Account = createAccount("Saving")
        print("you account created")

    elif(selection == "2"):
        createAccount("Deposit")
        print("your account created")

    elif(selection == "3"):
        print("in which account you want to add the interest amount")
        account_no = input("write your account NO: ")
        for i in all_accounts:
            if i.get_account_no() == account_no:
                i.add_interest()
                break
        print("enter valid account no")
        
    elif(selection == "4"):
        account_no = input("write your account NO: ")
        for i in all_accounts:
            if i.get_account_no() == account_no:
                amount = int(input("enter Amount to deposite: "))
                i.deposit(amount)
                break
        print("enter valid account no")

    elif(selection == "5"):
        account_no = input("write your account NO: ")
        for i in all_accounts:
            if i.get_account_no() == account_no:
                amount = int(input("enter Amount to withdraw: "))
                i.withdraw(amount)
                break
        print("enter valid account no")

    elif(selection == "6"):
        break
    else:
        print("enter valid command")
