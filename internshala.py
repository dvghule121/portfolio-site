import datetime
import json
import os
import re
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InternshipExtractor:
    def __init__(self):
        pass

    def convert_freshness_to_posted_date(self, freshness):
        today = datetime.datetime.now()
        freshness = freshness.replace('few', '')

        if 'just now' in freshness:
            return (today - datetime.timedelta(minutes=5)).strftime('%Y-%m-%d')
        elif any(keyword in freshness for keyword in ['hours', 'today']):
            return today.strftime('%Y-%m-%d')
        elif any(keyword in freshness for keyword in ['day', 'days']):
            days_ago = int(freshness.split()[0])
            return (today - datetime.timedelta(days=days_ago)).strftime('%Y-%m-%d')
        elif any(keyword in freshness for keyword in ['week', 'weeks']):
            weeks_ago = int(freshness.split()[0])
            return (today - datetime.timedelta(weeks=weeks_ago)).strftime('%Y-%m-%d')
        else:
            return None

    def extract_internship_data(self, internship_container, internship_id):
        try:
            profile = internship_container.find("h3", {"class": "profile"}).find("a")
            link = profile["href"]
            job_title = profile.get_text(strip=True)

            company_element = internship_container.find("div", {"class": "company_name"})
            company = company_element.find("a").get_text(strip=True) if company_element else "NA"

            location_element = internship_container.find("a", {"class": "location_link"})
            location = location_element.get_text(strip=True) if location_element else "NA"

            item_bodies = internship_container.find_all("div", {"class": "item_body"})
            start_date = item_bodies[0].get_text(strip=True) if item_bodies else "NA"
            duration = item_bodies[1].get_text(strip=True) if len(item_bodies) > 1 else "NA"

            stipend_element = internship_container.find("span", {"class": "stipend"})
            stipend = stipend_element.get_text(strip=True) if stipend_element else "NA"

            status_container = internship_container.find("div", {"class": "status-container"})
            status_text = status_container.find("div", {"class": "status"}).text.strip() if status_container else "NA"

            internship_data = {
                "id": internship_id,
                "job Title": job_title,
                "company": company,
                "link": link,
                "location": location,
                "start Date": start_date,
                "duration": duration,
                "stipend": stipend,
                "posted_time": self.convert_freshness_to_posted_date(status_text.lower())
            }

            return internship_data
        except Exception as e:
            logger.error(f"Error processing internship: {str(e)}")
            return None

    def extract_internships_from_html(self, html_text):
        try:
            soup = BeautifulSoup(html_text, 'html.parser')
            internship_containers = soup.find_all("div", {"class": "individual_internship"})
            data = [self.extract_internship_data(container, container.get("internshipid")) for container in internship_containers]
            return [item for item in data if item]
        except Exception as e:
            logger.exception(f"An error occurred while extracting internships: {str(e)}")
            return []

    def save_jobs_to_json(self, job_details, filename='internship_job_data.json'):
        with open(filename, 'w') as json_file:
            json.dump(job_details, json_file, indent=2)
        print(f"Job details saved to {filename}")

    def load_jobs_from_json(self, filename='internship_job_data.json'):
        if os.path.exists(filename):
            with open(filename, 'r') as json_file:
                job_details = json.load(json_file)
            return job_details
        else:
            print(f"{filename} not found. Returning an empty list.")
            return []

    def filter_jobs_by_freshness(self, job_details, max_days):
        today = datetime.datetime.now()
        return [job for job in job_details if (today - datetime.datetime.strptime(job['posted_time'], '%Y-%m-%d')).days <= max_days]

    def delete_old_entries(self, job_details, max_days):
        today = datetime.datetime.now()
        return [job for job in job_details if (today - datetime.datetime.strptime(job['posted_time'], '%Y-%m-%d')).days <= max_days]

    def update_and_save_jobs(self, max_days=30, sort=False):
        job_details = self.load_jobs_from_json()
        new_job_details = self.getInternshipList()

        if sort:
            new_job_details = self.sortByStipend(new_job_details)

        new_unique_jobs = [job for job in new_job_details if job not in job_details]
        updated_job_details = self.delete_old_entries(job_details + new_unique_jobs, max_days)

        print(updated_job_details)
        self.save_jobs_to_json(updated_job_details)
        return updated_job_details

    def sortByStipend(self, internships):
        for i in internships:
            salary_range = i['stipend']
            salary_range = self.parse_salary_string(salary_range)
            stipend_range = [0, 0]

            if salary_range:
                if salary_range != "Unpaid":
                    stipend_range = list(salary_range)

            i['stipend'] = stipend_range

        return sorted(internships, key=lambda internship: internship["stipend"][1], reverse=True)

    def getInternshipList(self):
        target_url = f'https://internshala.com/internships/android,android-app-development-internship/'
        response = requests.get(target_url)
        internships = self.extract_internships_from_html(response.text)
        return internships

    def sortByDate(self, internships):
        return sorted(internships, key=lambda internship: internship["posted_time"], reverse=True)


    def parse_salary_string(self, salary_string):
        salary_string = salary_string.replace(",", "")

        if "Unpaid" in salary_string:
            return "Unpaid"

        match = re.match(r"₹\s*(?P<lower>\d+)-(?P<upper>\d+)\s*/month", salary_string)
        if match:
            return int(match.group("lower")), int(match.group("upper"))

        match = re.match(r"₹\s*(?P<amount>\d+)\s*/month", salary_string)
        if match:
            amount = int(match.group("amount"))
            return amount, amount

        return None

    def get_internships(self, sortDate = True, sortStipend = True):
        internships = self.getInternshipList()
        if (sortStipend):
            internships = self.sortByStipend(internships)

        if (sortDate): internships = self.sortByDate(internships)
        return internships




if __name__ == "__main__":
    extractor = InternshipExtractor()
    # extractor.update_and_save_jobs()

    internship = extractor.load_jobs_from_json()

