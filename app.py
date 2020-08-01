import os
from flask import Flask, request
import smtplib
import imghdr
from email.message import EmailMessage

app = Flask(__name__)

# Parse Server Details
os.environ["PARSE_API_ROOT"] = "https://parseapi.back4app.com/"

from parse_rest.datatypes import Function, Object, GeoPoint
from parse_rest.connection import register
from parse_rest.query import QueryResourceDoesNotExist
from parse_rest.connection import ParseBatcher
from parse_rest.core import ResourceRequestBadRequest, ParseError

APPLICATION_ID = 'Ts1A7Zvn3GBJGN62VyvYJEUiKEJwyIBSumxwiPRk'
REST_API_KEY = 'mjbuzgxCofRDnSCUU7yovyKyKdkfSZr9KvJYqpgi'
MASTER_KEY = 'LHId46114Z1J3zwAggIwATTZ6CyWM1BpVAR4jZD3'

#Register the app with Parse Server
register(APPLICATION_ID, REST_API_KEY, master_key=MASTER_KEY)

# Sender Email ID and Password
EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

def sendEmail(result):
	with smtplib.SMTP("smtp.gmail.com", 587)as smtp:
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()

		smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)

		subject='Govt. of Sikkim | File Action Required'
		body='Hey your file with file ID:'+result['result']['FileID'] +' is pending. Please start / finish the job quickly if not done already.'
		msg= f'Subjext: {subject}\n\n{body}'

		smtp.sendmail(EMAIL_ADDRESS,'sarvesh4232@gmail.com',msg)

@app.route("/", methods=['POST','GET'])
def index():
	jobDeadline = Function("jobDeadline")
    result= jobDeadline(status="created")
    print(result)
    sendEmail(result)

    result= jobDeadline(status="reassigned - created")
    print(result)
    sendEmail(result)

    result= jobDeadline(status="pending")
    print(result)
    if(result['result']!="No Results Found"):
        sendEmail(result)

    result= jobDeadline(status="reassigned - pending")
    print(result)
    if(result['result']!="No Results Found"):
        sendEmail(result)
	
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))