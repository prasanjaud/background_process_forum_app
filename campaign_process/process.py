import json

from campaign_process.wordpress import wordpress_register_account, wordpress_remove_default_post, wordpress_change_title
from helper.campaign_sql_queries import updateTasks


def start_campaign(message_data):
    campaign_id = json.loads(message_data).get('campaign_id')
    print(campaign_id, "idx")
    res = wordpress_register_account(campaign_id)
    if res == "Done":
        updateTasks("WORDPRESS_ACCOUNT_REGISTER", campaign_id, "Done")

        res2 = wordpress_remove_default_post(campaign_id)
        if res2 == "Done":
            updateTasks("WORDPRESS_REMOVE_DEFAULT_POST", campaign_id, "Done")
        else:
            updateTasks("WORDPRESS_REMOVE_DEFAULT_POST", campaign_id, "Fail")

        res3 = wordpress_change_title(campaign_id)
        if res3 == "Done":
            updateTasks("WORDPRESS_CHANGE_TITLE", campaign_id, "Done")
            return "success"
        else:
            updateTasks("WORDPRESS_CHANGE_TITLE", campaign_id, "Fail")
            return "bad"

        res4 = post_publish_wordpress(campaign_id)
        if res4 == "Done":
            updateTasks("PUBLISH_WORDPRESS_CONTENT_POST_1", campaign_id, "Done")
        else:
            updateTasks("PUBLISH_WORDPRESS_CONTENT_POST_1", campaign_id, "Fail")
    else:
        updateTasks("WORDPRESS_ACCOUNT_REGISTER", campaign_id, "Fail")



def start_campaign_test(campaign_id):
    res = wordpress_register_account(campaign_id)
    if res == "Done":
        updateTasks("WORDPRESS_ACCOUNT_REGISTER", campaign_id, "Done")
        res2 = wordpress_remove_default_post(campaign_id)
        if res2 == "Done":
            updateTasks("WORDPRESS_REMOVE_DEFAULT_POST", campaign_id, "Done")
        else:
            updateTasks("WORDPRESS_REMOVE_DEFAULT_POST", campaign_id, "Fail")
    else:
        updateTasks("WORDPRESS_ACCOUNT_REGISTER", campaign_id, "Fail")
