import os
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib

def catmailbotPythonFunction(request):
    # Define the API endpoints
    cat_url = 'https://api.thecatapi.com/v1/images/search?api_key=live_T1sTvcdpPNHgTXC911q5S0sKW6N74y6Sxsb781UxBYFMSOGWvQZfpnnIl0n3YoXF'
    kanye_url = 'https://api.kanye.rest'

    # Send a GET request to the cat API
    response = requests.get(cat_url)

    if response.status_code == 200:
        data = response.json()
        image_url = data[0]['url']

        # Download the image
        image_response = requests.get(image_url)

        # Define the directory to save the image
        save_directory = "/tmp"  # Using /tmp directory as Cloud Function has limited writable space

        # Generate filename with datetime
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cat_image_{current_time}.jpg"

        # Save the image to the specified directory
        save_path = os.path.join(save_directory, filename)
        with open(save_path, "wb") as f:
            f.write(image_response.content)

        print("Image downloaded and saved to", save_path)
    else:
        print("Failed to retrieve image from the API")
        return "Failed to retrieve image", 500

    # Send a GET request to the Kanye API
    response = requests.get(kanye_url)

    if response.status_code == 200:
        data = response.json()
        quote = data['quote']
        print(quote)
    else:
        print("Failed to retrieve quote from the API")
        return "Failed to retrieve quote", 500

    # Email configuration
    sender = 'daracorr5@gmail.com'
    receivers = ['daracorr5@gmail.com']

    message = f"""

    \"{quote}\"
    \n Sent by daramailbot
    """

    gmail_user = "daracorr5@gmail.com"
    gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')  # Use environment variable for security
    sent_from = "daracorr5@gmail.com"
    sent_to = "daracorr5@gmail.com"
    email_text = message

    msg = MIMEMultipart()
    msg['From'] = sent_from
    msg['To'] = sent_to
    msg['Subject'] = 'Cat'

    msg.attach(MIMEText(email_text, 'plain'))

    # Attachment handling
    with open(save_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        msg.attach(part)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(sent_from, sent_to, msg.as_string())
        server.close()

        print('Email sent!')
    except Exception as e:
        print("Error: %s!\n\n" % e)
        return "Error sending email", 500

    return "Script executed successfully", 200
