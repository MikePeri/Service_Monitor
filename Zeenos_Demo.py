# !/usr/bin/python3
import time
import datetime
import ast
import inquirer
import os
import sys
import platform
import stat
from random import randrange
from subprocess import call
import difflib
from difflib import *
import requests
import smtplib



def Email_Sending(text):
    TO = 'perrymykle@gmail.com'
    SUBJECT = 'Hacker Identifier'
    TEXT = '%s' % text
    gmail_sender = 'secureSerMon@gmail.com'
    gmail_passwd = '1@3$5^7*9)'
    print("Connecting to server...")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    print("Server connected.")
    server.ehlo()
    server.starttls()
    print("Login to email...")
    server.login(gmail_sender, gmail_passwd)
    print("Logged in.")
    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])

    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print('email sent successfully.')
    except:
        print('error sending mail')

    server.quit()
def Display_Ip_Content():
    print("Printing hacker content...")
    time.sleep(2)
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']
    geo_request = requests.get('https://get.geojs.io/v1/ip/geo/' +my_ip + '.json')
    geo_data = geo_request.json()
    info =str("Area code:\t"+geo_data['area_code']+
          "\nContinent code:\t"+geo_data['continent_code']+
          "\nCountry:\t" + geo_data['country'] +
          "\nCountry code:\t" + geo_data['country_code'] +
          "\nCountry code3:\t" + geo_data['country_code3'] +
          "\nIp address:\t" + geo_data['ip'] +
          "\nlatitude:\t"+geo_data['latitude']+
          "\nlongitude:\t"+geo_data['longitude']+
          "\nOrganization:\t" + geo_data['organization']+
          "\nTimezone:\t" + geo_data['timezone'])
    print(info)
    print("\nSending content to mail...\n")
    time.sleep(2)
    Email_Sending(info)
def print_Changes(file_Name):
    print("\nPrinting the changes line...")
    time.sleep(2)
    time.sleep(2)
    with open(file_Name) as f, open(file_Name) as g:
        flines = f.readlines()
        glines = g.readlines()

        d = difflib.Differ()
        diff = d.compare(flines, glines)
        print("\n".join(diff))
    g.close()
    f.close()
    time.sleep(2)
def Write_Text_To_File(text):
    f = open("Status_Log.txt", "a")
    f.write(text)
    f.close()

def Windows_initFiles():
    if not os.path.exists("serviceList.txt"):
        f= open(".serviceList.txt","x")
        f2 = open("serviceList.txt", "x")
        f.close()
        f2.close()
    if not os.path.exists("Status_Log.txt"):
        w=open(".Status_Log.txt","x")
        w2 = open("Status_Log.txt", "x")
        w.close()
        w2.close()
    call(["attrib", "+H", ".Status_Log.txt"])
    call(["attrib", "+H", ".serviceList.txt"])


def Linux_initFiles():
    if not os.path.exists("serviceList.txt"):
        f= open(".serviceList.txt","w+")
        f2 = open("serviceList.txt", "w+")
        f.close()
        f2.close()
    if not os.path.exists("Status_Log.txt"):
        w=open(".Status_Log.txt","w+")
        w2 = open("Status_Log.txt", "w+")
        w.close()
        w2.close()

def user_mode_input():
    questions = [
        inquirer.List('mode',
                      message="Which mode do you want to run?",
                      choices=['Monitor', 'Manual'],
                      ),
    ]
    answers = inquirer.prompt(questions)
    return answers["mode"]
def date_mode_input():
    questions = [
        inquirer.List('mode',
                      message="Which filter do you want to use?",
                      choices=['Print all the dates.', 'Filtering by date only.', 'Filtering by date and time.'],
                      ),
    ]
    answers = inquirer.prompt(questions)
    return answers["mode"]
def Linux_Manual_Continue():
    confirm = {
        inquirer.Confirm('confirmed',
                         message="Do you want to continue?",
                         default=True),
    }
    confirmation = inquirer.prompt(confirm)
    if confirmation["confirmed"]:
        return 1
    else:
        return 0
def dateHelp_user_input():
    confirm = {
        inquirer.Confirm('confirmed',
                         message="Do you want some help with picking proper dates?",
                         default=True),
    }
    confirmation = inquirer.prompt(confirm)
    if confirmation["confirmed"]:
        answer = date_mode_input();
        if(answer== 'Print all the dates.'):
            f = open("serviceList.txt", "r")
            x = f.readlines()
            print("Please copy two dates from the list to compare:\n")
            for i in x:
                print(i.split("*")[0] + "\n")
            f.close()
        elif(answer == 'Filtering by date only.'):
            print("List of all the dates:\n")
            time.sleep(2)
            dateLists()
            print("Please enter dates as the following format: yyyy-mm-dd Where y is year,m is month and d is day.\n")
            date_str1=raw_input("Pleaste enter the first date:\n")
            date_object1 = datetime.datetime.strptime(str(date_str1), '%Y-%m-%d').date()

            date_str2 = raw_input("Pleaste enter the second date:\n")
            date_object2 = datetime.datetime.strptime(str(date_str2), '%Y-%m-%d').date()
            dateLists_RangeDates(date_object1,date_object2,1)
        else:
            print("Please enter dates as the following format:year-month-day hour:minutes:seconds.\n")
            date_str1 = raw_input("Pleaste enter the first date:\n")
            date_object1 = datetime.datetime.strptime(str(date_str1), '%Y-%m-%d %H:%M:%S').date()
            date_str2 = raw_input("Pleaste enter the second date:\n")
            date_object2 = datetime.datetime.strptime(str(date_str2), '%Y-%m-%d %H:%M:%S').date()
            dateLists_RangeDates(date_object1, date_object2, 2)
def Win_ListServices():
    import win32con
    import win32service
    resume = 0
    accessSCM = win32con.GENERIC_READ
    accessSrv = win32service.SERVICE_ACTIVE

    #Open Service Control Manager
    hscm = win32service.OpenSCManager(None, None, accessSCM)

    #Enumerate Service Control Manager DB
    typeFilter = win32service.SERVICE_WIN32
    stateFilter = win32service.SERVICE_RUNNING

    statuses = win32service.EnumServicesStatus(hscm, typeFilter, stateFilter)

    for (short_name, desc, status) in statuses:
        print(short_name)
def Linux_ListServices():
    stream = os.popen('service --status-all 2>&1 | grep +')
    output = stream.read()
def Windows_Active_Services():
    import win32con
    import win32service
    list = []
    resume = 0
    accessSCM = win32con.GENERIC_READ
    accessSrv = win32service.SERVICE_RUNNING

    # Open Service Control Manager
    hscm = win32service.OpenSCManager(None, None, accessSCM)

    # Enumerate Service Control Manager DB
    typeFilter = win32service.SERVICE_WIN32
    stateFilter = win32service.SERVICE_ACTIVE

    statuses = win32service.EnumServicesStatus(hscm, typeFilter, stateFilter)

    for (short_name, desc, status) in statuses:
        list.append(short_name)
    # print(list)
    return list

def Linux_Active_Services():
    list = []
    stream = os.popen('service --status-all 2>&1 | grep +')
    output = str(stream.read()).replace("[ + ]", "").replace(" ", "")
    for line in output.splitlines():
        list.append(line)
    return list
def Time_Scheduler():
    while True:
        try:
            userInput = int(input("Please write down the period of time that you want to track in seconds:"))
            if(userInput>=3600):
                raise Exception("ERR:Not make any sense to check services changes per hour and more.")
        except ValueError:
            print("Not an valid input! Try again.")
            continue
        else:
            return userInput
            break

def removed_services(old,new):
    if (not isinstance(old, list) or not isinstance(old, list)):
        raise Exception("The arguments suppose to be list type")
    services=""
    for x in old:
        if(x not in new):
            services += x
            services += "\tStopped\n"
            #services += "\n"
            #print("DOWN")
    return services

def added_services(old,new):
    if(not isinstance(old,list) or not isinstance(old,list)):
        sys.exit("ERR: The arguments suppose to be list type.")
    services= "";
    for x in new:
        if(x not in old):
            services += x
            services+="\tRunning\n"
            #services += "\n"
            #print("UP")
    return services



def out_serviceList(new,id):
    global sList
    date_time = datetime.datetime.now()
    if(not isinstance(new,list)):
        sys.exit("ERR: The argument suppose to be list")
    if(id==1):
        f = open(".serviceList.txt", "a")

        f.write(date_time.strftime("%Y-%m-%d %H:%M:%S") + "*" + str(new) + "\n")
        f.close()
    elif(id==2):
        f = open("serviceList.txt", "a")
        f.write(date_time.strftime("%Y-%m-%d %H:%M:%S") + "*" + str(new) + "\n")
        f.close()
        sList = time.ctime(os.stat("serviceList.txt")[stat.ST_MTIME])
    else:
        f = open("serviceList.txt", "a")
        f.write(date_time.strftime("%Y-%m-%d %H:%M:%S") + "*" + str(new) + "\n")
        f.close()
        sList = time.ctime(os.stat("serviceList.txt")[stat.ST_MTIME])

    out_serviceList.num_log=out_serviceList.num_log+1
    #print("--------------------------SERVICE LIST---------------------------")
    #print("NUMBER OF LOG : "+str(out_serviceList.num_log)+"\n"+"Date = "+str(datetime.datetime.now())+"\n")
    #print(get_str(new))

out_serviceList.num_log=0

def out_statusLog(old,new,id):
    global sLog
    if id==1:
        f=open(".Status_Log.txt", "a")
    elif id==2:
        f = open("Status_Log.txt", "a")
    else:
        f = open("Status_Log.txt", "a")
    removed=removed_services(old,new)
    added=added_services(old,new)
    #print("Previous sLog is: "+str(sLog))
    if added!="" and removed=="":
            print(added+"\n")
            f.write(added+"\n")
            f.close()
    elif removed!="" and added=="":
            print(removed+"\n")
            f.write(removed+"\n")
            f.close()
    elif removed!="" and added!="":
            print(added + "\n")
            f.write(added + "\n")
            print(removed + "\n")
            f.write(removed + "\n")
            f.close()
    else:
            f.close()
    if id==2:
        sLog = time.ctime(os.stat("Status_Log.txt")[stat.ST_MTIME])
    out_statusLog.num_log = out_statusLog.num_log+1

out_statusLog.num_log=1

def get_str(list):
    log=""
    for x in list:
        log+=x
        log+="\n"
    return log

def manualMonitor(old_date,new_date):
    if(new_date<old_date):
        print("The first argument should be older")
        return
    if(new_date==old_date):
        print("Your trying to compare the same date...")
        return
    f = open("serviceList.txt", "r")
    count = 0
    x = f.readlines()
    for i in x:
        if (i.split("*")[0] == str(old_date)):
            old = ast.literal_eval(i.split("*")[1])
            count = count + 1
        if (i.split("*")[0] == str(new_date)):
            new = ast.literal_eval(i.split("*")[1])
            count = count + 1
    if (count != 2):
        print("There is no such a record")
    else:
        remove=removed_services(old,new)
        if(remove!=""):
            print(remove+"\n")
        added=added_services(old,new)
        if(added!=""):
            print(added + "\n")
    f.close()

def dateLists_RangeDates(date1,date2,mode):
    f = open("serviceList.txt", "r")
    x = f.readlines()
    print("Please copy two dates from the list to compare:\n")
    for i in x:
        if(mode==1):
            d=datetime.datetime.strptime(i.split("*")[0].split(" ")[0], '%Y-%m-%d')
        else:
            d = datetime.datetime.strptime(i.split("*")[0], '%Y-%m-%d %H:%M:%S')
        if(d.date()==date1 or d.date()==date2):
            print(i.split("*")[0]+"\n")
    f.close()

def dateLists():
    f = open("serviceList.txt", "r")
    x = f.readlines()
    list=[]
    for i in x:
        d=i.split("*")[0].split(" ")[0]
        if d not in list:
            list.append(d)
            print(d+"\n")
    f.close()

def timeLists(date1,date2):
    f = open("serviceList.txt", "r")
    x = f.readlines()
    list=[]
    for i in x:
        if i.split("*")[0].split(" ")[0]==date1 or i.split("*")[0].split(" ")[0]==date2:
            d=i.split("*")[0].split(" ")[1].split(".")[0]
            if d not in list:
                list.append(d)
                print(d+"\n")
    f.close()

def dateLists_Windows():
    user_decision=str(input("Enter 1 - for list all the dates.\nEnter 2 - for filtering by dates.\nEnter 3 - for filtering by date and time.\n"))
    if(user_decision.lower()=="1"):
        f = open("serviceList.txt", "r")
        x = f.readlines()
        print("Please copy two dates from the list to compare:\n")
        for i in x:
                print(i.split("*")[0]+"\n")
        f.close()
    elif(user_decision.lower()=="2"):
        print("List of all the dates:\n")
        time.sleep(2)
        dateLists()
        print("Please enter dates as the following format:year-month-day hour:minutes:seconds.\n")
        date_str1 = input("Pleaste enter the first date:\n")
        date_object1 = datetime.datetime.strptime(str(date_str1), '%Y-%m-%d').date()

        date_str2 = input("Pleaste enter the second date:\n")
        date_object2 = datetime.datetime.strptime(str(date_str2), '%Y-%m-%d').date()
        dateLists_RangeDates(date_object1, date_object2,1)
    elif (user_decision.lower() == "3"):
        print("Please enter dates as the following format:year-month-day hour:minutes:seconds.\n")
        date_str1 = input("Pleaste enter the first date:\n")
        date_object1 = datetime.datetime.strptime(str(date_str1), '%Y-%m-%d %H:%M:%S').date()
        date_str2 = input("Pleaste enter the second date:\n")
        date_object2 = datetime.datetime.strptime(str(date_str2), '%Y-%m-%d %H:%M:%S').date()
        dateLists_RangeDates(date_object1, date_object2,2)
    else:
        pass
def Monitoring(old,id):
    if(platform.system()=="Linux"):
        new=Linux_Active_Services()
    if (platform.system() == "Windows"):
        new = Windows_Active_Services()
    out_serviceList(new)
    out_statusLog(old,new)
    return new

def Windows_Authentication():
    User_Name = str(input("Please enter admin user name:"))
    Password = str(input("Please enter admin password:"))
    flag = 0
    for i in range(3):
        if User_Name != "MyklePerry" or Password != "1@3$5^7*9)":
            time.sleep(randrange(3))
            print("invalid password or username.\n")
            User_Name = str(input("Please enter admin user name:"))
            Password = str(input("Please enter admin password:"))
        else:
            flag = 1
            pass
    if flag == 0:
        sys.exit("ERR: running without admin permission.")
#Main program:

if platform.system()=="Windows":
    print("Running Windows version of this program.\n")
    Windows_Authentication()
    Windows_initFiles()
    time.sleep(randrange(4))
    print("Activate tool... Please wait.")
    time.sleep(randrange(4))
    print("Running tool as admin.\n")
    user_input=input("Please enter Manual or Monitor mode as string:\n")
    flag=0
    for i in range(2):
        if(user_input.lower()=="monitor" or user_input.lower()=="manual"):
            flag=1
            break;
        else:
            print("Please try again...")
            user_input = input("Please enter Manual or Monitor mode as string:\n")
    if flag==0:
        sys.exit("Sorry, but you didn't answer well 3 times!\nSystem stopped.")
elif platform.system()=="Linux":
    print("Running Linux version of this program.\n")
    if not os.geteuid() == 0:
        sys.exit("ERR: running without root permission.")
    Linux_initFiles()
    time.sleep(randrange(4))
    print("Activate tool... Please wait.")
    time.sleep(randrange(4))
    print("Running tool as root.\n")
    user_input=user_mode_input()
else:
    sys.exit("ERR: Not support this platform")

sLog= time.ctime (os.stat("Status_Log.txt") [ stat.ST_MTIME ] )
sList= time.ctime (os.stat("serviceList.txt") [ stat.ST_MTIME ] )

if(user_input.lower()=="monitor"):
    print("Activate monitor mode...")
    time.sleep(2)
    timer = Time_Scheduler()
    print("----------------------STATUS-LOG---------------------------")
    if(platform.system()=="Linux"):
        old = Linux_Active_Services()
    if(platform.system()=="Windows"):
        old = Windows_Active_Services()
    time.sleep(timer)
    out_serviceList(old,1)
    out_serviceList(old, 2)
    time.sleep(timer)
    while True:
        sList_Current=time.ctime(os.stat("serviceList.txt")[stat.ST_MTIME])
        sLog_Current=time.ctime(os.stat("Status_Log.txt")[stat.ST_MTIME])
        try:
            #If something happened while sleeping
            if not os.path.exists("serviceList.txt"):
                Display_Ip_Content()
                sys.exit("ERR: System detect unexpected delete serviceList.txt please check the file.\nSystem stopped.")
            if not os.path.exists("Status_Log.txt"):
                Display_Ip_Content()
                sys.exit("ERR: System detect unexpected delete Status_Log.txt please check the file.\nSystem stopped.")
            if (sList != sList_Current):
                print("Service List HACKED!!!\t" + str(sList_Current) + "\n")
                Display_Ip_Content()
                print_Changes("serviceList.txt")
                Write_Text_To_File(str(
                    "Service List HACKED!!!\t" + str(sList_Current) + "\n"))
                sys.exit(
                    "ERR: System detect unexpexted changes at serviceList.txt please check the file.\nSystem stopped.")
            if (sLog != sLog_Current):
                print("Status Log HACKED!!!" + "\t" + str(sLog_Current))
                Display_Ip_Content()
                print_Changes("Status_Log.txt")
                Write_Text_To_File(
                    str("Status Log HACKED!!!" + "\t" + str(sLog_Current)))
                sys.exit(
                    "ERR: System detect unexpexted changes at Status_Log.txt please check the file.\nSystem stopped.")

            if (platform.system() == "Linux"):
                new = Linux_Active_Services()
            if (platform.system() == "Windows"):
                new = Windows_Active_Services()
            out_serviceList(new, 2)
            out_statusLog(old, new, 2)

            temp =old
            old = new

            time.sleep(timer)

            out_serviceList(new, 1)
            out_statusLog(temp, new, 1)


        except KeyboardInterrupt:
            print("\nSystem notice of key board interrupt.\n")
            print("Closing the system...")
            time.sleep(2)
            break


elif(user_input.lower()=="manual"):
    print("Activate manual mode.")
    time.sleep(2)
    print("Welcome to manual format, this tool will allow you to check differences between 2 dates.\n")
    cont=1
    while(cont):
        if(platform.system()=="Linux"):
            dateHelp_user_input()
            old_date = raw_input("Enter old date:\n")
            new_date = raw_input("Enter new date:\n")
        else:
            dateLists_Windows()
            old_date = input("Enter old date:\n")
            new_date = input("Enter new date:\n")
        s=manualMonitor(old_date,new_date)
        if not s:
            print(s)
        if platform.system()=="Linux":
            cont=Linux_Manual_Continue()
        else:

            flag=0
            for i in range(3):
                cont=int(input("Do you want to continue?\nEnter 0 for NO.\nEnter 1 for YES.\n"))
                if(cont!=0 and cont!=1):
                    print("Wrong answer, please try again.")
                else:
                    flag=1
                    break;
            if(flag==0):
                sys.exit("ERR: you have input wrong answer three times.")
    print("Closing the system...")
    time.sleep(2)
else:
    sys.exit("ERR: Sorry, no such mode")

