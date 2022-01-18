#Vehicle pollution check database management system using python and mysql connectivity
#Simple project for understanding mysql connectivity with python

import mysql.connector
import datetime
import string
import random
import smtplib
from email.message import EmailMessage
password = "sql@123" #your mysql password goes here
db = mysql.connector.connect(host='localhost',user="root",passwd=password)
mycursor = db.cursor()
mycursor.execute("CREATE DATABASE if not exists carpoll")
db = mysql.connector.connect(host='localhost',user="root",passwd=password,database="carpoll")
mycursor = db.cursor()

#creating tables
mycursor.execute("CREATE TABLE if not exists Admin(username varchar(50), password varchar(50))")
mycursor.execute("CREATE TABLE if not exists Pollution(PUCC_No varchar(20) PRIMARY KEY, Vehicle_RegNo varchar(20), Make varchar(50), Model varchar(20), Category varchar(20), EmissionNorms varchar(10), Fuel varchar(10), Testdate DATE, Validity DATE, Measured_Co decimal(5,2), Measured_HC integer)")


# Function for sending email
def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    #it is recommended to make your own mail ID to send the emails!!
    #for better understanding of email function, check out emailSend.py
    user = "pollutionucp@gmail.com"
    msg['from'] = user
    password = "cvjhxitjteiairxh"
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    print("Your PUCC number is sent to your email for future refrence!!")
    server.quit()


def check_pucc(pucc):
    mycursor.execute("Select PUCC_No from Pollution where PUCC_No=%s",(pucc,))
    rec = mycursor.fetchall()
    for i in rec:
        a = i[0]
        return(a)

def pas_fail(co,hc):
    if co<0.5 and hc<750:
        return True
    else:
        return False

#for pucc number we need to generate a random string
def pucc_generate():
    digs = string.digits
    chars=string.ascii_uppercase
    b = ''
    a = random.choice(chars)
    for i in range(9):
        b += random.choice(digs)
    c = a+b
    return(str(c))


def create_new_entery():
    pucc = pucc_generate()
    to = input("Enter your email id:")
    subject = "PUCC No."
    body = "Your PUCC number is " + pucc
    email_alert(subject,body,to)
    prev_pucc = check_pucc(pucc)
    if prev_pucc!=pucc:
        regno = input("Enter the registration number of vehicle:").upper()
        make = input("Enter the make of the vehicle:")
        model = input("Enter the model of car:")
        category = input("Enter the category of the vehicle:")
        emission = input("Enter the Emission Norms:")
        fuel = input("Enter the fuel type:")
        now=datetime.datetime.now()
        tdate = now.strftime("%y-%m-%d")
        val = now + datetime.timedelta(days=365)
        validity = val.strftime("%y-%m-%d")
        # validity = input("Enter date in yyyy-mm-dd format:")
        co = float(input("Enter the measured co, prescribed is 0.5-->"))
        hc = int(input("Enter the measured hc, precribed is 750-->"))
        test = pas_fail(co,hc)
        if test:
            query = "insert into Pollution(PUCC_No,Vehicle_RegNo,Make,Model,Category,EmissionNorms,Fuel,Testdate,Validity,Measured_Co,Measured_HC)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            value = (pucc,regno,make,model,category,emission,fuel,tdate,validity,co,hc)
            mycursor.execute(query,value)
            db.commit()
            print("Congratulations your vehicle stands on the prescribed limits of Pollution Under Control Certificate!")
            cer_choice = input("Do you want to print the certificate (y/n)?")
            if cer_choice == 'y' or cer_choice == "Y":
                certificate(pucc)
        else:
            print("Sorry your vehicle has failed the pollution under control test!!")
    else:
        print("This pucc number already exists!!")
        choice = int(input("Do you want to enter a new record or renew this record??\nPress 1 to enter new\nPress 2 to update this-->"))
        if choice == 1:
            create_new_DTH()
        if choice == 2:
            update_record(pucc)

def update_record(pucc):
    prev_pucc = check_pucc(pucc)
    if pucc == prev_pucc:
        now=datetime.datetime.now()
        new_tdate = now.strftime("%y-%m-%d")
        val = now + datetime.timedelta(days=365)
        new_validity = val.strftime("%y-%m-%d")
        # validity = input("Enter date in yyyy-mm-dd format:")
        new_co = float(input("Enter the measured co, prescribed is 0.5-->"))
        new_hc = int(input("Enter the measured hc, prescribed is 750-->"))
        test = pas_fail(new_co,new_hc)
        if test:
            query = "update Pollution set Testdate=%s,Validity=%s,Measured_Co=%s,Measured_HC=%s where PUCC_No=%s"
            mycursor.execute(query,(new_tdate,new_validity,new_co,new_hc,pucc))
            print("Congratulations your vehicle stands on the prescribed limits of Pollution Under Control Certificate!")
            db.commit()
        else:
            print("Sorry your vehicle has failed the pollution under control test!!")
    else:
        print("No such record exists!!")

def delete_record():
    dpucc = input("Enter the pucc number for deleting:")
    prev_pucc = check_pucc(dpucc)
    if dpucc == prev_pucc:
        mycursor.execute("delete from Pollution where PUCC_No=%s",(dpucc,))
        print("Record deleted succesfully")
        db.commit()
    else:
        print("No such record exists!!")

def show_record():
    spucc = input("Enter the pucc no to be displayed:")
    prev_pucc = check_pucc(spucc)
    if spucc == prev_pucc:
        mycursor.execute("SELECT * FROM Pollution where PUCC_No=%s",(spucc,))
        rec = mycursor.fetchall()
        for x in rec:
            print(x)
    else:
        print("No such record exists!")

def fetchdata():
    mycursor.execute("SELECT * FROM Pollution")
    rec = mycursor.fetchall()
    for x in rec:
        print(x)


def managemnet():
    choice = 'y'
    while choice == 'Y' or choice == 'y':
        print("Enter your choice:")
        print("1. Enter new record")
        print("2. Renew the record")
        print("3. Delete a record")
        print("4. Display a particular record")
        print("5. Show data")
        print("6. Print certificate of an existing record")
        print("7. Back")
        ch = int(input("Enter the choice:"))
        if ch == 1:
            create_new_entery()
        elif ch == 2:
            pucc = input("Enter the pucc number:")
            update_record(pucc)
        elif ch == 3:
            delete_record()
        elif ch == 4:
            show_record()
        elif ch == 5:
            fetchdata()
        elif ch == 6:
            pucc = input("Enter the pucc number:")
            certificate(pucc)
        elif ch == 7:
            break
        else:
            print("Wrong input!!")
        choice = input("Do you want to continue (y/n)?")

# main_menu()


def signup():
    user_name = input("Enter new user name:")
    paswd = input("Create password:")
    confirmpass = input("Confirm your password:")
    if paswd == confirmpass:
        mycursor.execute("insert into Admin values(%s,%s)",(user_name,paswd))
        db.commit()
        print("Account created succesfuly")
        main_menu()
    else:
        print("Confirm password and password should be same!!")


def login():
    uname = input("Enter your username:")
    pas = input("Enter your password:")
    mycursor.execute("SELECT * FROM Admin")
    rec = mycursor.fetchall()
    login_dic = {}
    for i in rec:
        login_dic[i[0]] = i[1]
    # print(login_dic)
    key,value = uname, pas
    a = key in login_dic and value == login_dic[key]
    return a

def table_format(text,length):
    if len(text) > length:
        text = text[:length]
    elif len(text)< length:
        text = (text + " " * length)[:length]
    return text

def certificate(pucc):
    # pucc = input("Enter PUCC No.--")
    prev = check_pucc(pucc)

    if pucc == prev:
        print("-"*50)
        t1 = "POLLUTION UNDER CONTROL CERTIFICATE"
        x = t1.center(50)
        print(x)
        print("-"*50)
        mycursor.execute("SELECT * FROM POLLUTION where PUCC_No=%s",(pucc,))
        rec = mycursor.fetchall()
        list1 = []
        for i in rec:
            print("PUCC No. DL -->",i[0])
            print("Vehicle Reg. No. -->",i[1])
            print("Make -->",i[2])
            print("Model -->",i[3])
            print("Category -->",i[4])
            print("Emission Norms -->",i[5])
            print("Fuel -->",i[6])
            print("Date -->",i[7])
            print('Validity',i[8])
            l1 = ["Fuel","Prescribed Standard CO.","Measured Level CO.","Prescribed Standard HC","Measured Level HC"]
            l2 = [i[6],'0.5',str(i[9]),'750',str(i[10])]
            list1.append(l2)
            print("*"*130)
            print("* ",end = " ")
        for column in l1:
            print(table_format(column,25), end = "  ")
        print()
        print("*"*130)
        for row in list1:
                print("*", end = " ")
                for column in row:
                    print(table_format(column,25), end = "   ")
                print()
        print("*"*130)
    else:
        print("No such record exists, Try Enter new record first!!")
        managemnet()


def main_menu():
    choice = 'y'
    while choice == 'y' or choice == 'Y':
        print("1. Already a user? Login")
        print("2. Create new account")
        print("3. Exit")
        ch = int(input("Enter your choice:"))
        if ch == 1:
            login_check = login()
            if login_check == True:
                print("Welcome to the Pollution under control Certificate center!!")
                managemnet()
            else:
                print("Wrong username or password")
                main_menu()

        elif ch == 2:
            signup()
        elif ch == 3:
            quit()
        else:
            print("Wrong Input")
            main_menu()

main_menu()
