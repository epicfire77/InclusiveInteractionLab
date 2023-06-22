import re
from bs4 import BeautifulSoup as bs
import os
from flask import *
from markupsafe import Markup
from datetime import datetime



#* time and date stuff
now = datetime.now()

current_time = now.strftime("%H:%M:%S").split(':')
print("Current Time =", current_time)

current_date = str(now.date()).replace('-','')
print("Current date =",current_date)
# location = "HELLO"
# date = "DATE"
# time = "TIME"

# print(cal_url)
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/hello")
def hello_world():
    return "Hi"

# regex = r'((\d?\d?\d?[-\.\s]??\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\d?\d?\d?[-\.\s]??\(\d{3}\)[-\.\s]*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))|(\d+[ ](?:[A-Za-z0-9.-]+[ ]?)+(?:Avenue|Lane|Road|Boulevard|Drive|Street|Ave|Dr|Rd|Blvd|Ln|St)\.?(\,?\s?\d{5}?)?)'

regexNum = r'(\d?\d?\d?[-\.\s]??\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\d?\d?\d?[-\.\s]??\(\d{3}\)[-\.\s]*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'

regexAddress = r'\d+[ ](?:[A-Za-z0-9.-]+[ ]?)+(?:Avenue|Lane|Road|Boulevard|Drive|Street|Ave|Dr|Rd|Blvd|Ln|St)\.?(\,?\s?\d{5}?)?'

# regexEvent = r'(((0?[1-9]|[0-2][0-2])[:\.\s]([0-5][0-9]) ?([AaPp][Mm])?)[ ,-]?((at|on)?) ?)?((([0-2]?[0-9]|3[0-1])[,\-\.\s]?[,-\.\s]?(January|Jan|February|Feb|Febuary|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|Sep|October|Octob|Oct|November|Nov|December|Dec))|((January|Jan|February|Feb|Febuary|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|Sep|October|Octob|Oct|November|Nov|December|Dec)[,-\.\s]?[,-\.\s]?([0-2]?[0-9]|3[0-1]))([,-\.\s][,-\.\s]?(1[0-9]|20)?\d{2})?)?'

regexEvent = r'(((0?[1-9]|[0-2][0-2])[:\.\s]([0-5][0-9]) ?([AaPp][Mm])?)[ ,-]?((at|on)?) ?)((([0-2]?[0-9]|3[0-1])[,\-\.\s]?[,-\.\s]?(January|Jan|February|Feb|Febuary|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|Sep|October|Octob|Oct|November|Nov|December|Dec))|((January|Jan|February|Feb|Febuary|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|Sep|October|Octob|Oct|November|Nov|December|Dec)[,-\.\s]?[,-\.\s]?([0-2]?[0-9]|3[0-1]))([,-\.\s][,-\.\s]?(1[0-9]|20)?\d{2})?)|(0?[1-9]|[0-2][0-2])[:\.\s]([0-5][0-9]) ?([AaPp][Mm])|((([0-2]?[0-9]|3[0-1])[,\-\.\s]?[,-\.\s]?(January|Jan|February|Feb|Febuary|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|Sep|October|Octob|Oct|November|Nov|December|Dec))|((January|Jan|February|Feb|Febuary|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|Sep|October|Octob|Oct|November|Nov|December|Dec)[,-\.\s]?[,-\.\s]?([0-2]?[0-9]|3[0-1]))([,-\.\s][,-\.\s]?(1[0-9]|20)?\d{2})?)'

regexEven = r'(January|Jan|February|Feb|Febuary|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|Sep|October|Octob|Oct|November|Nov|December|Dec)'

regexTime = r'(0?[1-9]|[0-2][0-2])[:\.\s]([0-5][0-9]) ?([AaPp][Mm])'

regexDate = r'((([0-2]?[0-9]|3[0-1])[,\-\.\s]?[,-\.\s]?(January|Jan|February|Feb|Febuary|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|Sep|October|Octob|Oct|November|Nov|December|Dec))|((January|Jan|February|Feb|Febuary|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|Sep|October|Octob|Oct|November|Nov|December|Dec)[,-\.\s]?[,-\.\s]?([0-2]?[0-9]|3[0-1]))([,-\.\s][,-\.\s]?(1[0-9]|20)?\d{2})?)'
messages=[]
@app.route("/msg/",methods=['POST','GET'])
def hello():
    if request.method == 'POST':
        msg = request.form['message']
        x =  str(re.sub(regexAddress,address,str(re.sub(regexNum,phone,msg))))
        y = str(re.sub(regexEvent,event,x))
        messages.append(y)
        print(messages)
        return render_template("msg.html", messages=messages)
    else:
        messages.clear()
        # msg = request.args.get('name')
        return render_template("msg.html", messages=['No messages'])
    x =  str(re.sub(regexAddress,address,str(re.sub(regexNum,phone,msg))))
    return str(re.sub(regexEvent,event,x))

def phone(x):
    return '<a href="tel:+'+str(x.group(0)).strip() + '\">'+str(x.group(0))+'</a>'

def address(y):
    return '<a href="https://google.com/maps/place/'+str(y.group(0)).strip() + '\">'+str(y.group(0))+'</a>'

def event(z):
    #time
    if str(z.group(0))!='':
        try:
            hr = str(re.search(regexTime,str(z.group(0))).group(1)).strip()
        except(AttributeError):
            hr = str((int(current_time[0])+7)%24)
        try:
            min = str(re.search(regexTime,str(z.group(0))).group(2)).strip()
        except(AttributeError):
            min = current_time[1]
        try:
            xm = str(re.search(regexTime,str(z.group(0))).group(3)).strip()
        except(AttributeError):
            xm = "PM"
            if int(current_time[0])<12:
                xm = "AM"
        if (int(hr) == 12):
            if (xm.upper()=='AM'):
                xm = 'PM'
            else:
                xm = 'AM'
        if (int(hr) == 12)&(xm.upper()=='PM'):
            xm = 'AM'
        hr = str(int(hr)+7)
        if xm.upper() == "PM":
            hr = str((int(hr)+12)%24)
        
        if int(hr) < 10:
            hr = '0' + str(int(hr))
        
        #day and month

        mnList = {'Jan':'01','January':'01','Feb':'02','February':'02','Febuary':'02','Mar':'03','March':'03','Apr':'04','April':'04','May':'05','Jun':'06','June':'06','Jul':'07','July':'07','Aug':'08','August':'08','Sep':'09','Sept':'09','September':'09','Oct':10,'Octob':10,'October':10,'Nov':11,"November":11,'Dec':12,'December':12}
        try:
            mn = re.search(regexDate,str(z.group(0))).group(6).strip()
        except(AttributeError):
            mn = current_date[4:5]
        try:
            mn = str(int(mn))
        except:
            mn = str(mnList[mn])
        try:
            dy = re.search(regexDate,str(z.group(0))).group(7).strip()
        except(AttributeError):
            dy = current_date[-2:]
        dy2 = str(int(dy)+1)

        dy = str(int(dy)+1)
        if (int(hr)<5) | (xm.upper() == "AM"):
            dy = str(int(dy)-1)

        if int(hr) < 10:
            hr = '0' + str(int(hr))
        hr1 = str(int(hr)+1)
        if int(hr1) < 10:
            hr1 = '0' + str(int(hr1))

        
        try:
            yr = str(re.search(regexDate,str(z.group(0))).group(8)).strip(',').strip()
        except:
            yr = current_date[:4]
        if yr:
            if len(yr) == 2:
                yr = '20'+yr
        print(str(f'<a href="https://www.google.com/calendar/render?action=TEMPLATE&dates={yr}{mn}{dy}T{hr}{min}00Z%2F{yr}{mn}{dy}T{hr1}{min}00Z">'+str(z.group(0))+'</a>'))
        return str(f'<a href="https://www.google.com/calendar/render?action=TEMPLATE&dates={yr}{mn}{dy}T{hr}{min}00Z%2F{yr}{mn}{dy}T{hr1}{min}00Z">'+str(z.group(0))+'</a>')

    else:
        return ''

def this(a):
    return str(a)

# @app.route('/num/<msg>')
# def num(msg):
#     print(msg)
#     return msg
# # event("time is 1:15PM date is November 11 2022")



if __name__ == "__main__":

    app.run(debug=True)


