import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="db_forum_app"

    # host="localhost",
    # user="root",
    # password="Kandy123",
    # database="db_forum_app"
)

cursor = db.cursor()