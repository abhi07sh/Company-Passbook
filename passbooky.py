import tkinter as tk
import datetime, time
import re
import sqlite3


acc_data = sqlite3.connect("accounts.db")
txn_data = sqlite3.connect("transactions.db")
cr_acc = acc_data.cursor()
cr_txn = txn_data.cursor()


# acc_data_tmp = sqlite3.connect(":memory:")
# txn_data_tmp = sqlite3.connect(":memory:")
# cr_acc = acc_data_tmp.cursor()
# cr_txn = txn_data_tmp.cursor()
# cr_acc.execute("""CREATE TABLE accounts(
#             username text,
#             Fisrt_name text,
#             Last_name text,
#             DOB text,
#             email_id text,
#             password text,
#             tot_balance integer
#              )""")

window = tk.Tk()
window.title("My PassBook")
window.geometry("500x300")
window.configure(bg="yellow")
canvas = tk.Canvas(window, width=500, height=300,bg='yellow',outline=None)
# canvas.pack()
canvas.place(x=0, y=70)
small_font = ('Verdana',10)
medium_font = ('Verdana',13)
large_font = ('Verdana',15)
username = tk.StringVar()
pasword = tk.StringVar()
first_name = tk.StringVar()
last_name = tk.StringVar()
email = tk.StringVar()
acc_balance = tk.StringVar()
user_name = tk.StringVar()
acc_name = tk.StringVar()
cash_flow = tk.StringVar()
cash_mode = tk.StringVar()
amount = tk.StringVar()
txn_date = tk.StringVar()
txn_month = tk.StringVar()
txn_year = tk.StringVar()
cashFlow_list = ['CREDIT','DEBIT']
cashMode_list = ['CASH','UPI','cheque'.upper(),'Other']
cashAdd_dateList = [date for date in range(1,32)]
cashAdd_monthList = ['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
# for cashAdd_yearList check add_date() function
today_year = int(datetime.date.today().strftime("%Y"))
today_month = int(datetime.date.today().strftime("%m"))
today_day = int(datetime.date.today().strftime("%d"))
cashAdd_yearList = [yr for yr in range(today_year, 2015, -1)]
# to clear after logged out
all_entrys = [username, pasword, first_name, last_name, email, acc_balance, user_name, acc_name, cash_flow, cash_mode, amount, txn_date, txn_month, txn_year]

global next_time
next_time  = 0

label_time = tk.Label(window, text="placeholder")
label_time.place(x=270, y=20)

class User:
    def __init__(self,first, last, email_id, username, pasword, balance):
        if last is None:
            last = ''
        self.first = first
        self.last = last
        self.email_id = email_id
        self.username = username
        self.pasword = pasword
        self.balance = balance
def check_user_name(userName, fetch_details = False):
    cr_acc.execute("SELECT * FROM Accounts WHERE username=:user_name", {'user_name':userName})
    tmp_list = cr_acc.fetchone()
    if fetch_details:
        return  tmp_list
    if tmp_list is None:
        return False
    else:
        return True
def commit_user(cur_user):
    with acc_data:
        cr_acc.execute("INSERT INTO Accounts VALUES (:username, :first, :last, :dob, :email, :password, :balance)",
                       dict(username=cur_user.username, first=cur_user.first, last=cur_user.last, dob="N/A",
                            email=cur_user.email_id, password=cur_user.pasword, balance=cur_user.balance))
def signup_menu():
    first_name = input("First_name:")
    last_name = input("Last_name:")
    # dob = input("Date of Birth:")
    email_id = input("email_id:")
    balance = int(input('Balance :'))
    user_name = input("user_name:")
    pas_word = input("pass word:")
    # check_user_name(user_name)
    if check_user_name(user_name):
        cur_user = User(first_name, last_name, email_id, user_name, pas_word, balance)
        commit_user(cur_user)
    else:
        signup_menu()
def check_username_password(userName, pasWord):

    cr_acc.execute("SELECT * FROM accounts WHERE username=:user_name AND password=:pas_word", {'user_name': userName, 'pas_word': pasWord})
    tmp_list = cr_acc.fetchone()
    if tmp_list is None:
        check_user_name(userName)
        return False
    else:
        return True
class Transaction:
    def __init__(self, username, txn_name, txn_amt, txn_date, flow, mode):
        if txn_date is None:
            txn_date = 'N/A'
        if flow is None:
            flow = 'N/A'
        if mode == 'Mode':
            mode = 'N/A'
        self.txn_name = txn_name
        self.txn_date = txn_date
        self.flow = flow
        self.username = username
        self.mode = mode
        self.txn_amt = int(txn_amt)
def commit_txn(cur_txn):
    cr_acc.execute("SELECT * FROM Accounts WHERE username=:username",{'username':cur_txn.username})
    tmp_list = cr_acc.fetchone()
    if tmp_list is None:
        raise Exception("User name problem")
    if cur_txn.flow == 'cr':
        tmp_balance = tmp_list[-1] + cur_txn.txn_amt
    elif cur_txn.flow == 'de':
        tmp_balance = tmp_list[-1] - cur_txn.txn_amt
    with acc_data:
        cr_acc.execute("UPDATE Accounts SET tot_balance=:balance WHERE username=:username",{'balance':int(tmp_balance), "username":cur_txn.username})
    with txn_data:
        cr_txn.execute("INSERT INTO Transactions VALUES (:txn_name, :amt, :flow, :date, :balance, :mode,  :username)",
                       dict(username=cur_txn.username, txn_name=cur_txn.txn_name, flow=cur_txn.flow, mode=cur_txn.mode,
                            date=cur_txn.txn_date, amt=cur_txn.txn_amt, balance=tmp_balance))
def check_name(name):
    regex = re.compile("[@_!#$%^&*',.\"()<>?/\|}{~:;]")

    if not name.isalpha() and not name == '': # latter one is for optional name where
        # only alpha is needed or else complete empty
        return False
    if (regex.search(name) == None):
        return True
    else:
        return False
def check_userName(name):
    regex = re.compile("[!#$%^&*',.\"()<>?/\|}{~:;]")
    if not name[0].isalpha() and not name[1].isalpha() is not None:
        return False
    if len(name) > 2 and (regex.search(name[2:]) == None):
        return True
    else:
        return False
def clear_screen():

    y = 65
    for _ in range(7):
        label_screen = tk.Label(window, text="", bg='yellow', fg='white', width=30,
                                font=("arial", 20, "bold"))
        label_screen.place(x=0, y=y)
        y += 38
def add_headline():
    # HeadLine = My PassBook
    label_passbook = tk.Label(window, text="My PassBook", relief="solid", bg='coral3', fg='white', width=12,
                           font=("arial", 20, "bold"))
    label_passbook.place(x=30, y=20)
def add_date():
    # show date
    # global cashAdd_yearList
    # global today_year, today_day, today_month
    today = datetime.date.today().strftime("%d %B, %Y")

    today_year = int(datetime.date.today().strftime("%Y"))
    today_month = int(datetime.date.today().strftime("%m"))
    today_day = int(datetime.date.today().strftime("%d"))
    # today_day =  int(datetime.date.today().strftime("%Y"))
    cashAdd_yearList = [yr for yr in range(today_year, 2015, -1)]
    label_date = tk.Label(window, text=today, font=("arial", 10))
    label_date.place(x=270, y=40)
def add_sign_login():
    clear_screen()
    # signup
    buton_signup = tk.Button(window, text="Sign Up", bg='red', fg='white', width=10,
                           font=("arial", 10, "bold"), command=signup_start)
    buton_signup.place(x=120, y=150)

    # login
    buton_login = tk.Button(window, text="Login", bg='sea green', fg='white', width=8,
                           font=("arial", 10, "bold"), command=login_start)
    buton_login.place(x=300, y=150)
def set_time():
    currentTime = datetime.datetime.now().strftime("%H: %M: %S")
    label_time['text'] = currentTime
    window.after(1000, set_time)
def add_homePage():
    add_userLogo(our_user)
    clear_screen()
    # add button
    buton_add = tk.Button(window, text="ADD", bg='sea green', fg='white', width=10,
                             font=("arial", 10, "bold"), command=add)
    buton_add.place(x=120, y=150)
    # add history
    buton_history = tk.Button(window, text="HISTORY", bg='goldenrod', fg='white', width=8,
                              font=("arial", 10, "bold"), command=history)
    buton_history.place(x=300, y=150)
    # home
    buton_home = tk.Button(window, text="LogOut", bg='red', fg='white', width=10,
                             font=("arial", 10, "bold"), command=Inroduction)
    buton_home.place(x=200, y=250)
def add_credentials():
    # clear screen
    clear_screen()
    # add username label
    label_username = tk.Label(window, text="Username :", font=("arial", 15))
    label_username.place(x=120, y=150)
    # add username entry
    entry_username = tk.Entry(window, textvar=username, font=small_font)
    entry_username.place(x=250, y=153)
    # add pasword label
    label_pasword = tk.Label(window, text="Password :", font=("arial", 15))
    label_pasword.place(x=120, y=200)
    # add pasword entry
    entry_pasword = tk.Entry(window, textvar=pasword, font=small_font, show='*')
    entry_pasword.place(x=250, y=205)
    # show_login()
    buton_login = tk.Button(window, text="Login", bg='sea green', fg='white', width=8,
                            font=("arial", 10, "bold"), command=login_verify)
    buton_login.place(x=320, y=250)
    # back
    buton_back = tk.Button(window, text="Sign up", bg='red', fg='white', width=8,
                             font=("arial", 10, "bold"), command=signup_start)
    buton_back.place(x=200, y=250)
def take_credentials():
    global entry_balance

    x_label, y_label  = 150, 70
    x_entry, y_entry  = 250, 70
    y_label_width = 30
    y_entry_width = 30
    # clear screen
    clear_screen()

    # add firstName label
    label_first_name = tk.Label(window, text="First Name*:", font=("arial", 12))
    label_first_name.place(x=x_label, y=y_label)
    # add firstName entry
    entry_first_name = tk.Entry(window, textvar=first_name, font=small_font)
    entry_first_name.place(x=x_entry, y=y_entry)
    # add lastName label
    y_label += y_label_width
    label_last_name = tk.Label(window, text="Last Name:", font=("arial", 12))
    label_last_name.place(x=x_label, y=y_label)
    # add lastName entry
    y_entry += y_entry_width
    entry_last_name = tk.Entry(window, textvar=last_name, font=small_font)
    entry_last_name.place(x=x_entry, y=y_entry)
    # add email label
    y_label += y_label_width
    label_email = tk.Label(window, text="email ID*:", font=("arial", 12))
    label_email.place(x=x_label, y=y_label)
    # add email_id entry
    y_entry += y_entry_width
    entry_email = tk.Entry(window, textvar=email, font=small_font)
    entry_email.place(x=x_entry, y=y_entry)
    # add balance label
    y_label += y_label_width
    label_balance = tk.Label(window, text="Balance*: Rs.", font=("arial", 12))
    label_balance.place(x=x_label, y=y_label)
    # add balance entry
    y_entry += y_entry_width
    entry_balance = tk.Entry(window, textvar=acc_balance, font=small_font)
    entry_balance.place(x=x_entry, y=y_entry)
    # add username label
    y_label += y_label_width
    label_username = tk.Label(window, text="User Name*:", font=("arial", 12))
    label_username.place(x=x_label, y=y_label)
    # add username entry
    y_entry += y_entry_width
    entry_username = tk.Entry(window, textvar=username, font=small_font)
    entry_username.place(x=x_entry, y=y_entry)
    # add pasword label
    y_entry += y_entry_width
    y_label += y_label_width
    label_pasword = tk.Label(window, text="Password*:", font=("arial", 12))
    label_pasword.place(x=x_label, y=y_label)
    # add pasword entry
    entry_pasword = tk.Entry(window, textvar=pasword, font=small_font, show='*')
    entry_pasword.place(x=x_entry, y=y_entry)
    # signup
    buton_signup = tk.Button(window, text="Sign Up", bg='sea green', fg='white', width=10,
                             font=("arial", 10, "bold"), command=signup_verify)
    buton_signup.place(x=x_entry+55, y=y_entry+35)
    # back
    buton_back = tk.Button(window, text="Login", bg='red', fg='white', width=10,
                             font=("arial", 10, "bold"), command=login_start)
    buton_back.place(x=x_label+20, y=y_label+35)
def show_account():
    clear_screen()
    user_details = check_user_name(our_user, fetch_details=True)
    userid, fst, lst, _, emel, __, bal = user_details
    text = f"User ID >> {userid}\n   Name >> {fst} {lst}\n Email Id >> {emel}\nAccount Balance >> Rs.{bal}"
    label_name = tk.Label(window, text=text, font=('arial', 20), bg='yellow', fg='maroon')
    label_name.place(x=80, y=100)
    label_name = tk.Label(window, text="go back ^", font=('arial', 10), bg='yellow', fg='red')
    label_name.place(x=398, y=77)
    # home
    buton_home = tk.Button(window, text="LogOut", bg='red', fg='white', width=10,
                           font=("arial", 10, "bold"), command=Inroduction)
    buton_home.place(x=200, y=250)
    clear_logo()
    add_userLogo(our_user,True)
def add_userLogo(name=None, back=False):
    if name is not None:
        # label_logo = tk.Label(window, text=name[:2].upper(), font=("Lucida Console", 45))
        # label_logo.place(x=420, y=0)
        text = name[0].upper() + '' + name[1].upper()
        if back:
            buton_logo = tk.Button(window, text=text, width=3, bg='gray90',
                                   font=("Lucida Console", 30, "bold"), command=add_homePage)
        else:
            buton_logo = tk.Button(window, text=text, width=3, bg='gray90',
                                   font=("Lucida Console", 30, "bold"), command=show_account)
        buton_logo.place(x=390, y=0)


def clear_entry():
    for each in all_entrys:
        each.set('')


def clear_logo():
    #clear all entrys
    clear_entry()


    # incase of back clicks---
    label_screen = tk.Label(window, text="", bg='yellow', fg='white', width=50,
                            font=("arial", 50, "bold"))
    label_screen.place(x=390, y=0)
    # ---------
def show_options():
    add_homePage()
def get_txn_history(userName):
    cr_txn.execute("SELECT * FROM Transactions WHERE username=:user_name", {'user_name': userName})
    tmp_list = cr_txn.fetchall()
    return tmp_list
def write_block(x, y, opt_Name, inverted):
    if inverted:
        b_g, f_g = 'sea green','white'
    else:
        b_g, f_g = 'gold', 'black'
    label_name = tk.Label(window, text=str(opt_Name), font=(5), bg=b_g, fg=f_g)
    label_name.place(x=x, y=y + 70)
def create_rectBlock(x, y, width,inverted):
    if inverted:
        b_g, f_g = 'sea green','white'
    else:
        b_g, f_g = 'gold', 'black'
    label_name = tk.Label(window, text=' '*width, font=(5),bg=b_g)
    label_name.place(x=x, y=y+70)
def create_cols(col_xy, inverted, rows_list):
    cols = {'sN': 5, 'ac_name': 46, 'amount': 15, 'flow': 4, 'balance': 22, 'date': 17}
    cols_width = {'sN': 30, 'ac_name': 195, 'amount': 70, 'flow': 25, 'balance': 98, 'date': 70}
    if rows_list is None:
        write_mode = False
    else:
        write_mode =True

    i = 0
    for each in cols:
        b_wt = cols[each]
        if write_mode:
            write_block(col_xy[0], col_xy[1], rows_list[i], inverted)
        else:
            create_rectBlock(col_xy[0], col_xy[1], b_wt, inverted)
        col_xy = (col_xy[0] + cols_width[each], col_xy[1])
        i += 1
def create_tableRows(rows, rows_list=None, index=0):
    b_ht = 28
    col_xy = [3, 10]
    if type(rows_list) is tuple:
        rows_list = [rows_list]
    j = index
    for i in range(rows):
        if i%2 == 0:
            inverted =True
        else:
            inverted=False
        if rows_list is not None:
            tmp_list = list(rows_list[i])
            tmp_list.insert(0, j+1)
            create_cols(col_xy, inverted, tmp_list)
            j += 1
        else:
            create_cols(col_xy, inverted, rows_list)


        col_xy[1] += b_ht


def create_history_blocks(nime):
    global next_time, history_count
    # |DATE|ACC NAME|AMT|FLOW|MODE
    total_tiles = 7
    hdate_list = [' '*12 for _ in range(total_tiles)]
    hac_name_list = [' '*24 for _ in range(total_tiles)]
    hamt_list = [' '*15 for _ in range(total_tiles)]
    hflow_list = [' '*10 for _ in range(total_tiles)]
    hmode_list = [' '*10 for _ in range(total_tiles)]
    hbalance_list = ['Rs.'+' '*19 for _ in range(total_tiles)]
    hsNo_list = [str(_)+')' for _ in range(total_tiles)]
    hdate_list[0], hac_name_list[0], hamt_list[0], hflow_list[0], hmode_list[0], hbalance_list[0] = 'Date   ',' '*5 + ' Name '+' '*5, ' Amount ', 'Flow', 'Mode','  Balance  '
    hsNo_list[0] = 'S.No'

    size_pixel = {'date': 60,'ac_name': 110,'amount':70,'flow':50,'mode':50,'balance':100}
    # temp soln
    txn_list = get_txn_history(our_user)
    n = 0
    if len(txn_list) > 0:
        txn_list = txn_list[::-1]
        if next_time is not None:
            from_index = next_time*6
            txn_list = txn_list[from_index:]
        if next_time == 0:
            history_count = len(txn_list)
        n = min(len(txn_list), total_tiles)
        if n > 6:
            n = 6
        create_tableRows(n)
        create_tableRows(n, txn_list, index=from_index)
    else:
        alert = 'No Transactions Found'
        label_name = tk.Label(window, text=alert, font=('arial',25), bg='yellow', fg='red')
        label_name.place(x=80, y=130)

    if n < 6:
        #   show_add
        buton_next = tk.Button(window, text="Add", bg='sea green', fg='white', width=6,
                               font=("arial", 10, "bold"), command=add)
        buton_next.place(x=280, y=265)


    elif history_count > (next_time+1)*6:
        #   show_next
        buton_next = tk.Button(window, text=">", bg='sea green', fg='white', width=6,
                               font=("arial", 10, "bold"), command=next_click)
        buton_next.place(x=280, y=265)
    if next_time > 0:
        # back
        buton_back = tk.Button(window, text="<", bg='sea green', fg='white', width=6,
                               font=("arial", 10, "bold"), command=reduce_click)
        buton_back.place(x=50, y=265)
    # else:
    #     buton_back = tk.Button(window, text="Add", bg='sea green', fg='white', width=6,
    #                            font=("arial", 10, "bold"), command=add)
    #     buton_back.place(x=50, y=265)
    buton_back = tk.Button(window, text="Home", bg='red', fg='white', width=6,
                                 font=("arial", 10, "bold"), command=add_homePage)
    buton_back.place(x=167, y=265)
def show_history(next_time=None):
    clear_screen()
    create_history_blocks(next_time)
def check_date():
    # return false if ok
    tn_day = int(txn_date.get())
    tn_month = cashAdd_monthList.index(txn_month.get()) + 1
    tn_year = int(txn_year.get())
    if tn_year < today_year:
        return False
    else:
        if tn_month < today_month:
            return False
        elif tn_month == today_month:
            if tn_day <= today_day:
                return False
    return True
def transaction_verify():
    global cashAdd_monthList
    amount_str = None
    acc_name_str = None
    flow_str = None
    txn_day_str = None
    # verify_ acc name
    if acc_name.get() == '':
        acc_Alert = "empty\t"
    elif check_name(acc_name.get()):
        acc_name_str = acc_name.get()
        acc_Alert = "\t" * 3
    else:
        acc_Alert = "X Special"
    label_accNameAlert = tk.Label(window, text=acc_Alert, bg='yellow', font=("arial", 12))
    label_accNameAlert.place(x=435, y=80)

    # cash flow verify >> no need for mode its optional
    if cash_flow.get() == 'Flow' :
        cashAlert = "select"
    else:
        flow_str = cash_flow.get()[:2].lower()
        cashAlert = "\t"*3
    label_cashAlert = tk.Label(window, text=cashAlert, bg='yellow', font=("arial", 12))
    label_cashAlert.place(x=435, y=120)

    # day/month/year verify
    if txn_date.get() == 'Day' or txn_month.get() == 'Month' or txn_year.get() == 'Year':
        txn_dayAlert = "select"
    else:
        thirty_month = ['Apr', 'June', 'Sept', 'Nov']
        if (txn_date.get() == '31' and txn_month.get() in thirty_month) or (int(txn_date.get()) >= 29 and txn_month.get() == 'Feb'):
            txn_dayAlert = "X date\t"
        elif check_date():
            txn_dayAlert = "!) reaM"
        else:
            month_no = cashAdd_monthList.index(txn_month.get()) + 1
            txn_dayAlert = "\t"*3
            txn_day_str = txn_date.get() + '/' + str(month_no) + '/' + txn_year.get()
    label_dayAlert = tk.Label(window, text=txn_dayAlert, bg='yellow', font=("arial", 12,"bold"))
    label_dayAlert.place(x=430, y=150)

    # amount_verify
    if amount.get() == '':
        amtAlert = "empty\t"
    elif len(amount.get()) >= 7:
        amtAlert = "too rich"
    elif amount.get().isdigit():
        amtAlert = "\t"*3
        amount_str = amount.get()
        while amount_str[0] == '0':
            amount_str = amount_str[1:]
        entry_amount.delete(0, "end")
        entry_amount.insert(0, amount_str)
    else:
        amtAlert = "X digit"
    label_amtalert = tk.Label(window, text=amtAlert, bg='yellow', font=("arial", 12))
    label_amtalert.place(x=435, y=190)

    add_txn_list = [acc_name_str, amount_str, txn_day_str, flow_str]
    if  not None in add_txn_list:
        actionAlert = '\t'*3
        cur_txn = Transaction(our_user, acc_name_str, amount_str, txn_day_str, flow_str, cash_mode.get())
        commit_txn(cur_txn)
        added()
    else:
        actionAlert = "Try Again.."
    label_actionalert = tk.Label(window, text=actionAlert, bg='yellow', font=("arial", 12,"bold"))
    label_actionalert.place(x=400, y=270)
        # add()
def add_transaction():
    global entry_amount
    # clear screen
    clear_screen()
    # add account holder from/to cash got
    label_name = tk.Label(window, text="Name*:", font=("arial", 12))
    label_name.place(x=150, y=80)
    # add account holder entry

    entry_name = tk.Entry(window, textvar=acc_name, font=small_font)
    entry_name.place(x=250, y=80)

    # add cashFlow label
    label_cashflow = tk.Label(window, text="Cash *:", font=("arial", 12))
    label_cashflow.place(x=150, y=115)

    cashFlow_dropList = tk.OptionMenu(window, cash_flow, *cashFlow_list)
    cash_flow.set("Flow")
    cashFlow_dropList.configure(width=7)
    cashFlow_dropList.place(x=250, y=115)

    cashMode_dropList = tk.OptionMenu(window, cash_mode, *cashMode_list)
    cash_mode.set("Mode")
    cashMode_dropList.configure(width=7)
    cashMode_dropList.place(x=340, y=115)
    # add cashFlow entry
    # entry_cashflow = tk.Entry(window, textvar=cash_flow, font=small_font)
    # entry_cashflow.place(x=250, y=115)

    # add txn_date label
    label_cashAdd_date = tk.Label(window, text="Date* :", font=("arial", 12))
    label_cashAdd_date.place(x=150, y=150)
    # Day
    cashAdd_date_dropList = tk.OptionMenu(window, txn_date, *cashAdd_dateList)
    txn_date.set("Day")
    cashAdd_date_dropList.configure(width=5)
    cashAdd_date_dropList.place(x=250, y=150)
    # Month
    cashAdd_month_dropList = tk.OptionMenu(window, txn_month, *cashAdd_monthList)
    txn_month.set("Month")
    cashAdd_month_dropList.configure(width=5)
    cashAdd_month_dropList.place(x=300, y=150)
    # Year
    cashAdd_year_dropList = tk.OptionMenu(window, txn_year, *cashAdd_yearList)
    txn_year.set("Year")
    cashAdd_year_dropList.configure(width=5)
    cashAdd_year_dropList.place(x=350, y=150)
    # # add cashMode entry
    # entry_cashMode = tk.Entry(window, textvar=cash_mode, font=small_font)
    # entry_cashMode.place(x=250, y=150)

    # add amount label
    label_amount = tk.Label(window, text="Amt* (Rs.):", font=("arial", 12))
    label_amount.place(x=150, y=185)
    # add cashMode entry
    entry_amount = tk.Entry(window, textvar=amount, font=small_font)
    entry_amount.place(x=250, y=190)
    # add
    buton_add = tk.Button(window, text="ADD", bg='sea green', fg='white', width=10,
                             font=("arial", 10, "bold"), command=transaction_verify)
    buton_add.place(x=320, y=230)

    # back
    buton_cancel = tk.Button(window, text="Cancel", bg='red', fg='white', width=10,
                             font=("arial", 10, "bold"), command=add_homePage)
    buton_cancel.place(x=200, y=230)
def add():
    clear_screen()
    add_transaction()
def added():
    clear_screen()
    label_actionalert = tk.Label(window, text="Added", bg='yellow', font=("arial", 12, "bold"))
    label_actionalert.place(x=400, y=270)
    add_homePage()
def history():
    global next_time
    next_time = 0
    show_history(next_time)
def reduce_click():
    global next_time
    next_time -= 1
    show_history(next_time)
def next_click():
    global next_time
    next_time += 1
    show_history(next_time)
def signup_start():
    pasword.set('')
    take_credentials()
def signup_verify():
    firstName_str = None
    lastName_str = None
    email_str = None
    balance_str = None
    userName_str = None
    pasWord_str = None

    x_alert, y_alert = 420, 70
    y_alertWidth = 30
    # FISRT_NAME
    if first_name.get() == '':
        nameAlert = 'empty'
    elif len(first_name.get()) >= 20:
        nameAlert = 'name >='
    elif check_name(first_name.get()):
        tmp_name = first_name.get().strip()
        start_letter = tmp_name[0].upper()
        rest_letter = tmp_name[1:].lower()
        firstName_str = start_letter + rest_letter
        nameAlert = '\t'*3
    else:
        nameAlert = "X Special"
    label_namealert = tk.Label(window, text=nameAlert, bg='yellow', font=("arial", 12))
    label_namealert.place(x=x_alert, y=y_alert)
    y_alert += y_alertWidth
    # LAST_NAME
    if last_name.get().strip() == '':
        lastNameAlert = '\t'*3
    elif check_name(last_name.get()):
        tmp_name = last_name.get().strip()
        start_letter = tmp_name[0].upper()
        rest_letter = tmp_name[1:].lower()
        lastName_str = start_letter + rest_letter

        lastNameAlert = '\t'*3
    elif len(last_name.get()) >= 20:
        lastNameAlert = 'name <20'
    else:
        lastNameAlert = 'X Special'
    label_lastNamealert = tk.Label(window, text=lastNameAlert, bg='yellow', font=("arial", 12))
    label_lastNamealert.place(x=x_alert, y=y_alert)
    y_alert += y_alertWidth

    # email_id
    if email.get() == '':
        emailAlert = 'empty\t'
    elif email.get().endswith('.com') and '@' in email.get() and not email.get().endswith('@.com') and not email.get().startswith('@'):
        emailAlert = '\t' * 4
        email_str = email.get().lower()
    else:
        emailAlert = 'X email-id'
    label_emailAlert = tk.Label(window, text=emailAlert, bg='yellow', font=("arial", 12))
    label_emailAlert.place(x=x_alert, y=y_alert)
    y_alert += y_alertWidth

    # balance
    if acc_balance.get() == '':
        balanceAlert = 'empty\t'
    elif acc_balance.get().isdigit():
        balanceAlert = '\t' * 3
        balance_str = acc_balance.get()
        while balance_str[0] == '0':
            balance_str = balance_str[1:]
        entry_balance.delete(0, "end")
        entry_balance.insert(0, balance_str)

        if len(acc_balance.get()) >= 7:
            balanceAlert = 'too rich'
            balance_str = None
    else:
        balanceAlert = 'only paisa'
    label_balanceAlert = tk.Label(window, text=balanceAlert, bg='yellow', font=("arial", 12))
    label_balanceAlert.place(x=x_alert, y=y_alert)
    y_alert += y_alertWidth

    # USER_NAME
    if username.get() == '':
        usernameAlert = 'empty\t'
    elif len(username.get()) >= 10:
        usernameAlert = '< 10\t'
    elif len(username.get()) <= 2:
        usernameAlert = '> 3\t'
    elif not username.get()[:2].isalpha():
        usernameAlert = 'X special\t'
    elif check_user_name(username.get().strip().lower()):
        usernameAlert = 'exists'
    else:
        usernameAlert = '\t' * 3
        userName_str = username.get().strip().lower()
    label_userNamealert = tk.Label(window, text=usernameAlert, bg='yellow', font=("arial", 12))
    label_userNamealert.place(x=x_alert, y=y_alert)
    y_alert += y_alertWidth

     # Pass_Word
    if pasword.get() == '':
        paswordAlert = 'empty'
    elif len(pasword.get()) >= 15:
        paswordAlert = '<15\t'
    elif len(pasword.get()) <= 5:
        paswordAlert = '>5\t'
    else:
        paswordAlert = '\t'*3
        pasWord_str = pasword.get()
    label_paswordalert = tk.Label(window, text=paswordAlert, bg='yellow', font=("arial", 12))
    label_paswordalert.place(x=x_alert, y=y_alert)
    y_alert += y_alertWidth

    actionAlert = "\t" * 3
    signup_cred_list = [firstName_str, email_str, userName_str, pasWord_str, balance_str]
    if not None in signup_cred_list:
        cur_user = User(firstName_str, lastName_str, email_str, userName_str, pasWord_str, balance_str)
        commit_user(cur_user)
        login_start()

    else:
        actionAlert = "Try Again.."
    label_actionalert = tk.Label(window, text=actionAlert, bg='yellow', font=("arial", 12,"bold"))
    label_actionalert.place(x=400, y=270)
def login_start():
    pasword.set('')
    add_credentials()
def login_verify():
    global our_user
    alert = None
    if username.get().strip() == '' or pasword.get().strip() == '' or (not check_userName(username.get().strip())):
        alert = ":( Incorrect credentials !! Try again :)"
        # login_start()
    elif not check_username_password(username.get().strip(), pasword.get().strip()):
        alert = ":( Incorrect credentials !! Try again :)"
    else:
        our_user = username.get().strip()
        add_homePage()
    if alert is not None:
        label_actionalert = tk.Label(window, text=alert, bg='gold', font=("arial", 13,))
        label_actionalert.place(x=120, y=100)
def Inroduction():
    clear_logo()
    add_sign_login()

# label.pack()
set_time()
add_headline()
add_date()

login_start()
acc_data.commit()
txn_data.commit()
window.mainloop()
acc_data.close()
txn_data.close()