import peewee
import requests
from peewee import IntegrityError
from database_manager import DatabaseManager
from datetime import timedelta


from celery import Celery
app = Celery('tasks', broker='amqp://localhost')

app.conf.beat_schedule = {
    'create-folder-every-2-minutes': {
        'task': 'mainscraper.scrape',
        'schedule': timedelta(hours=24),
    },
}


import sample_settings

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


@app.task
def scrape():

    try:
        
        category_dict={"20429":"startup" , "577030455":"venture" ,"577047203":"security" ,"577047203":"ai" ,"576601119":"crypto" , "577051039":"apps"}
       
        for categoryy in  category_dict :
            print(f"start scarping category {categoryy}")
            for page in range(1,200):
                print(f"page{page}")
                database_manager.create_tables(models=[Category,Author, Post , Keywords , Keywords_to_post])
                url =f"https://techcrunch.com/wp-json/tc/v1/magazine?page={page}&_embed=true&_envelope=true&categories={categoryy}"
                
                response = requests.get(url)
                json_data = response.json()
                print(page)
                print(categoryy)
                print(url)
                for i in range(20):  
                    content = {"data" : json_data["body"][i]["date"],
                            "link" :json_data["body"][i]["link"],
                            "title" :json_data["body"][i]["title"].get("rendered"),
                            "author" :json_data["body"][i]["yoast_head_json"].get("author"),
                            "keywords" :json_data["body"][i]["yoast_head_json"].get("schema").get("@graph")[0].get("keywords"),
                            "media URL" : json_data["body"][i]["yoast_head_json"].get("og_image")[0].get("url"),
                            "category" :json_data["body"][i]["yoast_head_json"].get("schema").get("@graph")[0].get("articleSection"),

                        }
                
                    author, _ = Author.get_or_create(title=content["author"])
                
                    category, _ = Category.get_or_create(title=category_dict[categoryy])

                    Post_create, _ = Post.get_or_create(title=content["title"], category=category, Author=author )
                                        
                    if content["keywords"] :
                        for i in content["keywords"]:
                            keyword , _ = Keywords.get_or_create(title=i)
                            Keywords_to_post.get_or_create(post_keyword=Post_create , keyword_post=keyword)


    except Exception as error:
        print("Error", error)
    finally:
        # closing database connection.
        if database_manager.db:
            database_manager.db.close()
            print("Database connection is closed")
