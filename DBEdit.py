from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, create_engine,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from random import *
from sqlalchemy.orm import sessionmaker, relationship

name = ""
engine=create_engine(name)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
meta = MetaData()

class companies(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    username = Column(String(50))
    password = Column(String(50))
    amountOwedInCents = Column(Integer)
    customerID = Column(String(100))
    subscriptionID = Column(String(100))
    daysFree = Column(Integer)

class instances(Base):
    __tablename__ = 'instances'
    id = Column(Integer, primary_key=True)
    instanceName = Column(String(50))
    apiKey = Column(Integer)
    companyID = Column(Integer)


class users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    recomenderID = Column(Integer)
    points = Column(Integer)
    instanceID = Column(Integer)

class codes(Base):
    __tablename__ = 'codes'
    id = Column(Integer, primary_key=True)
    code = Column(Integer)
    userID = Column(Integer)

Base.metadata.create_all(engine) #was deleted, meta thing
session.close()

def getCompName(username,password):
    session=Session()
    z = session.query(companies).filter(companies.username==username,companies.password==password).first().name
    session.close()
    return z
def getAPIKey(username,password):
    z={}
    session=Session()
    x=0
    q = session.query(companies).filter(companies.username == username, companies.password == password).first().id
    p=True
    while p == True:
        try:
            if session.query(instances).filter(instances.companyID==q).all()[x] is not None:
                z[session.query(instances).filter(instances.companyID == q).all()[x].instanceName]=session.query(instances).filter(instances.companyID == q).all()[x].apiKey
                x+=1
            else:
                p=False
        except Exception:
                print(Exception)
                p=False
    session.close()
    return z

def getReferrer(name, instanceName):
#get instance id, filter within the users for instnaceID and name. Save this. re do
    if name == None:
        return "error"
    session = Session()
    z=session.query(instances).filter(instances.instanceName==instanceName).first().id
    x=session.query(users).filter(users.name==name, users.instanceID == z).first().recomenderID
    if session.query(users).filter(users.id == x, users.instanceID == z).first() is not None:
        name = session.query(users).filter(users.id == x, users.instanceID == z).first().name
    else:
        name = "error"
    session.close()
    return name


def addCompany(name, username, password,customerID,subscriptionID,daysFree):
    session = Session()
    c = companies(name = name, username = username, password = password, amountOwedInCents = 0,customerID=customerID,subscriptionID=subscriptionID, daysFree=(daysFree+5))
    session.add(c)
    session.commit()
    session.close()

def getSubscriptionID(name):
    session=Session()

    z=session.query(companies).filter(companies.name==name).subscriptionID
    session.close()
    return z
def giveDaysFree(corpName): #20 now!?
    session=Session()
    if corpName == "error":
        return "error"
    r=session.query(companies).filter(companies.name==corpName).first().daysFree
    session.query(companies).filter(companies.name==corpName).update({companies.daysFree:r+15},synchronize_session=False)
    session.commit()
    session.close()
def transactionPrep():
    z={}
    x = 1;
    q = True
    session = Session()
    while(q):
        print("HIT")
        if session.query(companies).filter(companies.id == x).first() is not None:
            if session.query(companies).filter(companies.id == x).first().daysFree > 0:
                session.query(companies).filter(companies.id == x).update({companies.amountOwedInCents: 0},synchronize_session=False)
                r = session.query(companies).filter(companies.id == x).first().daysFree
                session.query(companies).filter(companies.id==x).update({companies.daysFree:r-1},synchronize_session=False)
            z[session.query(companies).filter(companies.id==x).first().amountOwedInCents] = session.query(companies).filter(companies.id==x).first().subscriptionID
            session.query(companies).filter(companies.id==x).update({companies.amountOwedInCents : 0}, synchronize_session=False)
            session.commit()
            x+=1
            q=True
        else:
            q=False
    session.close()
    return z


def addInstance(companyName, instanceName):
    session = Session()
    x = session.query(companies).filter(companies.name == companyName).first().id
    if session.query(instances).filter(instances.instanceName == instanceName, instances.companyID == x).first() is not None: #TODO test
        session.close()
        return "INSTANCE NAME IS TAKEN!"
    x = session.query(companies).filter(companies.name==companyName).first().id
    z=int((random()*10000000))
    i = instances(instanceName = instanceName, apiKey = z,companyID = x)
    session.add(i)
    session.commit()
    session.close()
    return "your api key is....." + str(z) + "WOHOO, keep this somewhere safe, I dont want to come and rescue you when you loose it..."

#addCompany(
#)
#addInstance(
#companyName="TEST", instanceName="Chirp" # was 
#)
print(getAPIKey("ahabramowitz@gmail.com","TEST"))
def addUser(instanceName, userName,code):
   session = Session()
   x = session.query(instances).filter(instances.instanceName == instanceName).first().id
   if session.query(users).filter(users.name==userName, users.instanceID == x).first() is not None: #TODO Test
       session.close()
       return "NAME IS TAKEN!"
   if int(code) != 0:
        x = session.query(instances).filter(instances.instanceName == instanceName).first().id

        r = session.query(codes).filter(codes.code == code).first().userID
        u = users(name=userName, recomenderID = r, points = 1, instanceID = x)
        session.query(users).filter(users.id == r).update({users.points:(users.points+1)}, synchronize_session=False)
        session.query(codes).filter(codes.code==code).update({codes.code:(random()*10000)}, synchronize_session=False)
        session.add(u)
        a = session.query(users).filter(users.name == userName).first().id
        c = codes(code=(random()*10000), userID=a)
        y = session.query(instances).filter(instances.instanceName == instanceName).first().companyID
        session.query(companies).filter(companies.id == y).update(
            {companies.amountOwedInCents: (companies.amountOwedInCents + 20)}, synchronize_session=False)
        session.add(c)
        session.commit()
        session.close()
        print("HIT")
   else:
       x = session.query(instances).filter(instances.instanceName == instanceName).first().id
       u = users(name=userName, points=0, instanceID=x)
       session.add(u)
       a = session.query(users).filter(users.name == userName).first().id
       c = codes(code=(random() * 10000), userID=a)
       print("Got here")
       session.add(c)
       session.commit()
       session.close()
       print("HIT2")


def getUserPoints(instanceName, userName):
    session = Session()
    instID = session.query(instances).filter(instances.instanceName == instanceName).first().id
    x = session.query(users).filter(users.name==userName, users.instanceID == instID).first().points
    print(x)
    session.close()
    return x
def changeUserPoints(instanceName, userName, numpts):
    session = Session()
    instID = session.query(instances).filter(instances.instanceName == instanceName).first().id
    x = session.query(users).filter(users.name == userName, users.instanceID == instID).update({users.points:(users.points+numpts)}, synchronize_session=False)
    session.commit()
    session.close()
    return "Complete"


def getCode(user,instanceName):
    session = Session()
    z = session.query(instances).filter(instances.instanceName==instanceName).first().id
    a = session.query(users).filter(users.name == user, users.instanceID==z).first().id
    try:

        x = session.query(codes).filter(codes.userID == a).first().code
        session.close()
        return x

    except Exception:
        session.close()
        return 0

def getCustomerID(compName):
    session=Session()
    a =session.query(companies).filter(companies.name==compName).first().customerID
    session.close()
    return a

def clearDB():
    session = Session()
    x = "LATER" #TODO:THIS
    session.close()

def checkAPIKey(apiKey,instanceName):
    session = Session()
    x = session.query(instances).filter(instances.instanceName==instanceName).first().apiKey

    y = int(apiKey)
    if x==y:
        session.close()
        print("HIIT")
        return True
    else:
        session.close()
        return False
def checkIfCompany(uName,pWord):
    session = Session()
    try:
        if session.query(companies).filter(companies.username == uName).first().password == pWord:
            session.close()
            return True
        else:
            session.close()
            return False
    except:
        session.close()
        return False

#q = session.query(mapped class)

#def changeName(id,newName):
    #session.query(Customers).get(id).name=newName
    #session.commit()
#changeName(1,"YOYOYO")

#def bulkUpdate(id):
    #session.query(Customers).filter(Customers.id == id).update({Customers.name:"Mr. " + Customers.name}, synchronize_session = False)
    #session.commit()
#bulkUpdate(1)

#def addCustomer(name):
    #c1 = Customers(name = name)
    #session.add(c1)
    #session.commit()


