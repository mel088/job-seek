import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


# Function to fetch the job details from a single job page
def get_job_details(job_url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
        }
        time.sleep(15)
        response = requests.get(job_url, headers=headers)
        if response.status_code != 200:
            return print(f"Error {response.status_code}: Could not retrieve page.")
        job = BeautifulSoup(response.text, "html.parser")

        job_title = job.find("h2", itemprop="title")
        if job_title:
            job_title = job_title.get_text(strip=True)

        # Extract Company Name
        company_name = job.find("h3", itemprop="name")
        if company_name:
            company_name = company_name.get_text(strip=True)

        # TODO: # Extract Days Posted Ago
        # time_element = job.find('td', class_='time').find('time')
        # datetime_str = time_element.get('datetime')
        # if days_posted:
        #     days_posted = days_posted.get_text(strip=True)

        # Extract Job Location (from <div class="location">)
        location = job.find("div", class_="location")
        if location:
            location = location.get_text(strip=True)

        # Extract Salary (from <div class="location tooltip">)
        salary = job.find("div", class_="location tooltip")
        if salary:
            salary = salary.get_text(strip=True)

        # Extract Years of Experience
        markdown_div = job.find("div", class_="markdown")
        matches = []
        if markdown_div:
            text = markdown_div.get_text()
            matches = re.findall(r"(\d+(?:\+?)?)\s*years?", text, re.IGNORECASE)
            if matches:
                print("Found mentions of years of experience:")
                for match in matches:
                    print(match)

        # Collect all extracted details in a dictionary
        job_details = {
            "job_title": job_title,
            "company_name": company_name,
            # "description": description_text,
            # "experience": years_of_experience,
            "location": location,
            "salary": salary,
            # "benefits": benefits,
            # "employment_type": employment_type,
            "job_url": job_url,
            "years_experience": matches,
        }
        return job_details

    except Exception as e:
        print(f"Error fetching details for {job_url}: {e}")
        return None


# Function to fetch job listings from a job board page (e.g., RemoteOK)
def get_job_listings(board_url):
    try:
        # Use a common User-Agent string to mimic a Chrome browser on macOS to pass bot through
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
        }
        time.sleep(10)
        response = requests.get(board_url, headers=headers)
        if response.status_code != 200:
            return print(f"Error {response.status_code}: Could not retrieve page.")
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all job links on the page
        job_links = []
        job_elements = soup.find_all(
            "tr", class_=lambda x: x and "expand" in x
        )  # Look for <tr> tags with 'expand' class
        for job in job_elements:
            job_id = job.get("class")[1].split("-")[1]
            if job_id:
                job_url = "https://remoteok.com/remote-jobs/" + job_id  # Full URL
                job_links.append(job_url)
        return job_links

    except Exception as e:
        print(f"Error fetching job listings: {e}")
        return []


# Main function to search multiple jobs and store details in a DataFrame
def search_multiple_jobs(board_url):
    job_links = get_job_listings(board_url)
    if not job_links:
        print("No job listings found.")
        return None

    # List to store all the job details
    job_data = []

    # Loop through all job links and fetch their details
    for job_url in job_links:
        job_details = get_job_details(job_url)
        if job_details:
            job_data.append(job_details)

    # Convert the list of job details into a DataFrame
    if job_data:
        job_df = pd.DataFrame(job_data)
        return job_df
    else:
        print("No job details found.")
        return None


if __name__ == "__main__":
    # Example usage: Replace this URL with the page listing multiple jobs
    job_board_url = "https://remoteok.com/remote-marketing-jobs?location=US"
    job_df = search_multiple_jobs(job_board_url)

    # If we found jobs, save to CSV or display the DataFrame
    if job_df is not None:
        print(job_df.head())  # Display first few rows of the DataFrame
        job_df.to_csv("job_listings.csv", index=False)  # Save to CSV
