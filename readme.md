# Web Scraper

This is a Python web scraping tool that extracts various types of data from a specified website. The extracted data can be saved in JSON, CSV, or HTML format.

## Features

1. **Data Extraction**: The scraper extracts the following data from a web page:
   - Title
   - Headings (h1 to h6)
   - Paragraphs
   - Image sources
   - All text data
   - CSS styles
   - Links
   - File download links (PDFs, DOCs, XLS files)
   - JavaScript script sources

2. **Link Validation**: The tool validates and cleans links to ensure they are accessible and within the same domain as the base URL.

3. **HTML Content**: The HTML content of the page is saved in the exported files.

4. **Export Formats**: You can save the extracted data in the following formats:
   - JSON
   - CSV
   - HTML
   -

 ## Bug Fixes

- **Fixed HTML Export**: The HTML content of the web page is now correctly saved when choosing the "HTML" export format. A bug that previously prevented it from saving has been resolved.

- **Error Handling**: Robust error-handling mechanisms have been implemented to gracefully handle various exceptions that might occur during scraping.

- **CSS Styles Bug**: Previously, certain CSS styles were not being extracted correctly. This issue has been fixed.

- **Link Validation Bug**: There was an issue with link validation where some links were not correctly validated. This bug has been addressed.


## Upcoming Features

We have exciting features in the pipeline, including:

1. **Batch Processing**: Enable batch processing of multiple URLs or websites in a single run.

2. **Custom Headers**: Provide the ability to specify custom headers for HTTP requests, useful for mimicking different user agents or providing specific headers as needed.

3. **Visual Scraping**: Incorporate a visual scraping tool that lets users click on elements to select data for extraction.

4. **Data Export Options**: Provide more options to export scraped data, such as exporting to a database.

Stay tuned for these upcoming enhancements!


## Getting Started

Follow these steps to get started with the web scraping project:

1. Starting the programm

   ```bash
   python scrapper.py

2. Install requirements
   
   ```bash
   pip install requests beautifulsoup4

## Rules

-Legal Use: Do not use this program for any illegal or unethical activities.
-Respect Licensing: Comply with the terms of the project's MIT License.
-Ethical Scraping: Follow ethical scraping practices, including respecting the robots.txt file of websites.
-User Privacy: Be respectful of user privacy and data. Do not collect sensitive or personal information without consent.


## Licence
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM,
OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


