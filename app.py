from turtle import home
from flask import Flask, redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'dfdsuhfwe78y57etrwud'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dmart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(500), nullable=False)

@app.route('/',methods=['GET', 'POST'])
def index():
    if 'uemail' in session and session['uemail'] == 'admin@gmail.com':
        return render_template('dm.html')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        contact = Contacts(name=name,email=email,subject=subject,message=message)
        db.session.add(contact)
        db.session.commit()
        flash("Message sent successfully", "success")
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    contacts = Contacts.query.all()
    return render_template('dashboard.html',contacts=contacts)
@app.route('/delete/<int:sno>')
def delete(sno):
    contact = Contacts.query.filter_by(sno=sno).first()
    db.session.delete(contact)
    db.session.commit()
    return redirect("/dashboard")
@app.route('/login', methods=['GET','POST'])
def login():
    if 'uemail' in session and session['uemail'] == 'admin@gmail.com':
        return render_template('dm.html')
    if request.method == 'POST':
        uemail = request.form['uemail']
        upassword = request.form['upassword']
        if uemail == "admin@gmail.com" and upassword == 'admin':
            session['email'] = uemail
            flash('Logged in successfully','success')
            return render_template('dm.html')
        else:
            flash('Incorrect email or password','danger')
            return render_template('login.html')
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('uemail',None)
    return render_template('login.html')
if __name__ == "__main__":
    app.run(debug=True)