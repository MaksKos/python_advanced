import cjson


dump = cjson.dumps({"k": "value", "key": 5, "русский": 3.6})
print(type(dump), dump)