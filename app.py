from flask import Flask, request, render_template, jsonify
import pandas as pd
import email_sender
import scheduler

app = Flask(__name__)

# Load CSV/Google Sheets Data
@app.route('/upload', methods=['POST'])
def upload_data():
    file = request.files['file']
    data = pd.read_csv(file)
    return jsonify(data.columns.tolist())  # Return column names for field selection

# Customize and Send Emails
@app.route('/email_sender.py', methods=['POST'])
def send_emails():
    data = request.json['data']
    prompt = request.json['prompt']
    email_sender.send_custom_emails(data, prompt)
    return jsonify({"status": "Emails sent successfully"})

# Schedule Emails
@app.route('/scheduler.py', methods=['POST'])
def schedule_emails():
    data = request.json['data']
    prompt = request.json['prompt']
    time = request.json['time']
    scheduler.schedule_emails(data, prompt, time)
    return jsonify({"status": "Emails scheduled successfully"})

# Dashboard Route
@app.route('/dashboard.html')
def dashboard():
    stats = email_sender.get_email_stats()
    return render_template('dashboard.html', stats=stats)

if __name__ == "_main_":
    app.run(debug=True)
