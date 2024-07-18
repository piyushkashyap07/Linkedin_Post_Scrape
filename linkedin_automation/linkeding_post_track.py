import json
import os
import time
import random
import requests
import pymongo
import csv
import gridfs
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

# Load environment variables from .env file
env_path = r'.env'
load_dotenv(dotenv_path=env_path)

# Get environment variables
LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
MONGO_URI = os.getenv("MONGO_URI")
DRIVER_PATH = os.getenv("DRIVER_PATH")

# Import configuration
config_path = r"config.json"
with open(config_path, 'r') as file:
    config = json.load(file)

client = pymongo.MongoClient(MONGO_URI)
db = client["test"]
collection = db["job_posts"]

def list_to_csv(list_of_lists, csv_filename):
    
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write each list (row) to the CSV file
        for row in list_of_lists:
            writer.writerow(row)
    print(f"Data has been written to {csv_filename}")

def slow_scroll(driver, duration_minutes=3):
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)

    while time.time() < end_time:
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)  # Adjust the sleep time as needed to control scroll speed

    print("Finished scrolling.")

# Function to login to LinkedIn
def login(driver, username, password):
    try:
        url = 'https://www.linkedin.com/login'
        driver.get(url)
        time.sleep(random.randint(6, 10))

        username_input = driver.find_element(By.XPATH, config["username_input_xpath"])
        username_input.send_keys(username)

        password_input = driver.find_element(By.XPATH, config["password_input_xpath"])
        password_input.send_keys(password)

        password_input.send_keys(Keys.RETURN)
        time.sleep(random.randint(180, 300))
    except Exception as e:
        print(f"Error during login: {e}")

# Function to initialize the WebDriver and login
def initialize_driver_and_login():
    try:
        chromedriver_path = DRIVER_PATH
        
        # Use ChromeService to specify the chromedriver executable path
        service = ChromeService(executable_path=chromedriver_path)
        
        # Set options to avoid sandbox and specify user data directory
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")  
        chrome_options.add_argument("--disable-dev-shm-usage")  
        
        # Initialize Chrome webdriver with options and service
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        return driver
    except Exception as e:
        print(f"Error from initialize_driver_and_login: {e}")

def scrape_posts(driver, task_search):
    try:
        driver.maximize_window()
        time.sleep(2)
        task = driver.find_element(By.XPATH, config["search_box"])
        task.send_keys(task_search)
        task.send_keys(Keys.RETURN)
        time.sleep(5)
        post_btn = driver.find_element(By.XPATH, config["post_btn"]).click()
        time.sleep(3)
        slow_scroll(driver)
        time.sleep(3)
        posts = driver.find_elements(By.XPATH, config["post_ele"])
        arr = []

        for post in posts:
            time.sleep(3)
            sm_arr = []

            try:
                name = post.find_element(By.XPATH, config["name_post"]).text
            except Exception as e:
                name = None
                print(f"Error getting name: {e}")

            try:
                designation = post.find_element(By.XPATH, config["designation_post"]).text
            except Exception as e:
                designation = None
                print(f"Error getting designation: {e}")

            try:
                linkedin_url = post.find_element(By.XPATH, config["linkedin_post"]).get_attribute('href')
            except Exception as e:
                linkedin_url = None
                print(f"Error getting LinkedIn URL: {e}")

            try:
                content = post.find_element(By.XPATH, config["post_text"]).text
            except Exception as e:
                content = None
                print(f"Error getting content: {e}")

            try:
                post_date = post.find_element(By.XPATH, config["post_time"]).text
            except Exception as e:
                post_date = None
                print(f"Error getting post date: {e}")

            try:
                image_element = post.find_element(By.TAG_NAME, 'img')
                image_url = image_element.get_attribute('src') if image_element else None
            except Exception as e:
                image_url = None
                print(f"Error getting image URL: {e}")

            # sm_arr.append(name)
            # sm_arr.append(designation)
            # sm_arr.append(linkedin_url)
            # sm_arr.append(content)
            # sm_arr.append(post_date)
            # sm_arr.append(image_url)

            time.sleep(5)

            # Uncomment the following block if you want to save data to MongoDB
            try:
                collection.insert_one({
                    "name": name,
                    "designation": designation,
                    "linkedin_url": linkedin_url,
                    "content": content,
                    "post_date": post_date,
                    "image_id": image_url
                })
            except Exception as e:
                print(f"Error inserting data to MongoDB: {e}")

            # arr.append(sm_arr)
        
        # Optionally, save the scraped data to a CSV file
        # list_to_csv(arr, "linkedin_posts.csv")

    except Exception as e:
        print(f"Error during scraping: {e}")

# Main script execution
if __name__ == "__main__":
    task_search = input("Enter the tag you want to search: ")
    driver = initialize_driver_and_login()
    login(driver, LINKEDIN_USERNAME, LINKEDIN_PASSWORD)
    scrape_posts(driver, task_search)
    time.sleep(180)
    driver.quit()
