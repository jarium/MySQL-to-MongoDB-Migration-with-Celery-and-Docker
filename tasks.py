from celery import Celery
from pymongo import MongoClient
import mysql.connector
import pandas as pd
import numpy as np

#Celery Workers
celery = Celery(
    'tasks',
     broker = 'pyamqp://guest@rabbitmq//',
     backend = 'db+sqlite:///db.sqlite3'
)

""" This is a function that can be used to migrate MySQL data tables to MongoDB as Mongo Collections. Happy migrating! -Efe Büyük """


# Mongodb upsert function
def upsert_to_mongo(data,collection):
    collection.update_one(data, {'$setOnInsert': data}, upsert=True)

#The main function
@celery.task
def transfer_datas(mysqlDbName,mysqlTableName,mongoDbName,mongoTableName):

  # Mongodb Database
  cluster = MongoClient("Your MongoDB connection link here") #Put your MongoDB connection link as a string inside the brackets.
  mongodb = cluster[mongoDbName]
  collection = mongodb[mongoTableName]

  # MySQL Database
  mysqldb = mysql.connector.connect(
        host="mysql_db",
        user="root",
        password="root",
        database=(mysqlDbName)
    )

  #Selecting the datas and columns from MySQL
  mycursor = mysqldb.cursor()
  mycursor.execute("SELECT * FROM {}".format(mysqlTableName))
  mysqldatas = mycursor.fetchall()
  mycursor.execute("SHOW COLUMNS FROM {}".format(mysqlTableName))
  columns = mycursor.fetchall()
  thecolumns = []
  for x in columns:
      thecolumns.append(x[0])

  #Transfering MySQL data to json like dict format in a list, using numpy and pandas
  dataArray = np.array(mysqldatas)
  dataFrame = pd.DataFrame(dataArray, columns=thecolumns)
  datas = dataFrame.to_dict(orient = 'records')

  #Importing the datas to MongoDB if they are not exist
  for data in datas:
   upsert_to_mongo(data, collection)


#Using the function
"""On this example of migration from MySQL to Mongodb, i used 'testdatabase' as my database name and 'testtable'
as my table name."""

#transfer_datas("testdatabase","testtable","testdatabase","testtable")

#Using the function with Celery workers
"""On this example of migration from MySQL to Mongodb, i used 'testdatabase' as my database name and 'testtable2'
as my table name. Writing .delay after the function is for sending the function to Celery workers to process them in the background."""

#transfer_datas.delay('testdatabase','testtable2','testdatabase','testtable2')

