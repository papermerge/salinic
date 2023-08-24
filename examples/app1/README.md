# App1

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
