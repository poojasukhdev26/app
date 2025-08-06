from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import sqlite3
from datetime import date
from menu_data import init_menu_db, save_menu, get_today_menu
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# ✅ Email Configuration
EMAIL_ADDRESS = 'messmaitri@gmail.com'
EMAIL_PASSWORD = 'uwsjatddrigryxpj'

def send_otp_email(recipient_email, otp):
    msg = MIMEText(f'Your OTP is: {otp}')
    msg['Subject'] = 'OTP Verification'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ OTP sent via Email")
        return True
    except Exception as e:
        print("❌ Failed to send email:", e)
        return False

# ✅ DB Initialization
def init_mess_db():
    conn = sqlite3.connect('mess_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mess (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mess_name TEXT,
            owner_name TEXT,
            location TEXT,
            mobile TEXT,
            email TEXT,
            otp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def init_consumer_db():
    conn = sqlite3.connect('mess_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS consumers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            location TEXT,
            mobile TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

def init_review_db():
    conn = sqlite3.connect('mess_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mess_name TEXT NOT NULL,
            review TEXT NOT NULL,
            rating INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ✅ Run all DB setups once
init_mess_db()
init_consumer_db()
init_menu_db()
init_review_db()

# 🚀 Splash Screen
@app.route('/')
def splash():
    return render_template('logo.html')

# 🏠 Home Page
@app.route('/home')
def home():
    return render_template('index.html')

# 🎭 Choose Role
@app.route('/choose_role')
def choose_role():
    return render_template('choose_role.html')

# 🧍 Role-Based Registration Redirect
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form.get('role')
        session['role'] = role
        if role == 'owner':
            return render_template('register.html')
        elif role == 'consumer':
            return render_template('register_consumer.html')
        else:
            return "❌ Invalid role selected"
    return render_template('choose_role.html')

# 📧 Get OTP for both consumer and owner
@app.route('/get_otp', methods=['POST'])
def get_otp():
    role = session.get('role')
    if role == 'owner' and 'mess_name' in request.form:
        data = {
            'role': 'owner',
            'mess_name': request.form['mess_name'],
            'owner_name': request.form['owner_name'],
            'location': request.form['location'],
            'mobile': request.form['mobile'],
            'email': request.form['email']
        }
    elif role == 'consumer' and 'name' in request.form:
        data = {
            'role': 'consumer',
            'name': request.form['name'],
            'location': request.form['location'],
            'mobile': request.form['mobile'],
            'email': request.form['email']
        }
    else:
        return "❌ Invalid role selected or missing data"

    otp = str(random.randint(1000, 9999))
    session['otp'] = otp
    session['registration_data'] = data

    if send_otp_email(data['email'], otp):
        return redirect(url_for('verify_otp'))
    else:
        return "❌ Failed to send OTP."

# 🔐 OTP Verification
@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if 'otp' not in session or 'registration_data' not in session:
        return redirect(url_for('register'))

    if request.method == 'POST':
        entered_otp = request.form['otp']
        if entered_otp == session['otp']:
            data = session['registration_data']
            conn = sqlite3.connect('mess_data.db')
            c = conn.cursor()
            if data['role'] == 'owner':
                c.execute("INSERT INTO mess (mess_name, owner_name, location, mobile, email) VALUES (?, ?, ?, ?, ?)",
                          (data['mess_name'], data['owner_name'], data['location'], data['mobile'], data['email']))
                conn.commit()
                conn.close()
                session['mess_name'] = data['mess_name']
                session.pop('otp', None)
                session.pop('registration_data', None)
                return redirect(url_for('submit_menu'))

            elif data['role'] == 'consumer':
                c.execute("INSERT INTO consumers (name, location, mobile, email) VALUES (?, ?, ?, ?)",
                          (data['name'], data['location'], data['mobile'], data['email']))
                conn.commit()
                conn.close()
                session.clear()
                return redirect(url_for('show_menu'))

        else:
            return "❌ Invalid OTP. Try again."
    return render_template('otp_verify.html', otp=session.get('otp'))

# 🍽 Submit Today's Menu
@app.route('/submit_menu', methods=['GET', 'POST'])
def submit_menu():
    if request.method == 'POST':
        mess_name = session.get('mess_name', 'Unknown Mess')
        if mess_name == 'Unknown Mess':
            flash('You must register and verify as a mess owner before submitting a menu.')
            return redirect(url_for('register'))
        date_value = request.form['date']
        print(f"[DEBUG] Saving menu for date: {date_value}")
        breakfast = request.form['breakfast']
        lunch = request.form['lunch']
        dinner = request.form['dinner']
        save_menu(mess_name, date_value, breakfast, lunch, dinner)
        return redirect(url_for('show_menu'))

    return render_template('submit_menu.html')

# 📅 Show Menu
@app.route('/show_menu')
def show_menu():
    today_menu = get_today_menu()
    return render_template('show_menu.html', menus=today_menu)

# ⭐ Review Page
@app.route('/review', methods=['GET'])
def review():
    return render_template('review.html')

@app.route('/submit_review', methods=['POST'])
def submit_review():
    name = request.form['name']
    mess_name = request.form['mess_name']
    review = request.form['review']
    rating = int(request.form['rating'])

    conn = sqlite3.connect('mess_data.db')
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO reviews (name, mess_name, review, rating)
        VALUES (?, ?, ?, ?)
    ''', (name, mess_name, review, rating))
    conn.commit()
    conn.close()

    return "<h3>⭐ Thanks for your feedback!</h3><a href='/'>Back to Home</a>"

# ✅ Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
