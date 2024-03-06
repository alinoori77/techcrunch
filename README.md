TechCrunch Scraper
This Python script scrapes articles from TechCrunch's API and stores them in a PostgreSQL database. It retrieves information such as the article title, author, publication date, keywords, media URL, and category.

Prerequisites
Python 3.x
PostgreSQL
Required Python packages (peewee, requests)
Setup
Install Python 3.x from python.org.
Install PostgreSQL from postgresql.org.
Install required Python packages using pip install -r requirements.txt.
Configure database connection details in sample_settings.py.
Usage
Run the script by executing python your_script_name.py.
The script will scrape articles from TechCrunch's API based on predefined categories and store them in the configured PostgreSQL database.
Configuration
Modify the category_dict dictionary to include desired categories and their corresponding IDs.
Adjust the range of pages to scrape within the loop (range(1, 200)).
Ensure that database connection details in sample_settings.py are accurate.
Structure
Category: Represents article categories.
Author: Represents article authors.
Post: Represents individual articles with title, category, and author.
Keywords: Represents keywords associated with articles.
Keywords_to_post: Represents the relationship between keywords and articles.
Error Handling
The script catches exceptions and prints any errors that occur during execution.
Cleanup
The database connection is closed after execution.
Note
It's recommended to use this script responsibly and in accordance with TechCrunch's API usage policy.
Ensure that you're complying with TechCrunch's terms of service and data usage policies when scraping their content.
This script serves as a basic example and may require modifications for production use or integration into larger projects.
