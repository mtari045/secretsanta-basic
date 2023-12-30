
import random
import smtplib
import logging
import re
from datetime import datetime

#from seperate python file containing strings for email info
from email_password import EMAIL
from email_password import PASSWORD

#constants 
DONE = 'done'
ENCODING = 'utf-8'

#validity check functions 
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_date(date, format='%B %d @ %I:%M %p'):
    try:
        datetime.strptime(date, format)
        return True
    except ValueError:
        return False
 
 #function to generate secret santa pairings 
def generate_secret_santa(names):
    participants = names.copy()
    random.shuffle(participants)
    
    pairings = []
    for i in range(len(participants)):
        giver = participants[i]
        receiver = participants[(i + 1) % len(participants)]
        pairings.append((giver, receiver))
    
    return pairings

#function to send the emails to particpants 
def send_email(receiver_email, recipient_name,event_datetime ):
    subject = f"Your Secret Santa Assignment is Here, {recipient_name}!"
    message = (
        f"Hi {recipient_name},\n\n"
        f"Exciting news, you're {recipient_name}'s Secret Santa! "
        f"Time to spread some holiday cheer. Keep it under wraps until our event on {event_datetime}.\n\n"
        "Happy gifting!"
    )
    text = f"Subject: {subject}\n\n{message}"
    text = text.encode(ENCODING)
    try:
        #connecting to the SMTP server + sending the email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail("myra.s.tariq@gmail.com", receiver_email, text)
        server.quit()
        logging.info("Email has been sent to participants")
    except Exception as e:
        # gogging  error if  email fails
        logging.error(f"Failed to send email: {str(e)}")

#function to get participants (name + email) from user
def get_participants():
    participants = []
    while True:
        name = input("Enter participant's name (or type 'done' to finish): ")
        if name.lower() == DONE:
            break

        email = input("Enter participant's email: ")
        
        while not is_valid_email(email):
            print("invalid email address")
            email = input("Enter participant's email: ")

        participants.append((name, email))

    return participants

 #main function 
def main():
    participants = get_participants()

    if len(participants) < 2:
        print("you need at least two participants to do a Secret Santa.")
    elif len(participants) % 2 != 0:
        print("you need an even number of participants for Secret Santa.")
    else:
        #getting the date/time of the event for the email 
        event_datetime = input("enter the date and time of the event (e.g., December 25 @ 7:00 PM): ")
        while not is_valid_date(event_datetime):
            print("Invalid date format. Please enter a valid date.")
            event_datetime = input("Enter the date and time of the event (e.g., December 25 @ 7:00 PM): ")
        
        #generating secret santa pairings
        pairings = generate_secret_santa(participants)
        print("\nSecret Santa Pairings:")
        for (giver_name, giver_email), (receiver_name, receiver_email) in pairings:
            print(f"{giver_name} -> {receiver_name}")
            send_email(receiver_email, receiver_name,event_datetime)

if __name__ == "__main__":
    main()
