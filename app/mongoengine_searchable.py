
from flask import current_app
from mongoengine import signals


def format_index(index):
    # Index must be lowercase
    return index.lower()


def add_to_index(index, document):
    index = format_index(index)

    # Build paylad
    payload = {}
    for field in document.__searchable__:
        payload[field] = getattr(document, field)

    # Add payload to index
    current_app.es.index(
        index=index, doc_type=index, id=str(document.id), body=payload)


def remove_from_index(index, document):
    index = format_index(index)

    current_app.es.delete(index=index, doc_type=index, id=str(document.id))


def query_index(index, query, page=1, per_page=10):
    index = format_index(index)

    search = current_app.es.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})

    results = [hit['_source'] for hit in search['hits']['hits']]

    return results


class SearchableMixin(object):
    '''
    Mixin class for Mongoengine docuemnts to
    allow search and indexing in Elasticsearch
    '''
    @classmethod
    def search(cls, expression, page=1, per_page=10):
        return query_index(cls.__name__, expression, page, per_page)

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        add_to_index(cls.__name__, document)

    @classmethod
    def post_bulk_insert(cls, sender, documents, **kwargs):
        for document in documents:
            add_to_index(cls.__name__, document)

    @classmethod
    def post_delete(cls, sender, document, **kwargs):
        remove_from_index(cls.__name__, document)

    @classmethod
    def reindex(cls):
        for document in cls.objects:
            add_to_index(cls.__name__, document)


def searchable(cls):
    '''
    Decorator to class register signal handlers
    '''

    signals.post_save.connect(cls.post_save, sender=cls)

    signals.post_bulk_insert.connect(cls.post_bulk_insert, sender=cls)

    signals.post_delete.connect(cls.post_delete, sender=cls)

    return cls
