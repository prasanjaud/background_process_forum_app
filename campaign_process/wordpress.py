import json
import random
import string
import threading
import time

from selenium.common import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods.posts import NewPost

from helper.campaign_sql_queries import updateTasks, getAllNewEmails, updateEmailStatus, saveNewUser, \
    getUserDetailsByCampaign, getCampaignDetailsQuery, getGroupsAllContents

from selenium import webdriver

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def get_driver():
    option = webdriver.ChromeOptions()
    option.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=option)

    return driver

def generate_random_website():
    websites = [
        "https://www.youtube.com/",
        "https://lk.linkedin.com/?original_referer=https%3A%2F%2Fwww.google.com%2F",
        "https://twitter.com/i/flow/login?redirect_after_login=%2F%3Flang%3Den",
        "https://www.fiverr.com/",
        "https://github.com/",
        "https://www.upwork.com/"
        # Add more random website URLs as needed
    ]
    return random.choice(websites)

def wordpress_register_account(campaignID):
    # result = getModuleCode('register_account')
    # code_snippet = result['code_text']
    # exec(code_snippet)

    try:
        driver = get_driver()

        driver.maximize_window()
        random_website = generate_random_website()
        driver.get(random_website)
        driver.get("https://wordpress.com")
        wait = WebDriverWait(driver, 10)
        password = generate_password(10)
        get_started_btn = driver.find_element(By.XPATH,
                                              "//a[@role=\"menuitem\" and contains(@class, \"x-nav-link--primary\") and contains(@class, \"x-link\")]")
        get_started_btn.click()

        # user_emails_file_path = "user_emails.txt"
        # txt_file = open(user_emails_file_path, "r")
        # user_emails = []
        #
        # for line in txt_file:
        #     user_emails.append(line.strip())
        # txt_file.close()
        user_emails = getAllNewEmails()
        print(user_emails[0], "tets")

        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"email\"]")))
        email_txt_field = driver.find_element(By.XPATH, "//*[@id=\"email\"]")
        email_txt_field.send_keys(user_emails[0]['email'])
        email_value = user_emails[0]['email']

        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"username\"]")))
        username_txt_field = driver.find_element(By.XPATH, "//*[@id=\"username\"]")
        username_txt_field.send_keys(user_emails[0]['email'][:5])
        username_value = user_emails[0]['email'][:5]

        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"password\"]")))
        password_txt_field = driver.find_element(By.XPATH, "//*[@id=\"password\"]")
        password_txt_field.send_keys(password)
        password_value = password

        register_form = driver.find_element(By.XPATH, "//form")
        register_form.submit()

        is_novalidate = register_form.get_attribute("novalidate") is not None

        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='signup-form__separator-text']")))
        empty_space = driver.find_element(By.XPATH, "//div[@class='signup-form__separator-text']")
        actions = ActionChains(driver)

        count = 0
        while is_novalidate:
            if is_novalidate:
                print("The form has the 'novalidate' attribute.")
                count += 1
                time.sleep(1)
                class_attribute_email = email_txt_field.get_attribute("class")
                is_error_email = "is-error" in class_attribute_email.split()

                class_attribute_username = username_txt_field.get_attribute("class")
                is_error_username = "is-error" in class_attribute_username.split()

                class_attribute_password = password_txt_field.get_attribute("class")
                is_error_password = "is-error" in class_attribute_password.split()

                # Print the result
                if is_error_email:
                    print("The email has the 'is-error' class.")
                    email_txt_field.clear()
                    email_txt_field.send_keys(user_emails[count]['email'])
                    email_value = user_emails[count]
                else:
                    print("The email does not have the 'is-error' class.")

                if is_error_username:
                    print("The username has the 'is-error' class.")
                    username_txt_field.clear()
                    username_txt_field.send_keys(email_value[:6] + str(count))
                    username_value = email_value[:6] + str(count)
                else:
                    print("The username does not have the 'is-error' class.")

                if is_error_password:
                    print("The password has the 'is-error' class.")
                    password_txt_field.clear()
                    password_txt_field.send_keys(password + str(count))
                    password_value = password + str(count)
                else:
                    print("The password does not have the 'is-error' class.")

                if not is_error_email and not is_error_username and not is_error_password:
                    break

            else:
                print("The form does not have the 'novalidate' attribute.")

            actions.move_to_element(empty_space).click().perform()

        register_form.submit()
        # saveNewUser(email_value, username_value, password_value)
        updateEmailStatus(email_value, "Used in Wordpress")

        time.sleep(2)
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[@id=\"primary\"]/div/div[2]/div/div/div/div[3]/div/div/div[2]/div[1]/div/div[3]/button")))
        domain_later_link = driver.find_element(By.XPATH,
                                                "//*[@id=\"primary\"]/div/div[2]/div/div/div/div[3]/div/div/div[2]/div[1]/div/div[3]/button")
        domain_later_link.click()

        time.sleep(2)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), \"Start with Free\")]")))
        free_start_btn = driver.find_element(By.XPATH, "//button[contains(text(), \"Start with Free\")]")
        free_start_btn.click()

        wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), \"Skip to dashboard\")]")))
        skip_btn = driver.find_element(By.XPATH, "//button[contains(text(), \"Skip to dashboard\")]")
        skip_btn.click()

        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[@id=\"wpcom\"]/div/div[3]/div[3]/main/div[2]/div[1]/div[1]/div[3]/ul/li[6]/button")))
        launch_site_btn = driver.find_element(By.XPATH,
                                              "//*[@id=\"wpcom\"]/div/div[3]/div[3]/main/div[2]/div[1]/div[1]/div[3]/ul/li[6]/button")
        launch_site_btn.click()
        time.sleep(5)
        user_id = saveNewUser(email_value, username_value, password_value, campaignID)
        # start_scheduler_wordpress(campaignID, user_id)

        return "Done"


    except TimeoutException as e:
        print(f"Timeout Exception: {e}")
        return "Fail"

    except NoSuchElementException as e:
        print(f"No Such Element Exception: {e}")
        return "Fail"

    except ElementNotInteractableException as e:
        print(f"Element Not Interactable Exception: {e}")
        return "Fail"

    except Exception as e:
        print(f"Exception occurred: {e}")
        return "Fail"

    finally:
        # Perform any cleanup or finalization tasks here
        driver.quit()

def wordpress_remove_default_post(campaignID):
    try:
        user_dets = getUserDetailsByCampaign(campaignID)
        option = webdriver.ChromeOptions()
        option.add_experimental_option('detach', True)
        driver = webdriver.Chrome(options=option)
        driver.maximize_window()
        random_website = generate_random_website()
        driver.get(random_website)
        driver.get("https://wordpress.com")
        wait = WebDriverWait(driver, 10)

        login_btn = driver.find_element(By.XPATH, "//*[@id=\"lpc-header-nav\"]/div/div/div[1]/div/nav/ul[2]/li[1]/a")
        login_btn.click()

        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"usernameOrEmail\"]")))
        email_txt_field = driver.find_element(By.XPATH, "//*[@id=\"usernameOrEmail\"]")
        email_txt_field.send_keys(user_dets['username'])

        continue_btn = driver.find_element(By.XPATH,
                                           "//*[@id=\"primary\"]/div/main/div/div/form/div[1]/div[2]/button")
        continue_btn.click()

        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"password\"]")))
        password_txt_field = driver.find_element(By.XPATH, "//*[@id=\"password\"]")
        password_txt_field.send_keys(user_dets['password'])

        login_btn = driver.find_element(By.XPATH, "//*[@id=\"primary\"]/div/main/div/div/form/div[1]/div[2]/button")
        login_btn.click()

        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"secondary\"]/div/ul/li[6]/ul/li[1]/a")))
        posts_nav_btn = driver.find_element(By.XPATH, "//*[@id=\"secondary\"]/div/ul/li[6]/ul/li[1]/a")
        posts_nav_btn.click()

        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id=\"primary\"]/main/div[3]/div[2]/div/div[3]/span/button")))
        post_action_btn = driver.find_element(By.XPATH,
                                              "//*[@id=\"primary\"]/main/div[3]/div[2]/div/div[3]/span/button")
        post_action_btn.click()

        # wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[7]/div/div[2]/div/button[4]")))
        trash_btn = driver.find_element(By.XPATH,
                                        "//button[contains(@class, 'popover__menu-item') and contains(., 'Trash')]")
        trash_btn.click()

        # time.sleep(30)
        driver.close()
        return "Done"

    except TimeoutException as e:
        print(f"Timeout Exception: {e}")
        return "Fail"

    except NoSuchElementException as e:
        print(f"No Such Element Exception: {e}")
        return "Fail"

    except ElementNotInteractableException as e:
        print(f"Element Not Interactable Exception: {e}")
        return "Fail"

    except Exception as e:
        print(f"Exception occurred: {e}")
        return "Fail"

    finally:
        # Perform any cleanup or finalization tasks here
        driver.quit()

def wordpress_change_title(campaignID):
    try:
        user_dets = getUserDetailsByCampaign(campaignID)
        campaigns_dets = getCampaignDetailsQuery(campaignID)
        option = webdriver.ChromeOptions()
        option.add_experimental_option('detach', True)
        driver = webdriver.Chrome(options=option)
        driver.maximize_window()
        random_website = generate_random_website()
        driver.get(random_website)
        driver.get("https://wordpress.com")
        wait = WebDriverWait(driver, 10)

        login_btn = driver.find_element(By.XPATH, "//*[@id=\"lpc-header-nav\"]/div/div/div[1]/div/nav/ul[2]/li[1]/a")
        login_btn.click()

        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"usernameOrEmail\"]")))
        email_txt_field = driver.find_element(By.XPATH, "//*[@id=\"usernameOrEmail\"]")
        email_txt_field.send_keys(user_dets['username'])

        continue_btn = driver.find_element(By.XPATH,
                                           "//*[@id=\"primary\"]/div/main/div/div/form/div[1]/div[2]/button")
        continue_btn.click()

        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"password\"]")))
        password_txt_field = driver.find_element(By.XPATH, "//*[@id=\"password\"]")
        password_txt_field.send_keys(user_dets['password'])

        login_btn = driver.find_element(By.XPATH, "//*[@id=\"primary\"]/div/main/div/div/form/div[1]/div[2]/button")
        login_btn.click()

        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"primary\"]/main/div[2]/div[1]/div[1]/div[2]/ul/li[1]/button")))
        give_site_name_btn = driver.find_element(By.XPATH, "//*[@id=\"primary\"]/main/div[2]/div[1]/div[1]/div[2]/ul/li[1]/button")
        give_site_name_btn.click()

        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"blogname\"]")))
        site_title_txt_field = driver.find_element(By.XPATH, "//*[@id=\"blogname\"]")
        site_title_txt_field.send_keys(Keys.CONTROL + 'a')
        site_title_txt_field.send_keys(Keys.DELETE)
        # site_title_txt_field.clear()
        site_title_txt_field.send_keys(campaigns_dets['site_title'])


        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id=\"primary\"]/main/div[2]/div[1]/div/div[1]/div[2]/button")))
        save_settings_btn = driver.find_element(By.XPATH,
                                              "//*[@id=\"primary\"]/main/div[2]/div[1]/div/div[1]/div[2]/button")
        save_settings_btn.click()
        time.sleep(5)


        # time.sleep(30)
        return "Done"

    except TimeoutException as e:
        print(f"Timeout Exception: {e}")
        return "Fail"

    except NoSuchElementException as e:
        print(f"No Such Element Exception: {e}")
        return "Fail"

    except ElementNotInteractableException as e:
        print(f"Element Not Interactable Exception: {e}")
        return "Fail"

    except Exception as e:
        print(f"Exception occurred: {e}")
        return "Fail"

    finally:
        # Perform any cleanup or finalization tasks here
        driver.quit()

def publish_post(post, user_dets):

    wp = Client(f'https://{user_dets["username"]}.wordpress.com/xmlrpc.php', user_dets["email"], user_dets["password"])
    new_post = WordPressPost()
    new_post.title = post['title']
    new_post.content = post['body']
    new_post.post_status = 'publish'
    wp.call(NewPost(new_post))

def publish_posts_with_delay(delay, campaign_id):
    campaign_dets = getCampaignDetailsQuery(campaign_id)
    user_dets = getUserDetailsByCampaign(campaign_id)

    contents = getGroupsAllContents(campaign_dets['content_group_id'])

    for post in contents:
        publish_post(post, user_dets)
        print(f"Published: {post['title']}")
        time.sleep(delay)

def post_publish_wordpress(campaign_id):
    try:
        # one_day = 24 * 60 * 60
        one_day = 60

        publishing_thread = threading.Thread(target=publish_posts_with_delay, args=(one_day, campaign_id))
        publishing_thread.start()

        publishing_thread.join()

        print("All posts published successfully!")

        return "Done"
    except Exception as e:
        print(f"Error in post_publish_wordpress: {e}")
        return "Fail"