import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

URL = "https://www.linkedin.com/jobs/search?keywords=Data%20Engineer&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"


def scrapeWebpage():
    driver = webdriver.Chrome()
    driver.get(URL)

    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "ul.jobs-search__results-list")
        )
    )

    # Get the number of job listings on the page
    num_job_listings = len(
        driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list > li")
    )

    # Create a directory for the job JSON files
    os.makedirs("jobs", exist_ok=True)

    # For each job listing
    for i in range(num_job_listings):
        # Fetch fresh references for the job listings
        job_listings = driver.find_elements(
            By.CSS_SELECTOR, "ul.jobs-search__results-list > li"
        )

        # Click on a job listing to get the full description
        job_listings[i].click()

        # Wait for the full job description to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "section.show-more-less-html")
            )
        )

        job_title = job_listings[i].find_element(By.CSS_SELECTOR, "h3").text
        company_name = job_listings[i].find_element(By.CSS_SELECTOR, "h4").text
        location = (
            job_listings[i]
            .find_element(By.CSS_SELECTOR, "span.job-search-card__location")
            .text
        )
        try:
            date_posted = (
                job_listings[i]
                .find_element(By.CSS_SELECTOR, "time.job-search-card__listdate")
                .get_attribute("datetime")
            )
        except NoSuchElementException:
            date_posted = None
        job_description = driver.find_element(
            By.CSS_SELECTOR, "div.show-more-less-html__markup"
        )

        # Parse the HTML
        soup = BeautifulSoup(job_description.get_attribute("innerHTML"), "html.parser")

        job = {
            "job_title": job_title,
            "company_name": company_name,
            "location": location,
            "date_posted": date_posted,
            "job_description": soup.get_text(),
        }

        # Save the job listing to a json file
        with open(os.path.join("jobs", f"job_{i}.json"), "w") as f:
            json.dump(job, f)

        # Navigate back to the listings page to avoid the stale element reference error
        driver.back()

        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "ul.jobs-search__results-list")
            )
        )

        # Delay execution for a certain amount of seconds
        time.sleep(3)

    driver.quit()
