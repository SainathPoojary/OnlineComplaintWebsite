import smtplib,os
from email.mime.text import MIMEText


def sendMail(email,name,token,op):
    EMAIL = "onlinecmplnt@gmail.com"
    PASSWORD = os.environ.get("emailPassword")
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
        Hey <b>Sainath</b>,<br>
        Your complaint with token number <em style="color: #6366f1; background-color: rgb(216, 216, 216); padding: 2px;" >YFDSGJSFGSKJB28939</em> has been rejected ❌ do you to some reason <br>
        If you have any query you can contact us.
        <p>
        <a href="https://complaintregistration.herokuapp.com" style="text-decoration: none; background-color: #6366f1; color: white; border: 0; padding: 10px; border-radius: 5px;">Contact us</a>
        </p>
        """
    elif(op=="1"):
        subject = 'Your Complaint was Approved!'
        html=f"""
        <p style="line-height: 1.7;">
            Hey <b>Sainath</b>,<br>
            Your complaint with token number <em
                style="color: #6366f1; background-color: rgb(216, 216, 216); padding: 2px;">YFDSGJSFGSKJB28939</em> has been
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
    # msg.set_content("Your Complaint was registered successfully\nYour token is <i>USGKSGBFKHBKDJG</ i>")


    with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
        server.login(EMAIL,PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL, email, text)
        server.quit()
