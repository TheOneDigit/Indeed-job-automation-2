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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config = configparser.ConfigParser()
config.read('config.ini')

email = config['JobDetails']['email']
Password = config['JobDetails']['Password']


first_name = config['JobDetails']['first_name']
last_name = config['JobDetails']['last_name']
phone_no = config['JobDetails']['phone_no']
job_zipcode = config['JobDetails']['job_zipcode']


def wait(driver):
    # print('Start: Wait for 2 second')
    driver.implicitly_wait(3)
    sleep(2)
    # print('End: Wait for 2 second')

def setup_driver():
    driver = Driver(uc=True, headless=False)
    return driver

def login_to_indeed(driver):
    print('\n\nstart: Hit login page URL\n')
    driver.get('https://secure.indeed.com/auth?hl=en_PK&co=PK&continue=https%3A%2F%2Fpk.indeed.com%2F%3Fr%3Dus&tmpl=desktop&from=gnav-util-homepage&jsContinue=https%3A%2F%2Fonboarding.indeed.com%2Fonboarding%3Fhl%3Den_PK%26co%3DPK%26from%3Dgnav-homepage&empContinue=https%3A%2F%2Faccount.indeed.com%2Fmyaccess')

    sleep(5)
    
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
    sleep(8)
    
    try: 
        driver.find_element(By.XPATH,'//span[text()="Continue"]//parent::button').click()
        sleep(7.3)
    except:
        pass   
    
    driver.switch_to.window(main_window)
    print("Login Successful!\n")


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
    Submit= False

    print('\nApply to this job URL: ', job_url)
    driver.get(job_url)

    try:
        driver.find_element('xpath', "//span[text()='Applied']")
        applied = True
    except: 
        applied = False

        
    if applied==False:
        try:
            print('\nStart: Click on Apply Button\n')
            apply_btn = driver.find_element('xpath', "//span[text()='Apply now']")
            apply_btn.click()
            wait(driver)
            print('\nEnd: Click on Apply Button\n')
        except Exception as e:
            print(f"Error applying: {e}")

        sleep(5.1)
        try:
            print('\nTry to add first name\n')
            f_name_input = driver.find_element(By.XPATH,'//input[@id="input-firstName"]')
            f_name_input.send_keys(Keys.CONTROL + "a")  
            f_name_input.send_keys(Keys.DELETE)  
            f_name_input.send_keys(str(first_name))
            print('\nFirst name added\n')
            
            print('\nTry to add last name\n')
            l_name_input = driver.find_element(By.XPATH,'//input[@id="input-lastName"]')
            l_name_input.send_keys(Keys.CONTROL + "a") 
            l_name_input.send_keys(Keys.DELETE)  
            l_name_input.send_keys(str(last_name))
            print('\nlast name added\n')

            print('\nTry to add city name\n')
            city_name_input = driver.find_element(By.XPATH,'//input[@id="input-location.city"]')
            city_name_input.send_keys(Keys.CONTROL + "a") 
            city_name_input.send_keys(Keys.DELETE)  
            city_name_input.send_keys(str(job_zipcode))  
            print('\ncity name added\n')  
            
            print('\nTry to add phone number\n')
            phone_no_input = driver.find_element(By.XPATH,'//input[@id="input-phoneNumber"]')
            phone_no_input.send_keys(Keys.CONTROL + "a")  
            phone_no_input.send_keys(Keys.DELETE)  
            phone_no_input.send_keys(str(phone_no))  
            print('\nphone number added\n')  
            
            print('\nTry to click on continue button\n')
            continue_buttons = driver.find_elements(By.XPATH, '//span[text()="Continue"]//parent::button')
            for btn in continue_buttons:
                try:
                    # Scroll the button into view
                    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                    
                    # Wait until the button is clickable (to ensure it is interactable)
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(btn))
                    
                    # Click the button
                    btn.click()
                    print('Clicked on the continue button.')
                except Exception as e:
                    # print(f'Failed to click continue button: {e}')
                    pass
        except Exception as e:
            print("Error in add personal details page (like: first name, last name, phone number): \n", e)
        sleep(5)

        print('\nTry to add resume\n')
        upload_resume(driver, file_path=resume_pdf_path)

        sleep(5)

        print('\nTry to click on continue button\n')
        continue_buttons = driver.find_elements(By.XPATH, '//span[text()="Continue"]//parent::button')
        for btn in continue_buttons:
            try:
                # Scroll the button into view
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                
                # Wait until the button is clickable (to ensure it is interactable)
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable(btn))
                
                # Click the button
                btn.click()
                print('Clicked on the continue button.')
            except Exception as e:
                # print(f'Failed to click continue button: {e}')
                pass
        sleep(5)
        
        print('\nTry to click on continue button\n')
        continue_buttons = driver.find_elements(By.XPATH, '//span[text()="Continue"]//parent::button')
        for btn in continue_buttons:
            try:
                # Scroll the button into view
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                
                # Wait until the button is clickable (to ensure it is interactable)
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable(btn))
                
                # Click the button
                btn.click()
                print('Clicked on the continue button.')
            except Exception as e:
                # print(f'Failed to click continue button: {e}')
                pass
        sleep(5)


        try:
            print("Try to click on Submit your application button")
            submit_application = driver.find_element(By.XPATH, "//button[span[text()='Submit your application']]")
            
            # Scroll the button into view
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_application)
            
            # Wait until the button is clickable (to ensure it is interactable)
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(submit_application))
            
            submit_application.click()
            print('Submit Application Successfully')
            Submit= True
            sleep(5)
        except Exception as e:
            print('Error while clicking Submit your application button:',e)

    else: 
        print("\n\n Application already Submitted")
        job_title, job_type, job_link  = job_info[0], job_info[1], job_url
        job_log =  [job_title] + [job_type] + ['Failed - Application already Submitted'] + [job_link]
        track_json = "track.json"
        update_job_json(file_path=track_json, job_data=job_log)
        Submit= "Any"


    if Submit== True:
        job_title, job_type, job_link  = job_info[0], job_info[1], job_url
        job_log =  [job_title] + [job_type] + ['Success - Application Submitted'] + [job_link]
        track_json = "track.json"
        update_job_json(file_path=track_json, job_data=job_log)
    if Submit== False:
        job_title, job_type, job_link  = job_info[0], job_info[1], job_url
        job_log =  [job_title] + [job_type] + ['Failed - Application not Submitted'] + [job_link]
        track_json = "track.json"
        update_job_json(file_path=track_json, job_data=job_log)
    # print('Finished Application Processing on this URL: ', job_url, '\n\n')


