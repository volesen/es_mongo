from mongoengine import Document, StringField, BooleanField
from mongoengine_searchable import SearchableMixin, searchable


@searchable
class Todo(SearchableMixin, Document):
    __searchable__ = ['title', 'description']

    title = StringField(required=True)
    description = StringField()
    completed = BooleanField(default=False)

    meta = {
        'collection': 'test',
        'indexes': [{

            'fields': ['$title', '$description'],
            'default_language': 'english'
        }]
    }
