import datetime
import json
import os
import time
from datetime import timedelta

import requests
from bs4 import BeautifulSoup


class LinkedInJobExtractor:
    def __init__(self):
        pass

    # Function to convert freshness to posted date
    def convert_freshness_to_posted_date(self, freshness):
        today = datetime.datetime.now()

        if 'minute' in freshness:
            minutes_ago = int(freshness.split()[0])
            posted_date = today - timedelta(minutes=minutes_ago)
        elif 'hour' in freshness:
            hours_ago = int(freshness.split()[0])
            posted_date = today - timedelta(hours=hours_ago)
        elif 'day' in freshness:
            days_ago = int(freshness.split()[0])
            posted_date = today - timedelta(days=days_ago)
        elif 'week' in freshness:
            weeks_ago = int(freshness.split()[0])
            posted_date = today - timedelta(weeks=weeks_ago)
        else:
            # Handle other cases or return None as needed
            return None

        return posted_date.strftime('%Y-%m-%d')

    def get_job_details_with_id(self, job_title, location, time_span, num_pages):
        job_details = []

        for i in range(num_pages):
            target_url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={job_title}&location={location}&f_TPR=r{time_span}&start={i}'
            response = requests.get(target_url)
            print(target_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                all_jobs_on_page = soup.find_all("li")
                time.sleep(1)
                for x in range(0, len(all_jobs_on_page)):
                    try:
                        soup_item = all_jobs_on_page[x]
                        jobid = soup_item.find("div", class_="base-card").get('data-entity-urn').split(":")[3]

                        # Extracting information with error handling
                        title = soup_item.find('h3', class_='base-search-card__title').text.strip() if soup_item.find(
                            'h3', class_='base-search-card__title') else "N/A"
                        company_name = soup_item.find('h4',
                                                      class_='base-search-card__subtitle').text.strip() if soup_item.find(
                            'h4', class_='base-search-card__subtitle') else "N/A"
                        location = soup_item.find('span',
                                                  class_='job-search-card__location').text.strip() if soup_item.find(
                            'span', class_='job-search-card__location') else "N/A"

                        # Check if the 'time' element is present before accessing 'text'
                        posted_time_element = soup_item.find('time', class_=lambda
                            value: value and 'job-search-card__listdate' in value)
                        posted_time = posted_time_element.text.strip() if posted_time_element else "N/A"
                        posted_time = self.convert_freshness_to_posted_date(posted_time)

                        link_element = soup_item.find('a', class_='base-card__full-link')
                        link = link_element['href'] if link_element else "N/A"

                        details = {
                            "id": jobid,
                            "title": title,
                            "link": link,
                            "company": company_name,
                            "location": location,
                            "posted_time": posted_time
                        }
                        job_details.append(details)
                    except Exception as e:
                        print(f"Error processing job with id {jobid}: {str(e)}")

        return job_details

    def get_job_ids(self, job_title, location, time_span, num_pages):
        job_ids = []

        for i in range(num_pages):
            target_url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={job_title}&location={location}&f_TPR=r{time_span}&start={i}'
            response = requests.get(target_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                all_jobs_on_page = soup.find_all("li")
                time.sleep(1)
                for x in range(0, len(all_jobs_on_page)):
                    try:
                        jobid = all_jobs_on_page[x].find("div", class_="base-card").get('data-entity-urn').split(":")[3]
                        job_ids.append(jobid)
                    except:
                        pass

        return job_ids

    def extract_job_details(self, job_id):
        job_details = []

        try:
            target_url = f"https://in.linkedin.com/jobs/view/{job_id}"
            response = requests.get(target_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                job_element = soup.find("section", class_="top-card-layout")

                if job_element:
                    title = job_element.find("h1", class_="top-card-layout__title").getText().strip()
                    url = ""
                    try:
                        url = job_element.find("code", {'id': 'applyUrl'})
                        link = url.string.replace('"', "")
                    except:
                        link = ""

                    organisation = job_element.find("a", class_="topcard__org-name-link").getText().strip()
                    location = job_element.find("span", class_="topcard__flavor--bullet").getText().strip()
                    freshness = job_element.find("span", class_="posted-time-ago__text").getText().strip()

                    details = {
                        "id": job_id,
                        "title": title,
                        "url": link,
                        "organisation": organisation,
                        "location": location,
                        "posted_date": self.convert_freshness_to_posted_date(freshness)
                    }

                    job_details.append(details)

        except Exception as e:
            print(f"Error processing job ID {job_id}: {str(e)}")

        return job_details

    def extract_jobs(self, job_title, location, time_span, num_pages):
        # job_ids = self.get_job_ids(job_title, location, time_span, num_pages)
        #
        # extracted_job_details = []
        #
        # for job_id in job_ids:
        #     time.sleep(0.5)
        #     job_details = self.extract_job_details(job_id)
        #     extracted_job_details.extend(job_details)
        # self.get_job_details_with_id(job_title, location, time_span, num_pages)
        # return extracted_job_details
        print(self.get_job_ids(job_title, location, time_span, num_pages))

        # here we will use new method
        return []

    def save_jobs_to_json(self, job_details, filename='job_data.json'):
        with open(filename, 'w') as json_file:
            json.dump(job_details, json_file, indent=2)
        print(f"Job details saved to {filename}")

    def load_jobs_from_json(self, filename='job_data.json'):
        if os.path.exists(filename):
            with open(filename, 'r') as json_file:
                job_details = json.load(json_file)
            return job_details
        else:
            print(f"{filename} not found. Returning an empty list.")
            return []

    def filter_jobs_by_freshness(self, job_details, max_days):
        today = datetime.datetime.now()
        filtered_jobs = []

        for job in job_details:
            posted_date = datetime.datetime.strptime(job['posted_time'], '%Y-%m-%d')
            days_ago = (today - posted_date).days

            if days_ago <= max_days:
                filtered_jobs.append(job)

        return filtered_jobs

    def delete_old_entries(self, job_details, max_days):
        today = datetime.datetime.now()
        updated_job_details = [job for job in job_details if
                               (today - datetime.datetime.strptime(job['posted_time'], '%Y-%m-%d')).days <= max_days]
        return updated_job_details

    def update_and_save_jobs(self, job_title, location, time_span, num_pages, max_days=30):
        # Load existing job details
        job_details = self.load_jobs_from_json()

        # Get new job details
        new_job_details = self.get_job_details_with_id(job_title, location, time_span, num_pages)

        # Combine old and new job details, then filter based on freshness
        updated_job_details = self.delete_old_entries(job_details + new_job_details, max_days)

        # Save the updated job details
        self.save_jobs_to_json(updated_job_details)

        return updated_job_details


def main():
    extractor = LinkedInJobExtractor()

    job_title = "Android developer"
    location = "india"
    time_span = "2592000"
    num_pages = 5

    # Update and save jobs
    updated_jobs = extractor.update_and_save_jobs(job_title, location, time_span, num_pages)

    # Filter jobs based on freshness
    filtered_jobs = extractor.filter_jobs_by_freshness(updated_jobs, max_days=15)

    print("Filtered Jobs:")
    print(filtered_jobs)




if __name__ == "__main__":
    main()
