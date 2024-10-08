import time
from celery import shared_task, Task
from flask_mail import Mail, Message
from .. import global_vars as gv
from ..server_db_manager import DB_Manager as DB_Manager
from collections import Counter
from datetime import datetime
import pytz

sender_id = ""

@shared_task(ignore_result=False)
def sponsor_export(id) -> str:
    d = [id]
    c = []

    name = DB_Manager().QueryModelName(id)
    email = DB_Manager().QueryModelEmail(id)
    d.append(name[0][0])
    d.append(email[0][0])
    
    campaigns = DB_Manager().QueryCampaignBySID(id)
    for j in range(len(campaigns[0])):
        
        ads  = DB_Manager().QueryLastAdStatus(campaigns[0][j])
        ads = ads[0] if len(ads) > 0 else []
        a = []
        for k in ads:
            a.append(DB_Manager().QueryAdRequestByAID(k)[5][0])
        a = Counter(a)
        a = [a['Approved'], a['Rejected'], a['PENDING']]
        tl = []
        for i in range(len(campaigns)):
            tl.append(campaigns[i][j])
        tl[3] = tl[3].replace(",", ".")
        tl[4] = datetime.utcfromtimestamp(tl[4]).replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        tl[5] = datetime.utcfromtimestamp(tl[5]).replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        c.append([tl, a])
    d.append(c)
    print(d)


    user_id, username, email, campaigns = d

    # Column headers for campaigns
    campaign_headers = ['Campaign ID', 'Sponsor ID', 'Campaign Name', 'Campaign Description', 'Start Date', 'End Date', 'Budget', 'Visibility', 'Goals', 'Flagged', 'Approved', 'Rejected', 'Pending']

    # Prepare CSV rows for campaigns
    rows = []
    for campaign in campaigns:
        campaign_details, metrics = campaign
        row = campaign_details + metrics
        rows.append(row)

    # Create CSV content
    csv_content = f'User ID, {user_id}\nUsername, {username}\nEmail, {email}\n\n'
    csv_content += ','.join(campaign_headers) + '\n'
    for row in rows:
        csv_content += ','.join(map(str, row)) + '\n'

    print(csv_content)

    return csv_content

# scheduled tasks
@shared_task
def daily_task() -> None:
    try:
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
                        sender = sender_id, 
                        recipients = list(IIDs)
                    ) 
        msg.body = """Hello,
                    You have pending sponsorships. Please check you'r portal inbox for more details.
                    """
        gv.mail.send(msg) 
    except Exception as e:
        print(e)

@shared_task
def monthly_task() -> None:
    try:
        SIDs = DB_Manager().QueryModelSponsorIDs()[0]
        details = []
        for i in SIDs:
            d = [i]
            c = []

            name = DB_Manager().QueryModelName(i)
            email = DB_Manager().QueryModelEmail(i)
            d.append(name[0][0])
            d.append(email[0][0])
            
            campaigns = DB_Manager().QueryCampaignBySID(i)
            for j in range(len(campaigns[0])):
                
                ads  = DB_Manager().QueryLastAdStatus(campaigns[0][j])
                ads = ads[0] if len(ads) > 0 else []
                a = []
                for k in ads:
                    a.append(DB_Manager().QueryAdRequestByAID(k)[5][0])
                a = Counter(a)
                a = [a['Approved'], a['Rejected'], a['PENDING']]
                c.append([campaigns[0][j], campaigns[2][j], a])
            d.append(c)
            
            details.append(d)
        print(details)

        for det in details:
            # create a html template for entering data 
            html = f"""<html>
                        <head>
                        <style>
                        table {{
                        font-family: arial, sans-serif;
                        border-collapse: collapse;
                        width: 100%;
                        }}
                        td, th {{
                        border: 1px solid
                        text-align: left;
                        padding: 8px;
                        }}
                        tr:nth-child(even) {{
                        background-color: #dddddd;
                        }}
                        </style>
                        </head>
                        <body>
                        <h2>Monthly Report</h2>
                        <h3>{det[1]} ({det[0]})</h3>
                        <h3>Email: {det[2]}</h3>
                        <table>
                        <tr>
                        <th>Campaign ID</th>
                        <th>Campaign Name</th>
                        <th>Approved</th>
                        <th>Rejected</th>
                        <th>PENDING</th>
                        </tr>"""
            for c in det[3]:
                html += f"""<tr>
                            <td>{c[0]}</td>
                            <td>{c[1]}</td>
                            <td>{c[2][0]}</td>
                            <td>{c[2][1]}</td>
                            <td>{c[2][2]}</td>
                            </tr>"""
            html += """</table>
                        </body>
                        </html>"""
            # send email
            msg = Message( 
                        'Monthly Report',
                        sender = sender_id,
                        recipients = [det[2]]
                    )
            msg.html = html
            gv.mail.send(msg)
    except Exception as e:
        print(e)