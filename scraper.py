from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def write_to_file(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        for faculty_info in data:
            file.write(f"{faculty_info}\n")


# Send an HTTP GET request to the faculty directory page
url = "https://csd.cmu.edu/people/faculty"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing faculty information
    faculty_table = soup.find('tbody')

    # Initialize lists to store faculty data
    faculty_names = []
    faculty_urls = []
    faculty_courses = []
    faculty_bios = []

    # Loop through the rows in the table to extract faculty information
    for row in faculty_table.find_all('tr')[0:]:  # Skip the header row
        columns = row.find_all('td')
        if len(columns) >= 2:
            faculty_name = columns[0].text.strip()
            faculty_homepage_url = columns[0].find('a')['href']

            if not faculty_homepage_url.startswith('http'):
                faculty_homepage_url = urljoin(url, faculty_homepage_url)

            faculty_names.append(faculty_name)
            faculty_urls.append(faculty_homepage_url)

            # Visit the faculty's homepage URL to scrape additional information, including bio
            faculty_homepage_response = requests.get(faculty_homepage_url)
            if faculty_homepage_response.status_code == 200:
                faculty_homepage_soup = BeautifulSoup(faculty_homepage_response.text, 'html.parser')

                # Find the <article> tag with class 'person-full'
                faculty_bio_article = faculty_homepage_soup.find('article', class_='person-full')

                faculty_Course_div = faculty_bio_article.find('div', class_='views-element-container')

                if faculty_Course_div:
                    faculty_Course = "\n".join([p.text.strip() for p in faculty_Course_div.find_all('p')])
                else:
                    faculty_Course = "Courses not found"

                # Find the <h2>Teaching/Research Statement</h2> section
                teaching_research_statement = faculty_bio_article.find('h2')

                # Find the first <p> tag after the <h2>Teaching/Research Statement</h2>
                if teaching_research_statement:
                    first_paragraph_after_statement = teaching_research_statement.find_next('p')
                    if first_paragraph_after_statement:
                        faculty_bio = first_paragraph_after_statement.text.strip()
                    else:
                        faculty_bio = "Bio not found"
                else:
                    faculty_bio = "Bio not found"

                faculty_courses.append(faculty_Course)
                faculty_bios.append(faculty_bio)

    # Now you have lists with faculty data (names, URLs, courses, and bios)

    # Save faculty names into a text file
    write_to_file('faculty_names.txt', faculty_names)

    # Save faculty URLs into a text file
    write_to_file('faculty_urls.txt', faculty_urls)

    # Save faculty courses into a text file
    write_to_file('faculty_courses.txt', faculty_courses)

    # Save faculty bios into a text file
    write_to_file('faculty_bios.txt', faculty_bios)

else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
