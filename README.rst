Installation
============

Install requirements::

    pip install -r requirements.txt

Create .env file::

    mv sample.env .env

Run migrations::

    python manage.py migrate


Running Tests
==============

::

    make test


Running Server
==============

::

    python manage.py runserver


Endpoints
=========

Creating a new brand
--------------------

Request::

    $ curl -X POST http://127.0.0.1:8000/brands \
      -H "Content-Type: application/json"
      -d '{
        "name": "Apple"
      }'

Response::

    Status: 201 OK

    {
      "id": "01234567-89ab-cdef-0123-456789abcdef",
      "name": "Apple",
      "created": "2015-05-14T02:46:40.537882Z",
      "updated": "2015-05-14T02:46:40.537882Z"
    }


Listing all brands
------------------

Request::

    $ curl http://127.0.0.1:8000/brands

Response::

    Status: 200 OK

    [
      {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "name": "Apple",
        "created": "2015-05-14T02:46:40.537882Z",
        "updated": "2015-05-14T02:46:40.537882Z"
      }
    ]


Adding a new profile
--------------------

Request::

    $ curl -X POST http://127.0.0.1:8000/profiles \
      -H "Content-Type: application/json"

Response::

    Status: 201 OK

    {
      "id": "01234567-89ab-cdef-0123-456789abcdef",
      "created": "2015-05-14T02:46:40.537882Z",
      "updated": "2015-05-14T02:46:40.537882Z"
    }



Adding brand to profile
-----------------------

Request::

    $ curl -X PUT http://127.0.0.1:8000/profiles/01234567-89ab-cdef-0123-456789abcdef/brands/01234567-89ab-cdef-0123-456789abcdef \
      -H "Content-Type: application/json"

Response::

    Status: 204 NO CONTENT


Removing brand from profile
---------------------------

Request::

    $ curl -X DELETE http://127.0.0.1:8000/profiles/01234567-89ab-cdef-0123-456789abcdef/brands/01234567-89ab-cdef-0123-456789abcdef \
      -H "Content-Type: application/json"

Response::

    Status: 204 NO CONTENT


Listing all brands for given profile
------------------------------------

Request::

    $ curl http://127.0.0.1:8000/profiles/01234567-89ab-cdef-0123-456789abcdef/brands

Response::

    Status: 200 OK

    [
      {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
        "name": "Apple",
        "created": "2015-05-14T02:46:40.537882Z",
        "updated": "2015-05-14T02:46:40.537882Z"
      }
    ]


Listing all profiles for given brand
------------------------------------

Request::

    $ curl http://127.0.0.1:8000/brands/01234567-89ab-cdef-0123-456789abcdef/profiles

Response::

    Status: 200 OK

    [
      {
        "id": "01234567-89ab-cdef-0123-456789abcdef",
         "created": "2015-05-14T02:46:40.537882Z",
         "updated": "2015-05-14T02:46:40.537882Z"
      }
    ]
