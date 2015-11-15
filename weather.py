__author__ = 'Zachary Charles Newton'
import requests
import json
import smtplib
import datetime

MYZIPCODE = '40206'

def current():
    f = requests.get('http://api.wunderground.com/api/74197920a8d4cc1b/geolookup/conditions/q/{0}.json'.format(MYZIPCODE))
    json_string = f.text
    parsed_json = json.loads(json_string)
    location = parsed_json['location']['city']
    feelslike = parsed_json['current_observation']['feelslike_f']
    condition = parsed_json['current_observation']['weather']
    time = parsed_json['current_observation']['observation_time_rfc822'][:16]
    mysub = "Feels like: " + feelslike + "F, Condtion: " + condition +", "+ location + ", " + time
    return mysub

def tenday():
    f = requests.get('http://api.wunderground.com/api/74197920a8d4cc1b/geolookup/forecast10day/q/{0}.json'.format(MYZIPCODE))
    json_string = f.text

    parsed_json = json.loads(json_string)
    day_list = parsed_json['forecast']['txt_forecast']['forecastday']
    myret = "******\n\nNext Five Days\n******\n"
    count = 0
    for day in day_list:
        title = day['title']
        forecast = day['fcttext'].split(".")
        myret += title + "\n"
        count2 = 0
        for line in forecast:
            myret += line.strip()
            count2+=1
            if count2 < len(forecast):
                myret += ".\n"
        if count == 8:
            break
        myret += "******"+"\n"
        count+=1
    return myret

def hourly():
    f = requests.get('http://api.wunderground.com/api/74197920a8d4cc1b/geolookup/hourly/q/{0}.json'.format(MYZIPCODE))
    #f = open('forecast.json')
    json_string = f.text
    parsed_json = json.loads(json_string)
    time_list = parsed_json['hourly_forecast']
    myret = "Next 12 Hours:\n******\n"
    count = 0
    for hour_interval in time_list:
        if count == 12:
            break
        day = hour_interval['FCTTIME']['weekday_name']
        civil_time = hour_interval['FCTTIME']['civil']
        condition = hour_interval['condition']
        feels_like = hour_interval['feelslike']['english'] + "F"
        humidity = hour_interval['humidity'] + "%"
        wind = hour_interval['wspd']['english'] + " mph"
        myret += civil_time +" "+ day+"\n"+condition+"\n"+"Feels Like: "+feels_like+"\n"+ "Humidity: "+humidity+"\n"+"Wind: "+wind+"\n"+"******"+"\n"
        count+=1
    return myret

def mailer(subject, body):
    myfrom = sys.argv[1]
    myto = sys.argv[2]
    myun = sys.argv[3]
    mypw = sys.argv[4]
    server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    msg = "\r\n".join([
        "From: {0}".format(myfrom),
        "To: {0}".format(myto),
        "Subject: " + subject,
        "",
        body
    ])
    server.login(myun, mypw)
    server.sendmail(myfrom, myto,msg)
    server.close()

def main():
    subject = current()
    hourly_cond = hourly()
    tenday_cond = tenday()
    body = hourly_cond + tenday_cond
    mailer(subject, body)

main()

