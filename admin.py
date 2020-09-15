import sqlite3

acc_data = sqlite3.connect("accounts.db")
txn_data = sqlite3.connect("transactions.db")

cr_acc = acc_data.cursor()
cr_txn = txn_data.cursor()

addTxn_tableCmd = """CREATE TABLE Transactions(
                                                txn_name text,
                                                amt integer,
                                                flow text,
                                                balance integer,
                                                txn_date text,
                                                mode text,
                                                username text
                                                )"""



def show_accounts(name = None):
    if name is None:
        cr_acc.execute("SELECT * FROM Accounts")
        print("All Accounts :")
    else:
        cr_acc.execute("SELECT * FROM Accounts WHERE username=:user_name", {'user_name':name})
        print(f"Details of {name} :")

    tmp_list = cr_acc.fetchall()

    if len(tmp_list) == 0:
        print("Not found")
    else:
        print("SNo, username, first name, last name, DOB, mail id, pasword, balance")
        i = 1
        for each in tmp_list:
            print(i, each, sep=") ")
            i += 1

def show_txns(acc = None):
    if acc is None:
        cr_txn.execute("SELECT * FROM Transactions")
        print("All Transactions :")
    else:
        print(f"Transactions of {acc} :")
    tmp_list = cr_txn.fetchall()
    if len(tmp_list) == 0:
        print("Not Found!")
    else:
        print("SNo, txn_name, amt, flow, balance, txn_date, mode, username")
        i = 1
        for each in tmp_list:
            print(i, each, sep=") ")
            i += 1

def delete_account(username):
    print("Transactions will be delted!!!")
    print("Type 0 to proceed, any other key to abort")
    proceed = int(input())
    if proceed == 0:
        cr_acc.execute("DELETE FROM Accounts WHERE username=:user_name", {'user_name': username})
        cr_txn.execute("DELETE FROM Transactions WHERE username=:txn_name", {'txn_name': username})
    else:
        print("Mission aborted")

def delete_transactions(txn_name):
    cr_txn.execute("DELETE FROM Transactions WHERE txn_name=:txn_name", {'txn_name': txn_name})

def show_intro():
    print("Show All Accounts : 0")
    print("Show All Transactions : 1")
    print("Show account by username : 2")
    print("Show transactions by txn_name : 3")
    ip = int(input("what you want : Enter"))
    if ip == 0:
        show_accounts()
    elif ip == 1:
        show_txns()
    elif ip == 2:
        name = input("enter username :")
        show_accounts(name)
    elif ip == 3:
        name = input("enter txn name :")
        show_txns(name)
    else:
        print("wrong input!")
        ex_it()

def del_intro():
    print("Delete account by username : 0")
    print("Delete transactions by txn_name : 1")
    ip = int(input("what you want : Enter"))
    if ip == 0:
        name = input("enter username :")
        delete_account(name)
    elif ip == 1:
        name = input("enter txn name")
        delete_transactions(name)
    else:
        print("wrong input!")
        ex_it()

def ex_it():
    acc_data.commit()
    txn_data.commit()
    acc_data.close()
    txn_data.close()
    exit()

def intro():
    print("SHOW : 0")
    print("DELETE : 1")
    ip = int(input("what you want : Enter"))
    if ip == 0:
        show_intro()
    elif ip == 1:
        del_intro()
    else:
        print("wrong input!")
        ex_it()

while True:
    intro()