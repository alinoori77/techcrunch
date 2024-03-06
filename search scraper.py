import argparse
import peewee
import requests
from peewee import IntegrityError
from database_manager import DatabaseManager
from time import sleep
from bs4 import BeautifulSoup
import sample_settings
import os  # Importing os module for interacting with the operating system
from datetime import datetime  # Importing datetime for working with dates and times
import argparse  # Importing argparse for parsing command-line arguments
import pandas as pd



database_manager = DatabaseManager(
    database_name=sample_settings.DATABASE['name'],
    user=sample_settings.DATABASE['user'],
    password=sample_settings.DATABASE['password'],
    host=sample_settings.DATABASE['host'],
    port=sample_settings.DATABASE['port'],
)

class Category(peewee.Model):
    title = peewee.CharField(max_length=2048, null=False, verbose_name='Title')

    class Meta:
        database = database_manager.db

class Author(peewee.Model):
    title = peewee.CharField(max_length=1024, null=False, verbose_name='Author')

    class Meta:
        database = database_manager.db

class Post(peewee.Model):
    title = peewee.CharField(max_length=2048, null=False, verbose_name='Title')
    category = peewee.ForeignKeyField(model=Category, null=False, verbose_name='Category')
    Author = peewee.ForeignKeyField(model=Author, null=False, verbose_name='Author')

    class Meta:
        database = database_manager.db

class Keywords(peewee.Model):
    title = peewee.CharField(max_length=1024, null=False, verbose_name='Title')

    class Meta:
        database = database_manager.db

class Keywords_to_post(peewee.Model):
    post_keyword = peewee.ForeignKeyField(model=Post, null=False, verbose_name='Post')
    keyword_post = peewee.ForeignKeyField(model=Keywords, null=False, verbose_name='Keywords')

    class Meta:
        database = database_manager.db


class search_result(peewee.Model):
    title = peewee.CharField(max_length=1024, null=False, verbose_name='title')
    key_word = peewee.CharField(max_length=1024, null=False, verbose_name='key_word')
    author = peewee.CharField(max_length=1024, null=False, verbose_name='author')

    class Meta:
        database = database_manager.db





def export_data(format, title2):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Getting current date and time
    folder_name = f"{current_time}_{title2}"  # Creating folder name based on current time and book name
    os.makedirs(folder_name, exist_ok=True)  # Creating folder to store exported files


    # Exporting data based on the specified format
    if format == 'xls':

        # Fetch data from the database where post title
        query = search_result.select().where(search_result.key_word == title2)

        # Convert the query result to a pandas DataFrame
        df = pd.DataFrame(list(query.dicts()))

        # Export DataFrame to an Excel file
        df.to_excel(os.path.join(folder_name, f"{title2}.xlsx"), index=False)

        # Close the database connection
        database_manager.db.close()

    elif format == 'json':

        # Fetch data from the database where post title 
        query = search_result.select().where(search_result.key_word == title2)

        # Convert the query result to a pandas DataFrame
        df = pd.DataFrame(list(query.dicts()))

        # Export DataFrame to an Excel file
        df.to_json(os.path.join(folder_name, f"{title2}.json"), index=False)

        # Close the database connection
        database_manager.db.close()
        
    elif format == 'csv':

        # Fetch data from the database where post 
        query = search_result.select().where(search_result.key_word == title2)
        # Convert the query result to a pandas DataFrame
        df = pd.DataFrame(list(query.dicts()))

        # Export DataFrame to an Excel file
        df.to_csv(os.path.join(folder_name, f"{title2}.csv"), index=False)

        # Close the database connection
        database_manager.db.close()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search TechCrunch for a specific word and export the data.')
    parser.add_argument('word', type=str, help='The word to search for on TechCrunch')
    parser.add_argument("export_format", type=str, choices=['xls', 'json', 'csv'], help="Export format (xls/json/csv)")

    args = parser.parse_args()
    word = args.word
    format= args.export_format
    try:
        all_titles = list()
        all_authors = list()
        for page in range(20):
            url = f"https://search.techcrunch.com/search;?p={word}&b={page}1"
            response = requests.get(url)
            print(f"scrape page {page}")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                titles = soup.find_all("a", class_="fz-20 lh-22 fw-b")
                authors = soup.find_all("span", class_="mr-15")

                if len(titles) == 0:
                    break  # No more results, exit the loop

                for title in titles:
                    all_titles.append(title.get_text(strip=True))

                for author in authors:
                    all_authors.append(author.get_text(strip=True))
            else:
                print("Failed to retrieve page", page)
                break

        database_manager.create_tables(models=[search_result])
        for title, author in zip(all_titles, all_authors):
            search__result , _ = search_result.get_or_create(title=title ,key_word=word, author=author )                


        export_data(format, word)


    except Exception as error:
        print("Error", error)
    finally:
        # closing database connection.
        if database_manager.db:
            database_manager.db.close()
            print("Database connection is closed")
