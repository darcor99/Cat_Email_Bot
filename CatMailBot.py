import requests
import os
from datetime import datetime
from google.colab import userdata


# Define the API endpoint
#url = "https://api.thecatapi.com/v1/images/0XYvRd7oD"
url = 'https://api.thecatapi.com/v1/images/search?api_key=live_T1sTvcdpPNHgTXC911q5S0sKW6N74y6Sxsb781UxBYFMSOGWvQZfpnnIl0n3YoXF'


# Send a GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Extract the image URL from the response
    data = response.json()
    print(data)
    image_url = data[0]['url']

    # Download the image
    image_response = requests.get(image_url)

    # Define the directory to save the image
    save_directory = "/content/drive/MyDrive/API-downloads"

    # Create the directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)

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



url = 'https://api.kanye.rest'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    quote = data['quote']
    print(quote)
else:
    print("Failed to retrieve quote from the API")



######################################################




import smtplib
from google.colab import userdata
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

sender = 'daracorr5@gmail.com'
receivers = ['daracorr5@gmail.com']

message = f"""From: daramailbot \n

{quote}
\n Sent by mailbot
"""

gmail_user = "daracorr5@gmail.com"
gmail_app_password = userdata.get('my_gmail_app_pw')
sent_from = "daracorr5@gmail.com"
sent_to = "daracorr5@gmail.com"#"seantobin1912@gmail.com"
email_text = message

msg = MIMEMultipart()
msg['From'] = sent_from
msg['To'] = sent_to
msg['Subject'] = 'Cat'

msg.attach(MIMEText(email_text, 'plain'))

# Attachment handling
filename = save_path  # Replace with your filename
attachment = open(filename, "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_app_password)
    server.sendmail(sent_from, sent_to, msg.as_string())
    server.close()

    print('Email sent!')
except Exception as exception:
    print("Error: %s!\n\n" % exception)