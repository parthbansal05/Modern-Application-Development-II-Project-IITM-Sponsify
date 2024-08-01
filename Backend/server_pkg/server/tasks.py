import time
from celery import shared_task, Task
from flask_mail import Mail, Message
from .. import global_vars as gv
from ..server_db_manager import DB_Manager as DB_Manager

@shared_task()
def sponsor_export() -> None:
    msg = Message( 
                    'Hello', 
                    sender ='', 
                    recipients = [''] 
                ) 
    msg.body = 'Hello Flask message sent from Flask-Mail'
    gv.mail.send(msg) 

# scheduled tasks
@shared_task
def daily_task() -> None:
    SIDs = DB_Manager().QueryModelSponsorIDs()[0]
    IIDs = set()
    for i in SIDs:
        lc = DB_Manager().QuerySponsorInBoxChatOverView(i)
        for j in range(len(lc[5])):
            if lc[5][j] == 'PENDING' or lc[11][j] == 'False':
                IIDs.add(DB_Manager().QueryModelEmail(lc[3][j])[0][0])
    print(IIDs)
    msg = Message( 
                    'Pending Sponsorship',
                    sender ='', 
                    recipients = list(IIDs)
                ) 
    msg.body = """Hello,
                You have pending sponsorships. Please check you'r portal inbox for more details.
                """
    gv.mail.send(msg) 

@shared_task
def monthly_task() -> None:
    
    pass
