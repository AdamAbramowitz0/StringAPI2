from twilio.rest import Client

class Validation:

    global x
    x={1:"yo"}

    def checkEmail(num, addr1):
        number = int(num)
        auth_token = ''
        account_sid = ''
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body="Thank you for signing up for the API, in order to validate your address, please click on the link below." \
                  "If you did not request this email, disregard this email. Thanks!:" + str(number),
            from_='',
            to=addr1
        )
        x[number]=addr1

        print(message.sid)

    def checkResponse(num, addr1):
        number=int(num)
        print(number)
        print(addr1)


        if number in x and x[number] == addr1:
            print("hit")
            print(x)
            x.pop(number)
            print(x)
            return True
        else:
            return False

#send them a codes
