import io

from django.test import TestCase
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetSerializer


def printh(header):
    print('\n')
    return('-'*len(header) + '\n|' + header + '|\n' + '-'*len(header))


class SnippetTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.snippet = Snippet.objects.create(code='print("hello, world")\n') 
        cls.snippet2 = Snippet.objects.create(code='foo = "bar"\n')
        cls.serializer = SnippetSerializer(cls.snippet)
        cls.content = JSONRenderer().render(cls.serializer.data)

    def test_get_snippet_model(self):
        snippet = Snippet.objects.get(code='print("hello, world")\n')
        snippet2 = Snippet.objects.get(code='foo = "bar"\n')

    def test_serialize_snippet_model(self):
        printh("MODEL SERIALIZATION")
        print(self.serializer.data)

    def test_render_snippet_model(self):
        printh("SERIALIZED MODEL RENDER")

        print(self.content)

    def test_deserialize_snippet_model(self):
        printh("MODEL DESERIALIZATION")
        stream = io.BytesIO(self.content)
        print("Steam", stream)
        data = JSONParser().parse(stream)
        print("Data:", data)
        serializer = SnippetSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True)
        # self.assertEqual(serializer.validated_data, 
        #     dict([
        #         ('title', ''), ('code', 'print("hello, world")\n'),
        #         ('linenos', False), ('language', 'python'), ('style', 'friendly')
        #     ])
        # )
        serializer.save()
    
    def test_serialize_queryset(self):
        printh("QUERY SERIALIZATION")
        serializer = SnippetSerializer(Snippet.objects.all(), many=True)
        print(serializer.data)
        # self.assertEqual(serializer.data,
        #     [dict([('id', 1), ('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), dict([('id', 2), ('title', ''), ('code', 'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]
        # )


