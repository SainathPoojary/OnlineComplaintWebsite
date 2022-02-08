import smtplib,os
from email.mime.text import MIMEText
from twilio.rest import Client

# Twilio Credentials
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

# SMTP Credentials
EMAIL = "onlinecmplnt@gmail.com"
PASSWORD = os.environ.get("emailPassword")

# Sends Mail using SMTP
def sendMail(email,name,token,op):
    html,subject="",""
    if(op==0):
        subject = 'Your Complaint was registered successfully'
        html = f"""
        <p style="line-height: 1.7;">
        Hey <b>{name}</b>,<br>
        We have Recived your Complaint <br>
        It will be reviewed by my our officer in 2-3 bussiness days <br>
        You can check your Complaint status at below given link. <br>
        Your token number is <em style="color: #6366f1; background-color: rgb(216, 216, 216); padding: 2px;" >{token}</em> <br>
        <p>
        <a href="https://complaintregistration.herokuapp.com/checkstatus" style="text-decoration: none; background-color: #6366f1; color: white; border: 0; padding: 10px; border-radius: 5px;">Check Status</a>
        </p>
        </p>
        """
    elif(op=="-1"):
        subject = 'Your Complaint was Rejected!'
        html = f"""
        <p style="line-height: 1.7;">
        Hey <b>{name}</b>,<br>
        Your complaint with token number <em style="color: #6366f1; background-color: rgb(216, 216, 216); padding: 2px;" >{token}</em> has been rejected ❌ do you to some reason <br>
        If you have any query you can contact us.
        <p>
        <a href="https://complaintregistration.herokuapp.com" style="text-decoration: none; background-color: #6366f1; color: white; border: 0; padding: 10px; border-radius: 5px;">Contact us</a>
        </p>
        """
    elif(op=="1"):
        subject = 'Your Complaint was Approved!'
        html=f"""
        <p style="line-height: 1.7;">
            Hey <b>{name}</b>,<br>
            Your complaint with token number <em
                style="color: #6366f1; background-color: rgb(216, 216, 216); padding: 2px;">{token}</em> has been
            approved. ✅ <br>
            Our officer will contact you as soon as possible. <br>
            If you have any query you can contact us.
        <p>
            <a href="https://complaintregistration.herokuapp.com"
                style="text-decoration: none; background-color: #6366f1; color: white; border: 0; padding: 10px; border-radius: 5px;">Contact
                us</a>
        </p>
        """


    
    msg = MIMEText(html, 'html')
    msg['Subject'] = subject
    msg['FROM'] = EMAIL
    msg['TO']=email 

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
        server.login(EMAIL,PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL, email, text)
        server.quit()

# Sending SMS using Twilio API
def sendSms(phoneNo,name,token,op):
    client = Client(account_sid, auth_token)
    if(op=="0"):
        msg=f" Hey {name}, We have Recived your Complaint. It will be reviewed by my our officer in 2-3 bussiness days.\nYou can check your Complaint status at below given link. Your Token number is {token}\nhttps://complaintregistration.herokuapp.com/checkstatus"
    elif(op=="-1"):
        msg=f" Hey {name}, Your complaint with token number {token} has been rejected ❌ do you to some reason. If you have any query you can contact us.\nhttps://complaintregistration.herokuapp.com"
    elif(op=="1"):
        msg=f" Hey {name}, Your complaint with token number {token} has been approved ✅. Our officer will contact you as soon as possible. If you have any query you can contact us. If you have any query you can contact us.\nhttps://complaintregistration.herokuapp.com"
        message = client.messages \
                .create(
                     body=msg,
                     from_='+16075644358',
                     to=f'+91{phoneNo}'
                 )
        print(message.status)

# Notify will send both SMS and MAIL
def notify(phoneNo,email,name,token,op):
    sendMail(email,name,token,op)
    sendSms(phoneNo,name,token,op)

