import schedule
import time


def schedule_emails(data, prompt, send_time):
    schedule.every().day.at(send_time).do(send_custom_emails, data=data, prompt=prompt)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)