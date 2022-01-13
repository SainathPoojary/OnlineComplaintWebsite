import threading
from flask import Flask,render_template,request,redirect,url_for,make_response
from flask_sqlalchemy import SQLAlchemy
import random,string
from sendEmail import sendMail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/complain")
def complain():
    return render_template("complain.html")

@app.route("/complainSubmission",methods=['POST'])
def complainSubmission():
    name = request.form['name']  
    email =request.form['email']  
    phone =request.form['phone']  
    station =request.form['station']  
    complaint =request.form['complain']
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
    # Inserting data into database  
    complain = Complains(name=name,email=email,phone=phone,station=station,complain=complaint,status=0,token=token)
    db.session.add(complain)
    db.session.commit()
    t1 = threading.Thread(target=sendMail,args=(email,name,token,0))
    t1.start()
    return render_template("token.html",token=token)

@app.route("/checkstatus")
def checkStatus():
    return render_template("checkStatus.html")

@app.route("/status",methods=['POST'])
def check():
    token = request.form['token']  
    complain = Complains.query.filter_by(token=token).first()
    return render_template("status.html",status=complain.status)

@app.route("/admin")
def admin():
    if(isAdmin()):
        return redirect(url_for('dashboard'))
    return render_template("admin.html")

@app.route("/login",methods=['POST'])
def login():
    username = request.form['username']  
    password = request.form['password']  
    admin = Admin.query.filter_by(username=username,password=password).first()
    if(admin!=None):
        resp = make_response(redirect(url_for('dashboard')))
        resp.set_cookie('username', username,max_age=86400)
        return resp
    else:
        return render_template("admin.html",error=True)

@app.route("/dashboard")
def dashboard():
    if(isAdmin()):
        data = Complains.query.filter_by(status=0).all()
        return render_template("dashboard.html",data=data)
    else:
        return redirect(url_for("admin"))

@app.route("/updatestatus",methods=['GET'])
def updateStatus():
    token = request.args.get('token')
    status = request.args.get('status')
    print(status)
    complain = Complains.query.filter_by(token=token).first()
    complain.status=status
    db.session.commit()
    t1 = threading.Thread(target=sendMail,args=(complain.email,complain.name,token,status))
    t1.start()
    return ""

# Utility Function
def isAdmin():
    username = request.cookies.get('username')
    return True if Admin.query.filter_by(username=username).first() !=None else False

app.jinja_env.globals.update(isAdmin=isAdmin)

# Database
class Complains(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    station = db.Column(db.String(120), nullable=False)
    complain = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer,nullable=False)
    token = db.Column(db.String(120),unique=True, nullable=False)
    def __repr__(self):
        return f' ({self.id} - {self.name} - {self.email} - {self.phone} - {self.station} - {self.complain} - {self.status} - {self.token})'

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return f' ({self.username} - {self.password})'

if __name__=="__main__":
    app.run(host="0.0.0.0",port=80,debug=True)