import json


import pika
from flask import Flask, render_template

# app = Flask(__name__)
from campaign_process.process import start_campaign, start_campaign_test
from campaign_process.wordpress import wordpress_register_account, wordpress_remove_default_post, \
    wordpress_change_title, post_publish_wordpress
from helper.campaign_sql_queries import getAllNewEmails, updateTasks

logs = []

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the 'bk_sample_1' queue to ensure it exists
channel.queue_declare(queue='bk_multi_prompt', durable=True)

# start_campaign_test(92)
# data = getAllNewEmails()
# print(data)
def callback(ch, method, properties, body):
    message_data = body.decode()
    task_name = json.loads(message_data).get('task_name')
    print(task_name)
    logs.append(f"Task name: {task_name}")

    if task_name == 'start_campaign':
        start_campaign(message_data)

    elif task_name == "WORDPRESS_ACCOUNT_REGISTER":
        campaign_id = json.loads(message_data).get('campaign_id')
        res = wordpress_register_account(campaign_id)
        if res == "Done":
            updateTasks(task_name, campaign_id, "Done")
        else:
            updateTasks(task_name, campaign_id, "Fail")

    elif task_name == "WORDPRESS_REMOVE_DEFAULT_POST":
        campaign_id = json.loads(message_data).get('campaign_id')
        res2 = wordpress_remove_default_post(campaign_id)
        if res2 == "Done":
            updateTasks("WORDPRESS_REMOVE_DEFAULT_POST", campaign_id, "Done")
        else:
            updateTasks("WORDPRESS_REMOVE_DEFAULT_POST", campaign_id, "Fail")

    elif task_name == "WORDPRESS_CHANGE_TITLE":
        campaign_id = json.loads(message_data).get('campaign_id')
        res3 = wordpress_change_title(campaign_id)
        if res3 == "Done":
            updateTasks("WORDPRESS_CHANGE_TITLE", campaign_id, "Done")
        else:
            updateTasks("WORDPRESS_CHANGE_TITLE", campaign_id, "Fail")

    elif task_name == "PUBLISH_WORDPRESS_CONTENT_POST_1":
        campaign_id = json.loads(message_data).get('campaign_id')
        res4 = post_publish_wordpress(campaign_id)
        if res4 == "Done":
            updateTasks("PUBLISH_WORDPRESS_CONTENT_POST_1", campaign_id, "Done")
        else:
            updateTasks("PUBLISH_WORDPRESS_CONTENT_POST_1", campaign_id, "Fail")
    else:
        print(f"Unknown message type: {task_name}")

    print(f"Received and processed: {body.decode()}")


# Consume messages from the 'bk_sample_1' queue and call the callback function
channel.basic_consume(queue='bk_multi_prompt', on_message_callback=callback, auto_ack=True)

# def start_flask_app():
#     def show_logs():
#         return render_template('logs.html', logs=logs)
#
#     app.run(host='localhost', port=5001)

print('Worker is waiting for messages. To exit, press CTRL+C')

# import threading
#
# flask_thread = threading.Thread(target=start_flask_app)
# flask_thread.start()
#
channel.start_consuming()