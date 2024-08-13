import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# List of URLs to scrape
urls = [
    "https://talentedge.com/iim-raipur/executive-certificate-program-in-digital-finance",
    "https://talentedge.com/iim-raipur/executive-certificate-program-in-general-management",
    "https://talentedge.com/iim-raipur/post-graduate-executive-certification-in-human-resource-management-iimr-hr",
    "https://talentedge.com/iim-raipur/executive-certificate-program-in-digital-marketing-course",
    "https://talentedge.com/iim-raipur/certificate-course-machine-learning-for-managers",
    "https://talentedge.com/iim-raipur/certificate-course-strategic-management",
    "https://talentedge.com/iim-raipur/certificate-course-project-management",
    "https://talentedge.com/iim-raipur/certificate-course-project-management",
    "https://talentedge.com/iim-raipur/certificate-course-applied-financial-risk-management"
]

def scrape_course_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting data
    def safe_find(selector, class_name, multiple=False):
        try:
            if multiple:
                elements = soup.find_all(selector, class_=class_name)
                return ' '.join([element.get_text(strip=True) for element in elements])
            else:
                element = soup.find(selector, class_=class_name)
                return element.get_text(strip=True) if element else "Not Available"
        except AttributeError:
            return "Not Available"
    def extract_fees_inr(fees_html):
        # Use regex to find the first occurrence of a number in the INR section
        match = re.search(r'\d+(?:,\d{3})*(?:\.\d+)?', fees_html)
        return match.group(0) if match else "Not Available"       

    try:
        title = safe_find('h1', 'pl-title')
        description = safe_find('div', 'desc', multiple=True)  # Get all paragraphs
        what_you_will_learn = safe_find('div', 'pl-deeper-undstnd to_flex_ul', multiple=True)
        skills = safe_find('div', 'key-skills-sec', multiple=True)
        target_students = safe_find('h4', 'cs-titlec', multiple=True)
        prerequisites = safe_find('div', 'eligible-right-top-list', multiple=True)
        content = safe_find('li', 'sylab-tab-ul', multiple=True)
        faculty1_name = safe_find('h4', 'best-fname')
        faculty1_designation = safe_find('p', 'best-fdesingnation')
        institute_name = safe_find('h4', 'about-ititle')
        fees_inr_elements = soup.find_all('div', class_='program-details-total-pay-amt-right')
        fees_inr_html = ' '.join([element.get_text(strip=True) for element in fees_inr_elements])
        fees_inr = extract_fees_inr(fees_inr_html)
        # Print the details including the URL
        print({
            'url': url,
            'title': title,
            'description': description,
            'what_you_will_learn': what_you_will_learn,
            'skills': skills,
            'target_students': target_students,
            'prerequisites': prerequisites,
            'content': content,
            'faculty1_name': faculty1_name,
            'faculty1_designation': faculty1_designation,
            'institute_name': institute_name,
            'fees_inr': fees_inr,
        })

        return {
            'url': url,
            'title': title,
            'description': description,
            'what_you_will_learn': what_you_will_learn,
            'skills': skills,
            'target_students': target_students,
            'prerequisites': prerequisites,
            'content': content,
            'faculty1_name': faculty1_name,
            'faculty1_designation': faculty1_designation,
            'institute_name': institute_name,
            'fees_inr': fees_inr,
        }

    except Exception as e:
        print(f"Error extracting data from {url}: {e}")
        return {'url': url}

# List to hold all course details
course_data = []

# Loop through the list of URLs
for url in urls:
    course_details = scrape_course_details(url)
    course_data.append(course_details)

# Create DataFrame
df = pd.DataFrame(course_data)

# Save DataFrame to CSV
df.to_csv('course_details.csv', index=False)

print("Data saved to 'course_details.csv'")
