import requests
from bs4 import BeautifulSoup
import datetime
import sys
import io
import contextlib
import csv
import json
from urllib.parse import urljoin
from urllib.parse import urlparse

def validate_links(links, base_url):
    validated_links = []
    parsed_base_url = urlparse(base_url)

    for link in links:
        if not link:
            continue

        parsed_link = urlparse(link)
        if not parsed_link.netloc:
            # Handle relative links
            absolute_link = urljoin(base_url, link)
        else:
            absolute_link = link

        if parsed_base_url.netloc == parsed_link.netloc:
            # Only include links with the same domain as the base URL
            validated_links.append(absolute_link)

    return validated_links

# Function to extract and log data
def extract_and_log_data(soup, url):
    data = {}
    data["title"] = soup.find('title').text if soup.find('title') else "Title not found on the page."
    data["headings"] = [heading.text for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    data["paragraphs"] = [paragraph.text for paragraph in soup.find_all('p')]
    data["image_sources"] = [image.get('src') for image in soup.find_all('img')]
    data["all_text_data"] = [text for text in soup.stripped_strings]
    data["console_log_messages"] = []

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
    data["scripts"] = [script.get('src') for script in script_tags]

    # Validate and clean links
    data["validated_links"] = validate_links(links, url)

    # Get HTML content
    data["html_content"] = str(soup)

    return data

# Function to export data
def export_data(data, export_format):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"scraped_data_{timestamp}.{export_format}"
    if export_format == "json":
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    elif export_format == "csv":
        with open(filename, "w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            for key, value in data.items():
                writer.writerow([key, value])
    elif export_format == "html":
        with open(filename, "w", encoding="utf-8") as html_file:
            html_file.write(data["html_content"])


def scrape_website(url, export_format):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        sys.exit(1)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        data = extract_and_log_data(soup, url)
        export_data(data, export_format)
        print(f"Data scraped and saved to 'scraped_data.{export_format}'.")
    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)

if __name__ == "__main__":
    url = input("Enter the URL you want to scrape: ")
    export_format = input("Enter the export format (json, csv, or html): ").lower()

    if export_format not in ["json", "csv", "html"]:
        print("Invalid export format. Please use 'json', 'csv', or 'html'.")
    else:
        scrape_website(url, export_format)
