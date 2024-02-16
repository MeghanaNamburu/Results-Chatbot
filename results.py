import telebot
import pandas as pd
import ast
import time

attendanceFlag=0
resultsFlag=0

data=pd.read_excel("results.xlsx")
data=data.iloc[:,:].values
data=list(data)
Rollno=[]
for i in data:
    Rollno.append(i[0])
data1=pd.read_excel("attendance.xlsx")
data1=data1.iloc[:,:].values
data1=list(data1)

token='6820671223:AAFBI9sr2_hd3Kwq_IV_1z6VR22R3dBfpM8'
bot = telebot.TeleBot(token, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.reply_to(message, "Welcome to students result and attendance check, what do you want to know? \n 1. /attendance \n 2. /cgpaAndPercentage \n 3. /SemWiseResults")

@bot.message_handler(commands=['cgpaAndPercentage'])
def handle_results_request(message):
    global resultsFlag
    bot.reply_to(message, "Please enter the student ID to which you want to check cgpa and percentage:")
    resultsFlag=1
@bot.message_handler(commands=['attendance'])
def handle_attendance_request(message):
    global attendanceFlag
    bot.reply_to(message, "Please enter the student ID for which you want to check attendance:")
    attendanceFlag=1
@bot.message_handler(commands=['SemWiseResults'])
def handle_results_request(message):
    global semresultsFlag
    bot.reply_to(message, "Please enter the student ID to which you want to check sem wise results:")
    semresultsFlag=1
  
@bot.message_handler(regexp="[a-zA-Z0-9_]")
def handle_message(message):
    global attendanceFlag,resultsFlag,semresultsFlag
    message=str(message)
    k=ast.literal_eval(message)
    #print(k,type(k))
    chat_id=(k['from_user']['id'])
    student_id=k['text'].upper()
    #print(m)
    flag=0
    #print(Rollno)

    for i in Rollno:
      #Attendance
      if(i==(student_id) and attendanceFlag==1):
        attendanceFlag=0
        flag=1
        rollindex=Rollno.index(i)
        atten=data1[rollindex][1]
        if(atten>90):
           feed="very good ! keep it up"
        elif(atten>=75 and atten<=90):
           feed="good!"
        elif(atten>=65 and atten<75):
           feed="need to improve!"
        else:
           feed="very poor! likely to be detained"
        bot.send_message(int(chat_id),'Hey ! Nice meeting to you.\nYour Registered Number is '+ str(i) +'.\nYour overall attendance is '+str(atten)+'% .\nAccording to your attendance you are '+str(feed)+'.')
      #cgpa and percentage
      if(i==(student_id) and resultsFlag==1):
        message=str(message)
        k=ast.literal_eval(message)
        chat_id=(k['from_user']['id'])
        student_id=k['text']
        flag=0
        for i in Rollno:
          if(i==(student_id) and resultsFlag==1):
            resultsFlag=0
            flag=1
            rollindex=Rollno.index(i)
            att=data[rollindex][10]
            agg=data[rollindex][9]
            bot.send_message(int(chat_id),'Hey,Nice meeting to you.\nYour Registered Numbers is ' + str(i) + '.\nyour academic percentage is '+str(att)+'% .\nyour aggregate is '+str(agg) + '.\n\nThank You')
        if(flag==0):
          bot.send_message(int(chat_id),"Sorry ! student ID is not present")
      #sem wise results
      if(i==(student_id) and semresultsFlag==1):
        message=str(message)
        k=ast.literal_eval(message)
        chat_id=(k['from_user']['id'])
        student_id=k['text']
        flag=0
        for i in Rollno:
          if(i==(student_id) and semresultsFlag==1):
            semresultsFlag=0
            flag=1
            rollindex=Rollno.index(i)
            att=data[rollindex][10]
            agg=data[rollindex][9]
            bot.send_message(int(chat_id),'Hey,Nice meeting to you.\nYour Registered Numbers is ' + str(i) + '.\nHere are your sem wise results.\nSemester 1 : '+str(data[rollindex][1])+'\nSemester 2 : '+str(data[rollindex][2])+'\nSemester 3 : '+str(data[rollindex][3])+'\nSemester 4 : '+str(data[rollindex][4])+'\nSemester 5 : '+str(data[rollindex][5])+'\nSemester 6 : '+str(data[rollindex][6])+'\nSemester 7 : '+str(data[rollindex][7])+'\nSemester 8 : '+str(data[rollindex][8])+'\n\nThank You')
        if(flag==0):
          bot.send_message(int(chat_id),"Sorry ! student ID is not present")

         
def listener(messages):
  for m in messages:
    print(str(m))

bot.set_update_listener(listener)

while True:
    try:
        bot.polling(none_stop=True, timeout=120)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)