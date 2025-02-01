import requests
from bs4 import BeautifulSoup
import pandas as pd
import ssl

print(ssl.OPENSSL_VERSION)

# URL of Remote OK's job listings page (you can modify for pagination or filters)
url = 'https://remoteok.com/?location=US'

# Send a GET request to the URL
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all job listings
job_cards = soup.find_all('tr', class_='job')

# Prepare lists to store extracted data
job_titles = []
companies = []
job_links = []

# Loop through each job listing and extract data
for job_card in job_cards:
    title_tag = job_card.find('h2', class_='job-title')
    company_tag = job_card.find('span', class_='company')
    link_tag = title_tag.find('a', href=True) if title_tag else None

    # Extract job title, company name, and job link
    if title_tag and company_tag and link_tag:
        job_titles.append(title_tag.text.strip())
        companies.append(company_tag.text.strip())
        job_links.append(link_tag['href'])

# Create a pandas DataFrame for better structure
job_data = pd.DataFrame({
    'Job Title': job_titles,
    'Company': companies,
    'Job Link': job_links
})

# Print the result
print(job_data)

# Optionally, save the data to a CSV file
job_data.to_csv('remote_jobs.csv', index=False)
