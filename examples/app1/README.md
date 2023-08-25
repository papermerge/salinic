# App1

What index backend and index location is provided via environment
variable INDEX_URL:

    export INDEX_URL=solr://localhost:8983/myindex

In above example the 'solr' backend is used, with solr instance
running on http://localhost:8983 and index name is 'myindex'.

In order to use xapian backend:

    export INDEX_URL=xapian:////home/eugen/.../examples/app1/xapian_db

Xapian backend is indicated by "xapian://" part.
The rest of URL is the absolute path to xapian index (local) folder.

Apply index schema:

    python app1/main.py schema-apply

Note that you can run schema-apply command as many times as you want.
If schema changes already exist in the index - nothing will be applied.
Schema changes need to be applied before adding any data to the index.

Add data to index:

    python app1/main.py index-add data/nodes1.json


Search:

    python app1/main.py search "*"


Remove data from index:

    python app1/main.py index-delete 817ad10c-16fd-4b45-9bad-17cf166b19d0

In order to remove all content added by specific data file:

    python app1/main.py reset data/nodes1.json
