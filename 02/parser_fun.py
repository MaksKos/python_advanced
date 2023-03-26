import json


def string_function(string: str):
    pass


def parse_json(json_str: str, keyword_callback, required_fields=None, keywords=None):
    if json_str is None:
        return 'json is None'
    if keyword_callback is None:
        return 'callback is None'
    if required_fields is None or keywords is None:
        return None
    json_doc = json.loads(json_str)
    for field in required_fields:
        doc = json_doc.get(field, None)
        if doc is None:
            continue
        for word in doc.split():
            if word in keywords:
                keyword_callback(word)
    return None
