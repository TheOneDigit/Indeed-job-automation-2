from seleniumbase import Driver
from HandyWrappers import HandyWrappers
import json
import os
import csv
from selenium.webdriver.common.by import By


class IndeedScrapper:
    
    def scrapper(self, job_title: str, job_location: str, total_page: int):
        
        print('Start: Job data scrapping Process Begin')
        Job_Title = job_title
        Job_Location = str(job_location)
        total_pages = int(total_page)

        Job_Title_for_link = Job_Title.replace(" ", "+")
        Job_Location_for_link = Job_Location.replace(" ", "+")
        base_url = f'https://pk.indeed.com/jobs?q={Job_Title_for_link}&l={Job_Location_for_link}&start='

        csv_file = 'IndeedData.csv'
        fieldnames = ['Job Title', 'Location', 'Company Name', 'Pay', 'Job Type', 'Description', 'Location or Zipcode', 'href']

        # Load existing jobs to check for duplicates
        existing_jobs = set()
        if os.path.exists(csv_file):
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    existing_jobs.add((row['Job Title'], row['Company Name']))

        # Open CSV to add new jobs
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Write header if the file is newly created
            if os.path.getsize(csv_file) == 0:
                writer.writeheader()

            
            for page in range(int(total_pages)):           
                page_url = f"{base_url}{page*10}"
                # print(page_url)
                driver = Driver(uc=True, headless=False)
                helpers = HandyWrappers(driver)
                driver.get(page_url)
                driver.implicitly_wait(5)

                

                if not helpers.isElementPresent('//h1[text()= " did not match any jobs."]', 'xpath'):
                    job_urls = driver.find_elements(By.XPATH, '//span[text()="Easily apply"]//parent::span//parent::div//parent::div//parent::div//child::a')
                    # job_urls = driver.find_elements(By.CSS_SELECTOR, 'tr > td > div >h2 > a')
                    job_title_elements = driver.find_elements(By.XPATH, '//span[text()="Easily apply"]//parent::span//parent::div//parent::div//parent::div//child::a//child::span')
                    hrefs = []
                    jobs_titles = []
                    for element in job_urls:
                        if element.text !="View similar jobs with this employer":
                            try:
                                href = element.get_attribute('href')
                                # print(href)
                                if '/rc/clk?jk=' in href:
                                    hrefs.append(href)
                            except Exception as e:
                                print(f"Error retrieving href: {e}")
                    
                    for element in job_title_elements:
                        try:
                            jobs_title = element.text
                            # print(jobs_title)
                            jobs_titles.append(jobs_title)
                        except Exception as e:
                            print(f"Error retrieving job title: {e}")
                        

                    # Get jobs list on the current page
                    # jobs_ = helpers.GetElementlistofattribute(Locator='//span[text()="Easily apply"]//parent::span//parent::div//parent::div//parent::div//child::a', LocatorType='xpath', attribute='aria-label')
                    list_of_jobs = [job.replace("full details of ", "") for job in jobs_titles]
                    # print('This is len of list_of_jobs: ', len(list_of_jobs))
                    for job, href in zip(list_of_jobs,hrefs):
                        
                        # Scrape job title and company name first
                        try:
                            helpers.ClickElement(Locator=f'//div//h2//a[@aria-label="full details of {job}"]', LocatorType='xpath')
                            # time.sleep(2)

                            # Scrape the company name
                            company_name = helpers.GetElementAttribute(f'//span[text()="{job}"]//ancestor::div//div[@data-company-name]//a[contains(@aria-label, "(opens in a new tab)")]', 'xpath', 'aria-label')
                            company_name = company_name.split(" (")[0]
                        except:
                            continue
                       

                        # Check if job already exists in file
                        if (job, company_name) in existing_jobs:
                            print(f"Skipping duplicate job: {job} at {company_name}")
                            continue

                        # If not a duplicate
                        try: 
                            pay = helpers.GetElementText('//h3[text()="Pay"]//parent::div//div[text()]', 'xpath')
                        except: 
                            try: 
                                pay = helpers.GetElementText('//div[@id="jobDescriptionText"]//p[contains(., "Pay")]', 'xpath')[5:]
                            except: 
                                pay = 'N/A'

                        try: 
                            job_type = helpers.GetElementlistofText('//h3[text()="Job type"]//parent::div//div[text()]', 'xpath')
                            job_type = ', '.join(job_type)
                        except:
                            try: 
                                job_type = helpers.GetElementText('//div[@id="jobDescriptionText"]//p[contains(., "Job Type")]', 'xpath')[11:]
                            except: 
                                job_type = 'N/A'

                        try: 
                            description = helpers.GetElementlistofText('//div[@id="jobDescriptionText"]//*[self::div or self::p or self::li]', 'xpath')
                            description = ' '.join(description)
                        except: 
                            description = 'N/A'

                        # print('This is job title Before Save: ', job)
                        data = {
                            'Job Title': job, 
                            'Location': Job_Location, 
                            'Company Name': company_name, 
                            'Pay': pay, 
                            'Job Type': job_type, 
                            'Description': description,
                            'Location or Zipcode': Job_Location,
                            'href': href 
                        }
                        print(json.dumps(data, indent=4))
                        writer.writerow(data)

                        existing_jobs.add((job, company_name))

                    # for href in hrefs:
                    #     writer.writerow({'href': href})
                else:
                    print('There is no Job Posts Available')

                driver.close()
                driver.quit()
                print('End: Scrapping Process End', "\n\n")


