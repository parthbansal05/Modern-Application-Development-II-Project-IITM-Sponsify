from flask import Flask, request, jsonify
from celery import Celery
from celery.schedules import crontab
import smtplib
from email.mime.text import MIMEText
import csv
import os
from datetime import datetime


# Flask setup
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Celery setup
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Example data
influencers = [{'id': 1, 'email': 'influencer1@example.com', 'has_pending_ad_request': True}]
sponsors = [{'id': 1, 'email': 'sponsor1@example.com'}]

def send_email(subject, body, to):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'your-email@example.com'
    msg['To'] = to

    with smtplib.SMTP('smtp.example.com') as server:
        server.login('your-email@example.com', 'your-email-password')
        server.sendmail('your-email@example.com', to, msg.as_string())

def send_google_chat_message(webhook_url, message):
    import requests
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    response = requests.post(webhook_url, headers=headers, json={"text": message})
    return response.status_code

# Scheduled Task - Daily reminders
@celery.task
def send_daily_reminders():
    for influencer in influencers:
        if influencer['has_pending_ad_request']:
            send_email(
                'Daily Reminder',
                'Please visit/accept the ad request or checkout the public ad requests.',
                influencer['email']
            )
            # Optionally send Google Chat message
            # send_google_chat_message(influencer['gchat_webhook'], 'Daily Reminder: ...')

# Scheduled Task - Monthly Activity Report
@celery.task
def send_monthly_activity_report():
    for sponsor in sponsors:
        # Example report generation
        report = """
        Campaign Details:
        - Campaigns done: 10
        - Growth in sales: 20%
        - Budget used: $1000
        - Budget remaining: $500
        """
        send_email(
            'Monthly Activity Report',
            report,
            sponsor['email']
        )

# User Triggered Async Job - Export as CSV
@celery.task
def export_campaigns_to_csv(user_id):
    campaigns = [{'description': 'Ad Campaign 1', 'start_date': '2023-01-01', 'end_date': '2023-01-10', 'budget': 100, 'visibility': 'public', 'goals': 'Increase sales'}]
    file_path = f'/tmp/campaigns_{user_id}.csv'
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Description', 'Start Date', 'End Date', 'Budget', 'Visibility', 'Goals'])
        for campaign in campaigns:
            writer.writerow([campaign['description'], campaign['start_date'], campaign['end_date'], campaign['budget'], campaign['visibility'], campaign['goals']])
    
    # Send email notification (example)
    send_email(
        'Your Campaigns Export',
        f'Your campaigns have been exported and saved to {file_path}.',
        'user@example.com'
    )

    return file_path

# Celery Beat Schedule
celery.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'send_daily_reminders',
        'schedule': crontab(hour=18, minute=0),  # Adjust the time as needed
    },
    'send-monthly-activity-report': {
        'task': 'send_monthly_activity_report',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),
    },
}

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=18, minute=0), send_daily_reminders.s(), name='Daily Reminders')
    sender.add_periodic_task(crontab(day_of_month=1, hour=0, minute=0), send_monthly_activity_report.s(), name='Monthly Activity Report')

@app.route('/export_csv', methods=['POST'])
def export_csv():
    user_id = request.json['user_id']
    export_campaigns_to_csv.delay(user_id)
    return jsonify({"message": "Export started"}), 202

if __name__ == '__main__':
    app.run(debug=True)
