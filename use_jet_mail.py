from mailjet_rest import Client

import re

api_key = 'your_api_key'
api_secret = 'your_api_secret'


# Make a regular expression
# for validating an Email
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


# Define a function for
# for validating an Email


def validate_email(email):
    # pass the regular expression
    # and the string in search() method
    if re.search(regex, email):
        # print("Valid Email")
        return True

    else:
        # print("Invalid Email")
        return False


def send_email_to_employee(name, lname, email_address, subject, message):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
      'Messages': [
        {
          "From": {
            "Email": "your email address",
            "Name": "HT Employment System"
          },
          "To": [
            {
              "Email": f"{email_address}",
              "Name": f"{name} {lname}"
            }
          ],
          "Subject": f"{subject}",
          "TextPart": "Greetings",
          "HTMLPart": f"<h5>Dear {name} {lname}!</h5><br /><p>{message}</p>",
          "CustomID": "AppGettingStartedTest"
        }
      ]
    }
    result = mailjet.send.create(data=data)
    #print(result.status_code)
    # print (result.json())
