from tastypie import fields
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from models import *
from specifiedfields import SpecifiedFields
from tastypie.api import Api
from serializers import PrettyJSONSerializer

api = Api(api_name='v1')

class PublisherResource(SpecifiedFields):
    class Meta:
        queryset = Publisher.objects.all()
        serializer = PrettyJSONSerializer()

api.register(PublisherResource())

class LanguageResource(SpecifiedFields):
    class Meta:
        queryset = Language.objects.all()
        serializer = PrettyJSONSerializer()
api.register(LanguageResource())

class AuthorResource(SpecifiedFields):
    language = fields.ForeignKey(LanguageResource, 'language')

    class Meta:
        queryset = Author.objects.all()
        serializer = PrettyJSONSerializer()
        filtering = {
            'language': ALL,
        }
api.register(AuthorResource())

class BookResource(SpecifiedFields):
    publisher = fields.ForeignKey(PublisherResource, 'publisher')
    author = fields.ManyToManyField(AuthorResource, 'author', related_name='author')
    class Meta:
        queryset = Book.objects.all()
        serializer = PrettyJSONSerializer()
        filtering = {
            'publisher': ALL,
            'author': ALL_WITH_RELATIONS,
        }

api.register(BookResource())


