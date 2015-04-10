#!/usr/bin/env python3

import cgi
import json
from KeywordBase import KeywordBase


print("Content-Type: application/json")
print()

db = KeywordBase("../data/keyword.db")
form = cgi.FieldStorage()
if "keyword" in form:
    data = db.inc_query(form["keyword"].value)
    print('{"status": 0}')
else:
    print('{"status": -1}')


