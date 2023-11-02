import requests
from bs4 import BeautifulSoup
import datetime
import sys
import io
import contextlib
import pandas as pd
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin  # Import urljoin from urllib.parse

# Function to validate the URL against the robots.txt file
def validate_url(url):
    rp = RobotFileParser()
    rp.set_url(urljoin(url, '/robots.txt'))  # Use urljoin to construct the full URL
    rp.read()
    return rp.can_fetch("*", url)

# Prompt the user for the URL they want to scrape
url = input("Enter the URL you want to scrape: ")

# Validate the user-provided URL
if not validate_url(url):
    print("This URL is not allowed for scraping according to robots.txt.")
    sys.exit(1)

# Function to extract and log data
def extract_and_log_data(soup):
    data = {}
    data["title"] = soup.find('title').text if soup.find('title') else "Title not found on the page."
    data["headings"] = [heading.text for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    data["paragraphs"] = [paragraph.text for paragraph in soup.find_all('p')]
    data["image_sources"] = [image.get('src') for image in soup.find_all('img')]
    data["all_text_data"] = [text for text in soup.stripped_strings]
    data["console_log_messages"] = []
    data["css_styles"] = []
    data["links"] = []
    data["file_downloads"] = []
    data["scripts"] = []

    # Capture and save the content of the website's console log to the data
    with contextlib.redirect_stdout(io.StringIO()) as console_output:
        try:
            with requests.get(url) as r:
                r.raise_for_status()
        except requests.exceptions.RequestException as e:
            data["console_log_messages"].append(f"Request Exception: {e}")
        print("Console log messages:")
        console_output = console_output.getvalue()
        data["console_log_messages"].append(console_output)

    # Extract and log CSS styles
    style_tags = soup.find_all('style')
    data["css_styles"] = [style.text for style in style_tags]

    # Extract and log links
    links = [link.get('href') for link in soup.find_all('a')]
    data["links"] = links

    # Extract and log file download links
    file_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith(('.pdf', '.doc', '.xls'))]
    data["file_downloads"] = file_links

    # Extract and log JavaScript scripts
    script_tags = soup.find_all('script')
    for script in script_tags:
        script_link = script.get('src')
        if script_link is not None:
            data["scripts"].append(script_link)

    return data

# Send an HTTP GET request to the URL
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Request Exception: {e}")
    sys.exit(1)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract and log data
    data = extract_and_log_data(soup)

    # Save the entire webpage content to a local HTML file
    with open("webpage_content.html", "w", encoding="utf-8") as file:
        file.write(response.text)

    # Save the data to a text file
    with open("scraped_data.log", "a", encoding="utf-8") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"Timestamp: {timestamp}\n")
        log_file.write(f"Title: {data['title']}\n")
        log_file.write("Headings on the Page:\n")
        for heading_text in data["headings"]:
            log_file.write(heading_text + '\n')
        log_file.write("Paragraphs on the Page:\n")
        for paragraph_text in data["paragraphs"]:
            log_file.write(paragraph_text + '\n')
        log_file.write("Image Sources on the Page:\n")
        for image_src in data["image_sources"]:
            log_file.write(image_src + '\n')
        log_file.write("All Text Data:\n")
        for text in data["all_text_data"]:
            log_file.write(text + '\n')
        log_file.write("Webpage content saved to 'webpage_content.html'\n")
        if data["console_log_messages"]:
            log_file.write("Console log messages:\n")
            for message in data["console_log_messages"]:
                log_file.write(message + '\n')
        if data["css_styles"]:
            log_file.write("CSS Styles:\n")
            for css_style in data["css_styles"]:
                log_file.write(css_style + '\n')
        log_file.write("Links on the Page:\n")
        for link in data["links"]:
            log_file.write(link + '\n')
        log_file.write("File Downloads:\n")
        for file_link in data["file_downloads"]:
            log_file.write(file_link + '\n')
        log_file.write("JavaScript Scripts:\n")
        for script_link in data["scripts"]:
            log_file.write(script_link + '\n')
        log_file.write("\n")

    print("Data scraped and saved to 'scraped_data.log', 'webpage_content.html', and 'console.log'")

else:
    print("Failed to retrieve the web page. Status code:", response.status_code)
