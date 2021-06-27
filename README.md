# MySQL to MongoDB Migration Tool (With Celery(Multiworker) and Docker)
With this function, you can migrate your MySQL data tables to your MongoDB data tables(collections)
The process is simple, just have your database and tables set up for both mysql and mongodb.
You can export your datas from your local MySQL server and import to the docker MySQL server.

For this example, we will be using the databases and tables i created for mysql, called called testdatabase.sql that i imported to the mysql server running inside docker.
For mongodb, you will have to put in your mongodb connnection link inside the "tasks.py" script, at line 26.

<br>

## Example MySQL Database Creation(Importing)

1) The example database file i exported is located in:     C:\Users\USER\Desktop\MySQL-to-Mongo\testdatabase.sql

2) With this command below, you can import databases to our mysql server running in docker. The path to your database could be different. Cd into the folder of your sql file, then use this command:

   docker exec -i mysql-to-mongo_mysql_db_1 mysql -uroot -proot testdatabase < testdatabase.sql

<br>

## Example of MongoDB

1) Put in your mongodb connnection link inside the "tasks.py" script, at line 26.

<br>

## Connecting to Tools
1) After composing, and setting the database, open a terminal window, paste the command below to connect the program inside container.

   docker exec -it  mysql-to-mongo_python_app_1 /bin/bash

2) Type in "python" to the terminal. (Without "")

3) Type in "from tasks import *" to the terminal (Without "")

3) If you want to migrate without workers, just use the function
   
   transfer_data(mysqlDatabaseName,mysqlTableName,mongoDatabaseName, mongoTableName)

   example: transfer_data("testdatabase","testtable","testdatabase", "testtable")

<br>

## Celery Task (Multiworker)
1) Open another terminal window, independent from the window that we are using our python console.
Type the following code:

   docker exec -it  mysql-to-mongo_python_app_1 /bin/bash

2) Then use this code at the same terminal

   celery -A tasks worker --loglevel=INFO

<br>

This will create a terminal window that you can check your worker orders. Keep this terminal up for watching the process of workers.

<br>

## How to Add Migration Task as Celery Worker
After you set the celery terminal mentioned above, just type the function, add .delay and send the parameters, this will create a worker for our function that will run inside celery, you can check the worker's status at the terminal, mentioned at Celery Task section above.

Example:

transfer_datas.delay("testdatabase","testtable","testdatabase","testtable")


