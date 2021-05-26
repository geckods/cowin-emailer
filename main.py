import json
import smtplib
import ssl
from datetime import datetime, timedelta

import requests

# 31: State Number For TamilNadu
# 571: Chennai District Number
# 557: Kanchipuram District Number
# 565: Chengalpet District Number

# curl 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=571&date=25-05-2021' \
#   -H 'authority: cdn-api.co-vin.in' \
#   -H 'pragma: no-cache' \
#   -H 'cache-control: no-cache' \
#   -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'upgrade-insecure-requests: 1' \
#   -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36' \
#   -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
#   -H 'sec-fetch-site: none' \
#   -H 'sec-fetch-mode: navigate' \
#   -H 'sec-fetch-user: ?1' \
#   -H 'sec-fetch-dest: document' \
#   -H 'accept-language: en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7' \
#   --compressed

headers = {
    # "authority": "authority: cdn-api.co-vin.in",
    # 'pragma': 'no-cache',
    # 'cache-control': 'no-cache',
    # 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    # 'sec-ch-ua-mobile': '?0',
    # 'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'sec-fetch-site': 'none',
    # 'sec-fetch-mode': 'navigate',
    # 'sec-fetch-user': '?1',
    # 'sec-fetch-dest': 'document',
    # 'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7'
}


def getDateString(daysToAdd):
    abc = datetime.now()
    abc += timedelta(days=daysToAdd)
    return datetime.now().strftime("%d-%m-%Y")


def checkDistrict(districtNumber, dateString):
    # print(getDateString())
    response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=" + str(districtNumber) + "&date=" + dateString, headers=headers)
    # print(response.json())
    assert (response.status_code == 200)
    return response.json()


def isGoodSession(sess):
    return sess['min_age_limit'] <= 21 and sess['available_capacity_dose1'] > 0


def sendEmail(goodSessions):
    print("SENDING EMAIL!!")

    port = 465  # For SSL
    password = "fupwqiuiqzcfezzk"

    # Create a secure SSL context
    context = ssl.create_default_context()

    message = """\
From: Gecko Test <geckotest79@yahoo.com>\nTo: Abhinav Ramachandran <geckods@gmail.com>\nSubject: COWIN Updates\n\n

These are the COWIN Updates:
"""

    message += "THE TIME IS " + str(datetime.now()) + "\n"

    for sess in goodSessions:
        message += "GOOD SESSION:\n"
        # message += json.dumps(sess)
        message += "Name: " + sess["name"] + "\n"
        message += "Vaccine: " + str(sess["vaccine"]) + "\n"
        message += "Available Sessions: " + str(sess["available_capacity_dose1"])
        message += "\n\n"

    server = smtplib.SMTP_SSL('smtp.mail.yahoo.com')
    # server.starttls()
    server.set_debuglevel(1)
    server.login("geckotest79@yahoo.com", password)
    # TODO: Send email here
    server.sendmail("geckotest79@yahoo.com", "geckods@gmail.com", message)
    server.quit()

    print("EMAIL SENT!!")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print(checkChennai())
    print("Program Is Starting")
    daySessions = [checkDistrict(571, getDateString(0)), checkDistrict(571, getDateString(1)), checkDistrict(571, getDateString(2)), checkDistrict(571, getDateString(3)), checkDistrict(571, getDateString(4)), checkDistrict(571, getDateString(5))]
    goodSessions = []
    numSessions = 0
    for chennaiSessions in daySessions:
        for sess in chennaiSessions['sessions']:
            # print("HI")
            numSessions += 1
            if isGoodSession(sess):
                goodSessions.append(sess)

    print("Collated a total of", numSessions, "sessions.")
    print("There are", len(goodSessions), "good sessions.")

    if len(goodSessions) > 0:
        sendEmail(goodSessions)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
