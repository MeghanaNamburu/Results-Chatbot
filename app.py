import telebot
import pandas as pd
import ast
import time
import matplotlib.pyplot as plt
import requests
from io import BytesIO

print("Code Started")

# Function to download file from GitHub repository
def download_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        return None

attendanceFlag = 0
resultsFlag = 0
semresultsFlag = 0
performanceFlag = 0

results_url = 'https://raw.githubusercontent.com/MeghanaNamburu/Results-Chatbot/main/results.xlsx'
attendance_url = 'https://raw.githubusercontent.com/MeghanaNamburu/Results-Chatbot/main/attendance.xlsx'

data = pd.read_excel(download_file(results_url))
data = data.iloc[:, :].values
data = list(data)
Rollno = []
for i in data:
    Rollno.append(i[0])
data1 = pd.read_excel(download_file(attendance_url))
data1 = data1.iloc[:, :].values
data1 = list(data1)

token = '6820671223:AAFBI9sr2_hd3Kwq_IV_1z6VR22R3dBfpM8'
bot = telebot.TeleBot(token, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to students result and attendance check bot, what do you want to know? \n 1. /attendance \n 2. /cgpaAndPercentage \n 3. /SemWiseResults \n 4. /performanceGraph")

@bot.message_handler(commands=['cgpaAndPercentage'])
def handle_results_request(message):
    global resultsFlag
    bot.reply_to(message, "Please enter the student ID to which you want to check cgpa and percentage:")
    resultsFlag = 1

@bot.message_handler(commands=['attendance'])
def handle_attendance_request(message):
    global attendanceFlag
    bot.reply_to(message, "Please enter the student ID for which you want to check attendance:")
    attendanceFlag = 1

@bot.message_handler(commands=['SemWiseResults'])
def handle_results_request(message):
    global semresultsFlag
    bot.reply_to(message, "Please enter the student ID to which you want to check sem wise results:")
    semresultsFlag = 1

@bot.message_handler(commands=['performanceGraph'])
def handle_academic_performance_request(message):
    global performanceFlag
    bot.reply_to(message, "Please enter the student ID to visualize academic performance:")
    performanceFlag = 1

@bot.message_handler(regexp="[a-zA-Z0-9_]")
def handle_message(message):
    global attendanceFlag, resultsFlag, semresultsFlag, performanceFlag
    message = str(message)
    k = ast.literal_eval(message)
    chat_id = (k['from_user']['id'])
    student_id = k['text'].upper()
    flag = 0

    for i in Rollno:
        # Attendance
        if i == student_id and attendanceFlag == 1:
            attendanceFlag = 0
            flag = 1
            rollindex = Rollno.index(i)
            atten = data1[rollindex][1]
            if atten > 90:
                feed = "very good"
            elif 75 <= atten <= 90:
                feed = "good"
            elif 65 <= atten < 75:
                feed = "bad"
            else:
                feed = "very poor"
            bot.send_message(int(chat_id), f'Hey! Nice meeting you.\nYour Registered Number is {i}.\nYour overall attendance is {atten}%.\nYou are {feed} at maintaining your attendance.')
            
        # CGPA and percentage
        if i == student_id and resultsFlag == 1:
            resultsFlag = 0
            flag = 1
            rollindex = Rollno.index(i)
            att = data[rollindex][10]
            agg = data[rollindex][9]
            bot.send_message(int(chat_id), f'Hey! Nice meeting you.\nYour Registered Numbers is {i}.\nYour academic percentage is {att}%.\nYour aggregate is {agg}.\n\nThank You')
            
        # Sem wise results
        if i == student_id and semresultsFlag == 1:
            semresultsFlag = 0
            flag = 1
            rollindex = Rollno.index(i)
            att = data[rollindex][10]
            agg = data[rollindex][9]
            bot.send_message(int(chat_id), f'Hey! Nice meeting you.\nYour Registered Numbers is {i}.\nHere are your sem wise results.\nSemester 1: {data[rollindex][1]}\nSemester 2: {data[rollindex][2]}\nSemester 3: {data[rollindex][3]}\nSemester 4: {data[rollindex][4]}\nSemester 5: {data[rollindex][5]}\nSemester 6: {data[rollindex][6]}\nSemester 7: {data[rollindex][7]}\nSemester 8: {data[rollindex][8]}\n\nThank You')
            
        # Academic Performance (Line Graph)
        if i == student_id and performanceFlag == 1:
            performanceFlag = 0
            flag = 1
            rollindex = Rollno.index(i)
            semesters = ['Semester 1', 'Semester 2', 'Semester 3', 'Semester 4', 'Semester 5', 'Semester 6', 'Semester 7', 'Semester 8']
            marks = [data[rollindex][1], data[rollindex][2], data[rollindex][3], data[rollindex][4], data[rollindex][5], data[rollindex][6], data[rollindex][7], data[rollindex][8]]
            plt.plot(semesters, marks)
            plt.xlabel('Semester')
            plt.ylabel('Marks')
            plt.title('Academic Performance')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            plt.savefig('academic_performance.png')
            bot.send_photo(int(chat_id), open('academic_performance.png', 'rb'))
            plt.close()

    if flag == 0:
        bot.send_message(int(chat_id), "Sorry! Student ID is not present")

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

print("Code Ended")
