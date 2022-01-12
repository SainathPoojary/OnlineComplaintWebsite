import smtplib,os
from email.mime.text import MIMEText

EMAIL = "onlinecmplnt@gmail.com"
PASSWORD = os.environ.get("PASSWORD")

# msg = EmailMessage()
html = open("./templates/email.html")
msg = MIMEText(html.read(), 'html')
msg['Subject'] = 'Your Complaint was registered successfully'
msg['FROM'] = EMAIL
msg['TO']='spoojary614@gmail.com' 
# msg.set_content("Your Complaint was registered successfully\nYour token is <i>USGKSGBFKHBKDJG</ i>")


with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
    server.login(EMAIL,PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL, "spoojary614@gmail.com", text)
    server.quit()