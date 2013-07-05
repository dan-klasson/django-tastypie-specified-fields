django-tastypie-specified-fields
================================

With this extension you can do the following:

    curl -H "Accept: application/json" http://127.0.0.1:8000/api/v1/book/?fields=title,publication_date,publisher__name
    
Which produces something like:
    
       "objects": [
        {
          "publication_date": "1983-07-04",
          "publisher__name": "Viking Press",
          "resource_uri": "/api/v1/book/1/",
          "title": "Misery"
        },
        {
          "publication_date": "1945-08-17",
          "publisher__name": "Penguin Press",
          "resource_uri": "/api/v1/book/2/",
          "title": "Animal Farm"
        },
        {
          "publication_date": "1949-06-08",
          "publisher__name": "Penguin Press",
          "resource_uri": "/api/v1/book/3/",
          "title": "1984"
        }
      ]

And yields the following two queries:

    SELECT COUNT(*) FROM "app_book"

    SELECT "app_book"."id", "app_book"."title", "app_book"."publisher_id", "app_book"."publication_date", "app_publisher"."id", "app_publisher"."name" 
    FROM "app_book" 
    INNER JOIN "app_publisher" ON ("app_book"."publisher_id" = "app_publisher"."id") 
    LIMIT 20
    
You can also filter on m2m relations:

    curl -H "Accept: application/json" http://127.0.0.1:8000/api/v1/book/?fields=title,publication_date,publisher__name&author=1

### Demo

There is an example project included you can play around with. The password is `demo/demo`.

### TODO

* Support multiple levels in depth for related fields
* Make it support m2m fields


    
