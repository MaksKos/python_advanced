# pylint: disable=missing-docstring


import time
import random
import json
from faker import Faker

# generate json format {<str>: <str> or <int> or <float>}

NUM = 500_000
FILE_NAME = "new.json"

fake = Faker()


def get_value():
    prob = random.random()
    if prob <= 0.33:
        return fake.lexify(text="Valeu ?????")
    if prob <= 0.66:
        return random.randint(0, 500_000)
    return random.random()


st = time.time()
data = {fake.lexify(text="key ??????"): get_value() for _ in range(NUM)}
end = time.time()
print(f"generate for {end-st} s")

with open(FILE_NAME, 'w') as f:
    json.dump(data, f)
