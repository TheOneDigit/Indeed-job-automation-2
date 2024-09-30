import streamlit as st
from indeed_autoapply import setup_driver, login_to_indeed, apply_for_job
from Indeed_Scrapper import IndeedScrapper
import os
import pandas as pd

st.title("Job Application Automation")

job_title = st.text_input("Enter the Job Title")
job_zipcode = st.text_input("Enter the Job Zipcode")
job_pages = st.text_input("Enter the Number of Job Pages")
resume_pdf = st.text_input("Please Input Resume Full Path")

if st.button("Apply to All") and job_pages and job_zipcode and job_title:
    runtest = IndeedScrapper()
    runtest.scrapper(job_title, job_zipcode, job_pages)

    # csv_file = 'IndeedData.csv'
    # if os.path.exists(csv_file):
    #     print("CSV File exists.")
    # else:
    #     print("CSV File does not exist.")

    df = pd.read_csv('IndeedData.csv')
    df_list = df.values.tolist()
    job_data = [[i[0], i[4], i[-1]] for i in df_list]
    # job_url_list: list = df['href'].to_list()

    # Set up driver and perform operations
    print('Setting up Driver')
    print('Wait For one Minute')
    driver = setup_driver()
    login_to_indeed(driver)  # Logging into Indeed
            
    for single_row in job_data:
        job_url = single_row[-1]
        rest_of = single_row[:-1]
        print("Starting the application process...")
        apply_for_job(driver, job_url, rest_of, resume_pdf)
        print("Job application process completed.", '\n\n')
   
    driver.close()
    driver.quit()