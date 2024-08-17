import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from app_job_scraping.streamlit_app.config.core import config
import time
import pandas as pd

sites = config.base_site
def get_base_site(parent_site) -> str:
    if parent_site == 'naukri':
        site = sites['naukri']
    else:
        site = "https://www.google.com"

    return site

def get_site_url(job_descr_1=None, job_descr_2=None) -> str:
    for page_no in range(1, 11):
        job_descr = job_descr_1 + str(page_no) + job_descr_2
        site = get_base_site(parent_site = 'naukri') + job_descr

    return site


def apply_join_url(job_descr=None) -> str:
    job_descr_1 = "-".join(job_descr.split()) + "-jobs-"
    job_descr_2 = "?k=" + "%20".join(job_descr.split())

    return job_descr_1, job_descr_2


def scrape_naukri_func(job_descr=None) -> list:
    driver = webdriver.Firefox()
    job_elems = []
    job_descr_1, job_descr_2 = apply_join_url(job_descr)

    for page_no in range(1, 11):
        site = get_site_url(job_descr_1, job_descr_2, page_no)
        driver.get(site)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.find(class_='styles_job-listing-container__OCfZC')
        job_elements = results.find_all('div', class_='srp-jobtuple-wrapper')
        job_elems = job_elems + job_elements

    driver.close()  # closes the browser
    return job_elems

def scrape_soup_data(job_elems=None):
    list_data = []
    for job_elem in job_elems:
        # print(job_elem)

        # URL to qpply job
        URL = job_elem.find('a', class_='title').get('href')
        #         print(URL)

        title = job_elem.find('a', class_='title')
        #         print(title.text)

        company = job_elem.find('a', class_=lambda x: "comp-name" in x)
        if company is None:
            continue
        #         else:
        # #             print(company.text)

        experience = job_elem.find('div', class_="row3")
        if experience is None:
            #             print('Not Disclosed')
            continue
        #         else:
        #             print(experience.text.split())

        keywords_ = job_elem.find('div', class_="row5")
        if keywords_ is None:
            #             print('Not Disclosed')
            continue
        else:
            lis = []
            list_ = keywords_.find_all("li")
            for li in list_:
                lis.append(li.text)
        #             print(lis)

        ratings = job_elem.find('span', class_=lambda x: "main-2" in x)
        if ratings is None:
            #             print('No Review')
            continue
        else:
            #             print(ratings.text)
            ratings_no = job_elem.find('a', class_=lambda x: "review ver-line" in x)
            if ratings_no is None:
                # print('No Details')
                continue
        #             else:
        # #                 print(ratings_no.get('href'))
        # #                 print(ratings_no.text)

        #   Appending data to the DataFrame
        list_data.append(
            ['Naukri', URL, title.text, company.text, experience.text.split(), lis, ratings.text, ratings_no.text])
    df = pd.DataFrame(list_data, columns=['SOURCE', 'URL', 'TITLE', 'COMPANY', 'EXPERIENCE', 'KEYWORDS', 'RATINGS',
                                          'NO_OF_RATINGS'])
    return df


