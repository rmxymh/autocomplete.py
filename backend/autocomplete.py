#!/usr/bin/env python3

import cgi
import json
from KeywordBase import KeywordBase


print("Content-Type: application/json")
print()

db = KeywordBase("../data/keyword.db")
form = cgi.FieldStorage()

if "keyword" in form:
    data = db.get_word_list(form["keyword"].value)
    autocomplete_data = []
    for keypair in data:
        d = {"key": keypair[0], "count": int(keypair[1])}
        autocomplete_data.append(d)
    print(json.dumps(autocomplete_data))
    with open("../data/autocomplete.log", "a+") as f:
        f.write(json.dumps(autocomplete_data))
        f.close()
else:
    print('{}')

