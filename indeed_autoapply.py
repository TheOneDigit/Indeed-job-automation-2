from time import sleep
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from urllib.parse import urlparse
from track_job_json import update_job_json
from openpyxl import Workbook, load_workbook
from datetime import datetime
import os
import json
from seleniumbase import Driver
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

email = config['JobDetails']['email']
Password = config['JobDetails']['Password']


def wait(driver):
    print('Start: Wait for 2 second')
    driver.implicitly_wait(3)
    sleep(2)
    print('End: Wait for 2 second')

def setup_driver():
    # print('Start: Initializing chrome Driver')
    # options = uc.ChromeOptions()
    # driver = uc.Chrome(version_main=128, options=options)
    # print('End: Initializing Chrome Driver')
    driver = Driver(uc=True, headless=False)
    return driver

def login_to_indeed(driver):
    print('start: Hit login page URL')
    driver.get('https://secure.indeed.com/auth?hl=en_PK&co=PK&continue=https%3A%2F%2Fpk.indeed.com%2F%3Fr%3Dus&tmpl=desktop&from=gnav-util-homepage&jsContinue=https%3A%2F%2Fonboarding.indeed.com%2Fonboarding%3Fhl%3Den_PK%26co%3DPK%26from%3Dgnav-homepage&empContinue=https%3A%2F%2Faccount.indeed.com%2Fmyaccess')

    sleep(10)
    
    driver.find_element(By.ID,'login-google-button').click()
    
    # Store the main window handle (current window)
    main_window = driver.current_window_handle

    # Wait for the new window to open (optional)
    sleep(2)

    # Get the list of all window handles
    all_windows = driver.window_handles

    # Switch to the new window (which should be the Google login window)
    for window in all_windows:
        if window != main_window:
            driver.switch_to.window(window)
            break
        
        
    email_input = driver.find_element(By.ID,"identifierId")
    email_input.send_keys(email)
    sleep(4.8)
    
    
    driver.find_element(By.XPATH,'//span[text()="Next"]//parent::button').click()
    sleep(7.3)
    
    email_input = driver.find_element(By.XPATH,'//input[@aria-label="Enter your password"]')
    email_input.send_keys(str(Password))
    sleep(8.1)
    
    
    driver.find_element(By.XPATH,'//span[text()="Next"]//parent::button').click()
    sleep(23.9)
    
    try: 
        driver.find_element(By.XPATH,'//span[text()="Continue"]//parent::button').click()
        sleep(7.3)
    except:
        pass   
    
    driver.switch_to.window(main_window)
    # print('start: Wait for 120 second for manual login')
    # sleep(120)
    # print("End: Wait for 120 second for manual login")
    # print('End: Hit login page URL')
    
# def log_job_application(job_url, status):
    # file_path = 'track.xlsx'
    # # If file doesn't exist, create it
    # if not os.path.exists(file_path):
    #     wb = Workbook()
    #     ws = wb.active
    #     ws.title = 'Job Applications'
    #     ws.append(['Job URL', 'Status', 'Timestamp'])  # Adding headers
    # else:
    #     wb = load_workbook(file_path)
    #     ws = wb.active

    # # Append the job record
    # ws.append([job_url, status, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    # wb.save(file_path)


def upload_resume(driver, file_path: str):
    upload_resume = driver.find_elements(By.XPATH, "//span[text()='Upload a resume']") 

    if upload_resume:  # Upload new resume
        print('Resume not Found --- Start Uploading Process...')
        track = None
        try:
            upload_resume = driver.find_element(By.CSS_SELECTOR, "input[type='file'][accept='.pdf,.txt,.docx,.doc,.rtf']")
            track = True
        except:
            print('Failed to find a upload resume tag')
            track = False
        if track:
            try:
                file_path = file_path
                upload_resume.send_keys(file_path)
            except:
                print('Invalid PDF resume path')
        
    else : # if resume found, select it
        print('Resume is already uploaded')
        try:
            cv_select = driver.find_element(By.CSS_SELECTOR, 'div > div > fieldset > div')
            cv_select.click()  
            wait(driver)
            print('Select Resume successfully')
        except:
            print('failed to select Resume')



def apply_for_job(driver, job_url, job_info, resume_pdf_path: str):

    print('Apply to this job URL: ', job_url)
    driver.get(job_url)
    try:
        print('Start: Click on Apply Button')
        apply_btn = driver.find_element('xpath', "//span[text()='Apply now']")
        apply_btn.click()
        wait(driver)
        print('End: Click on Apply Button')
    except Exception as e:
        print(f"Error applying: {e}")

    while True:
        wait(driver)
        url = driver.current_url
        parsed_url = urlparse(url)
        # print('URL after clicking apply button > ',  parsed_url)
        
        if parsed_url.netloc == 'smartapply.indeed.com':
            print('continue')
        else:
            print('Break: The Apply button redirected to company page.')
            break

        try:
            continue_buttons = driver.find_elements('xpath', "//button[span[text()='Continue']]")
            for btn in continue_buttons:
                btn.click()
                wait(driver)
            print('Clicked on the continuer button')
        except:
            print('Failed to click continue button.')


        upload_resume(driver, file_path=resume_pdf_path)

        sleep(5)
        try:
            submit_application = driver.find_element('xpath', "//button[span[text()='Submit your application']]")
            submit_application.click()
            print('Submit Application Successfully')
            
            job_title, job_type, job_link  = job_info[0], job_info[1], job_info[2]
            job_log =  [job_title] + [job_type] + ['Success - Application Submitted'] + [job_link]
            track_json = "track.json"
            update_job_json(file_path=track_json, job_data=job_log)

            # log_job_application(job_url, 'Success - Application Submitted')
            break
        except:
            print('Failed to submit the application.')
    # print('Finished Application Processing on this URL: ', job_url, '\n\n')



    

# csv_file = 'IndeedData.csv'
# if os.path.exists(csv_file):
#     print("CSV File exists.")
# else:
#     print("CSV File does not exist.")

# import pandas as pd
# df = pd.read_csv('IndeedData.csv')
# job_url_list: list = df['href'].to_list()
# len(job_url_list)

# print('Setting up Driver')
# driver = setup_driver()
# login_to_indeed(driver)  # Logging into Indeed
        
# for job_url in job_url_list:
#     apply_for_job(driver, job_url)
    
