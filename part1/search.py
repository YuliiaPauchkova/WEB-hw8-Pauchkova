from mongoengine import Document, StringField, ListField, ReferenceField, connect, queryset_manager
from mongoengine.queryset.visitor import Q

connect(
    db='database',
    host='mongodb+srv://new1:2312@database.9kdee0f.mongodb.net/',
)

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, required=True) 
    quote = StringField()

    @queryset_manager
    def search_quotes(doc_cls, queryset, query):
        return queryset.filter(Q(tags=query) | Q(author=Author.objects(fullname=query).first()))

def search_quotes(query):
    quotes = Quote.search_quotes(query)
    for quote in quotes:
        print(f'Цитата: {quote.quote}')
        print(f'Автор: {quote.author.fullname}')
        print(f'Теги: {quote.tags}')
        print()

while True:
    command = input("Введіть команду (tag, author або tags): ")
    if command:
        parts = command.split(':')
        if len(parts) == 2:
            key, value = parts[0].strip(), parts[1].strip()
            if key == 'tag':
                search_quotes(value)
            elif key == 'author':
                search_quotes(value)
            elif key == 'tags':
                tags = value.split(',')
                for tag in tags:
                    search_quotes(tag.strip())
            else:
                print("Невірна команда. Спробуйте ще раз.")
    else:
        print("Будь ласка, введіть команду.")
