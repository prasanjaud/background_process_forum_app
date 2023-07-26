import mysql

from helper.db_cofig import db

cursor = db.cursor(dictionary=True)

def getAllUsers():
    try:
        query = "SELECT * FROM admin_users"
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)

    except mysql.connector.Error as error:
        print(f"Error: {error}")

    finally:
        cursor.close()
        db.close()

def updateTasks(taskName, campaignID, status):
    try:
        query = "UPDATE tasks_of_campaign SET status = %s WHERE task_name = %s AND campaign_id = %s"
        data = (status, taskName, campaignID)
        cursor.execute(query, data)

        result = db.commit()
        return "success"

    except mysql.connector.Error as error:
        print(f"Error: {error}")
        return "bad"

def getAllNewEmails():
    try:
        query = "SELECT * FROM email_list WHERE status = 'NEW' ORDER BY id DESC"
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    except mysql.connector.Error as error:
        print(f"Error: {error}")

def updateEmailStatus(email, status):
    try:
        query = "UPDATE email_list SET status = %s WHERE email = %s"
        data = (status, email)
        cursor.execute(query, data)
        # return result
        result = db.commit()
        return "success"

    except mysql.connector.Error as error:
        print(f"Error: {error}")
        return "bad"

def saveNewUser(email_value, username_value, password_value, campaign_id):
    try:
        query = "INSERT INTO wordpress_users (email, username, password, campaign_id) VALUES (%s, %s, %s, %s)"
        data = (email_value, username_value, password_value, campaign_id)
        cursor.execute(query, data)
        db.commit()
        inserted_id = cursor.lastrowid
        print("User ID:", inserted_id)
        # return result
        return inserted_id

    except mysql.connector.Error as error:
        print(f"Error: {error}")

def getUserDetailsByCampaign(campaignID):
    cursor = db.cursor(dictionary=True)
    try:
        query = "SELECT * FROM wordpress_users WHERE campaign_id= %s"
        cursor.execute(query, (campaignID,))
        data = cursor.fetchone()
        print(data)
        return data

    except mysql.connector.Error as error:
        print(f"Error: {error}")

def getCampaignDetailsQuery(campaign_id):
    cursor = db.cursor(dictionary=True)
    try:
        query = "SELECT * FROM campaigns WHERE id = %s"
        cursor.execute(query, (campaign_id,))
        data = cursor.fetchone()
        return data

    except mysql.connector.Error as error:
        print(f"Error: {error}")


def getGroupsAllContents(groupId):
    cursor = db.cursor(dictionary=True)
    try:
        query = f"SELECT * FROM contents WHERE content_group_id= {groupId}"
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        return data

    except mysql.connector.Error as error:
        print(f"Error: {error}")