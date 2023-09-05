import json
from company import company
from user import user


class JSONWorker:

    def checkIfCompany(email, password):
        with open("users.json","r+") as f:
            data=json.load(f)
            for x in range(0, len(data['creds'])):
                if data['creds'][email]==password:
                    return True

            return False

    def addCompanyCreds(email, password):
        with open("users.json", "r+") as f:
            data = json.load(f)
            for x in range(0,len(data['creds'])):
                if data['creds'][email] == password:

                    return "INVALID PASSWORD OR USERNAME, PLEASE REMAKE! IF ERROR, CONTACT ME!"
            data['creds'][email] = password
            return True
#ValueGood, numPoints,
    def addnewcompany(company):
        print("hit")
        comp = company
        with open("info.json", "r+") as f:
            data = json.load(f)
            dit = {
                'name': comp.name,
                'apiKey': comp.apiKey,
                'pointsReq': comp.pointsReq,
                'numPoints' : comp.numPoints,
                'ValueGood' : comp.ValueGood,
                'amountOwed': comp.amountOwed,
                'email': comp.email,
                'password': comp.passwrod,
                'users': comp.users
            }
            data['companies'].append(dit)
            f.seek(0)
            json.dump(data, f, indent=4)

    def addnewpersonincompany(q, compObj, refererName):

        with open("info.json", "r+") as f:
            data = json.load(f)


            for x in range(0, len(data['companies'])):
                y = data['companies'][x]
                print('hitt')
                z = y['name']
                print(z +"YOO")
                if z == (compObj.name):
                    if y['apiKey'] != compObj.apiKey:
                        return "TRAITOR"
                    print("HITT")
                    newUser = user(q, 0, 0)
                    print()
                    ditt = {
                        'name': newUser.name,
                        'currPoints': newUser.currPoints,

                        'secondDegree': newUser.secondDegree,

                    }
                    data['companies'][x]['users'].append(ditt)
                    #
                    for z in range(0, len(data['companies'][x]['users'])):
                        if data['companies'][x]['users'][z]['name'] == refererName:
                            data['companies'][x]['users'][z]['currPoints']+=1
                            refererTwo = data['companies'][x]['users'][z]['secondDegree']
                            for q in range(0, len(data['companies'][x]['users'])):
                                if data['companies'][x]['users'][q]['name'] == refererTwo:
                                    data['companies'][x]['users'][q]['currPoints']+=1

                f.seek(0)
                json.dump(data, f, indent=4)
                return "sucess"

    def addPoint(compName,usersName,apiKey):

        with open("info.json", "r+") as f:

            data = json.load(f)

            for x in range(0, len(data['companies'])):

                if data['companies'][x]['name'] == compName:
                    if data['companies'][x]['apiKey'] != apiKey:
                        return "TRAITOR"
                    for y in range(0, len(data['companies'][x]['users'])):
                        print(data['companies'][x]['users'][y])

                        if data['companies'][x]['users'][y]['name'] == usersName:

                            data['companies'][x]['users'][y]['currPoints'] = \
                                data['companies'][x]['users'][y]['currPoints']+1

                            f.seek(0)
                            json.dump(data, f, indent=4)
                            return "sucess"

    def removePoint(compName,usersName,apiKey):
        with open("info.json", "r+") as f:
            data = json.load(f)
            for x in range(0, len(data['companies'])):
                if data['companies'][x]['name'] == compName:
                    if data['companies'][x]['apiKey'] != apiKey:
                        return "TRAITOR"
                    for y in range(0, len(data['companies'][x]['users'])):
                        if data['companies'][x]['users'][y]['name'] == usersName and \
                                data['companies'][x]['users'][y]['currPoints'] != 0:
                            data['companies'][x]['users'][y]['currPoints'] \
                                = data['companies'][x]['users'][y]['currPoints']-1
                            print("HITTTTTT")
                            f.seek(0)
                            json.dump(data, f, indent=4)

    def getPoint(compName, usersName,apiKey):
        with open("info.json", "r+") as f:

            data = json.load(f)

            for x in range(0, len(data['companies'])):

                if data['companies'][x]['name'] == compName:
                    if data['companies'][x]['apiKey'] != apiKey:
                        return "TRAITOR"
                    for y in range(0, len(data['companies'][x]['users'])):
                        print(data['companies'][x]['users'][y])

                        if data['companies'][x]['users'][y]['name'] == usersName:
                            return data['companies'][x]['users'][y]['currPoints']





    #    with open("info.json", "r+") as f:
    #        data = json.load(f)
    #        x=data[company.name]
    #       y=x[user.name]
    #       y['currPoints'] =

    # def getAmountOwed(self):
