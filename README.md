# FTS with Mongoengine and Elasticsearch

This is an example of full text search with ES as an auxillary database for Mongoengine, inspired by this [blogpost](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-full-text-search).

Contrary to most examples, this webapp serves the models saved on Elasticsearch, rather than get the ids, to fetch models in the main database. 

The document name is used as an index in Elasticsearch.

```shell
$ git clone https://github.com/volesen/es_mongo.git
$ cd es_mongo
$ docker-compose up
$ pipenv shell
$ python app/app.py
```