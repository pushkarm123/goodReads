from goodreads import client

gc = client.GoodreadsClient("bGWIjisPFyumZuoaqIHcA", "8vqct0BaeV8hXBC8qPPCpmFFdTKcRsrGDK7tjusiQ")
book = gc.book(100)

print book.title
print book.authors[0].name.encode('utf-8')