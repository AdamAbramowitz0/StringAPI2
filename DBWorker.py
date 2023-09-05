import mysql.connector
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, create_engine,ForeignKey,exists
import sys
from random import *
engine=create_engine("", echo = True)
meta = MetaData()
#engine.connect()

companies = Table(
    'companies',meta,
    Column('id', Integer, primary_key=True),

    Column('name', String(50)),
    Column('username', String(50)),
    Column('password', String(50))
)

instance = Table(
    'instance',meta,
    Column('id', Integer, primary_key=True),

    Column('foreginID', Integer()),

    Column('instanceName', String(50)),
    Column('apiKey', Integer()),
    Column('AmountOwed', Integer)
)

user = Table(
    'Users',meta,
    Column('id', Integer, primary_key=True),
    Column('foreginID', Integer()),
    Column('name', String(50)),
    Column('reccomenderID', Integer()), #MAKE SURE RECCOMENDED FROM RIGHT COMPANY!
    Column('points', Integer())


)

codes = Table(
    'Codes',meta,
    Column('foreginID', Integer()),
    Column('Code',Integer())
)

meta.create_all(engine)


def addCompany(compName ,password, username ):
    engine.connect().execute(companies.insert().values(name=compName, password=password, username=username))
def addInstance(instanceName, compName):#too what company id
    y = companies.query.filter_by(companies.name == compName).first()

    engine.connect().execute(instance.insert().values(foreignID = y.id, instanceName=instanceName, apiKey = random(1000000000000000,999999999999999), AmountOwed = 0.00 ))

def addUser(NameOfUser, InstanceName,code): #and increment other users #to what company id to what instance id
    #######WORKHERE
    y = instance.select().where(instance.instanceName==InstanceName)
    if user.select().where(user.reccomenderID==recID).exists():
        z=user.select().where(user.reccomenderID==recID)
        engine.connect().execute(z.update().values(points=(z.points+1)))
    engine.connect().execute(user.insert().values(foreignID = y.id, name=NameOfUser, reccomenderID = z.id, points = ))

def addUser(NameOfUser, InstanceName):  # and increment other users #to what company id to what instance id
        #######WORKHERE
    y = instance.select().where(instance.instanceName == InstanceName)
    if user.select().where(user.reccomenderID == recID).exists():
        z = user.select().where(user.reccomenderID == recID)
        engine.connect().execute(z.update().values(points=(z.points + 1)))
    engine.connect().execute(user.insert().values(foreignID=y.id, name=NameOfUser, reccomenderID=z.id, points=))

#def getPoints():

#def removePoints():


#TODO: USE FAKE NAMES for testing!

#Q1 = "CREATE TABLE Users (id int PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), passwd VARCHAR(50))"
#Q2 = "CREATE TABLE Scores (userId int PRIMARY KEY, FOREIGN KEY(userId) " \
     #"REFERENCES Users(id), game1 int DEFAULT 0, game2 int DEFAULT 0)"
#mycursor = db.cursor()
#mycursor.execute(createACompanyTable)
#mycursor.execute("DROP TABLE Person")
#mycursor.execute(Q1)
#mycursor.execute(Q2)

#def addNewCompany(CompanyName, Username, Password):

    #mycursor.execute("INSERT INTO companies (CompanyName, Username, Password) VALUES (%s,%s,%s)", (CompanyName, Username, Password))
    #db.commit()

#def addNewInstance(CompanyName):
    #x = mycursor.execute("SELECT id FROM Companies WHERE CompanyName = (%s)"(CompanyName))


#mycursor.execute("SELECT * FROM companies")
#for x in mycursor:
    #print(x)
##mycursor.execute("DESCRIBE Test")
#print(mycursor.fetchone())
#mycursor.execute("ALTER TABLE Test ADD COLUMN food VARCHAR(50) NOT NULL")
#mycursor.execute("DROP TABLE test")
#mycursor.execute("CREATE TABLE Test (name varchar(50) NOT NULL, created datetime NOT NULL, gender ENUM('M','F','O') NOT NULL, id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
#mycursor.execute("INSERT INTO Test (name, created, gender) VALUES (%s,%s,%s)", ("TIMA", datetime.now(), "M"))
#mycursor.execute("INSERT INTO Test (name, created, gender) VALUES (%s,%s,%s)", ("JAN", datetime.now(), "F"))
#db.commit()
#mycursor.execute("SELECT name, id FROM Test WHERE gender = 'F' ORDER BY id DESC")
#for x in mycursor:
#print(x)
