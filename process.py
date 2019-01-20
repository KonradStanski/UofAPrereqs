# # new file
import json

with open('data.txt', 'r') as f:
    array = json.load(f)

print (array[0]["title"])