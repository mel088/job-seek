import json
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL of Remote OK's job listings page (you can modify for pagination or filters)
url = "https://remoteok.com/remote-marketing-jobs?location=US"

# Use a common User-Agent string to mimic a Chrome browser on macOS to pass bot through
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Send a GET request to the URL
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code != 200:
    print(f"Error {response.status_code}: Could not retrieve page.")

soup = BeautifulSoup(response.text, "html.parser")
# Find all job listings

job_titles = soup.find_all("h2", itemprop="title")
for job in job_titles:
    print(job.text.strip())

# List to hold job information
job_list = []

# Find all job rows in the table (adjust based on your page structure)
job_rows = soup.find_all(
    "tr", {"data-offset": True}
)  # Find job rows based on attribute

for job in job_rows:
    # Extract Job Title (from <h2 itemprop="title">)
    job_title = job.find("h2", itemprop="title")
    if job_title:
        job_title = job_title.get_text(strip=True)

    # Extract Job URL (from the href attribute of the <a> tag)
    job_url_tag = job.find("a", {"class": "preventLink"})
    job_url = "URL not found"
    if job_url_tag:
        job_url = "https://remoteok.com" + job_url_tag["href"]  # Full URL

    # Extract Company Name (from JSON inside <script> tag)
    script_tag = job.find("script", type="application/ld+json")
    company_name = "Company not found"
    if script_tag:
        job_data = json.loads(script_tag.string)  # Parse the JSON data
        company_name = job_data.get("hiringOrganization", {}).get(
            "name", "Company not found"
        )

    # Extract Job Location (from <div class="location">)
    location = job.find("div", class_="location")
    if location:
        location = location.get_text(strip=True)

    # Extract Salary (from <div class="location tooltip">)
    salary = job.find("div", class_="location tooltip")
    if salary:
        salary = salary.get_text(strip=True)

    # Extract Description for Experience Filtering
    description = job.find("div", class_="markdown")
    experience_text = ""
    if description:
        experience_text = description.get_text(strip=True)

    # Regex to match years of experience mentioned in the description
    experience_match = re.search(
        r"(\d+)\s*[\+\s]*years", experience_text, re.IGNORECASE
    )

    if experience_match:
        experience_years = int(experience_match.group(1))  # Extract the number of years

        # Only keep jobs that require 2 or fewer years of experience
        if experience_years > 2:
            continue  # Skip jobs requiring more than 2 years of experience

    # Add the job details to the list
    job_list.append(
        {
            "Job Title": job_title,
            "Company Name": company_name,
            "Location": location,
            "Salary": salary,
            "Job URL": job_url,
        }
    )

df = pd.DataFrame(job_list)

# Save the data to a CSV file
df.to_csv("remote_jobs.csv", index=False)
