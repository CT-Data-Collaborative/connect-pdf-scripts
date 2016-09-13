import csv, json
from re import sub
from string import digits as DIGITS
from os.path import isdir
from os import mkdir

# for making curl requests
import requests

## Helper functions
def sluggify(text):
    # if text begins with digit, prepend underscore
    if text[0] in DIGITS:
        text = "_" + text

    # change to lowercase
    text = text.lower()
    # replace all chars besides letters, numbers, hyphens and underscores with underscore
    text = sub(r"[^a-zA-Z0-9-_]", "_", text)
    # replace any consecutive number of underscores with just one underscore
    text = sub(r"_+", "_", text)

    return text

def filterdata(o, regionID):
    if regionID not in o["data"]["records"]:
        return False

    return({
        "config" : o["config"],
        "type" : o["type"],
        "name" : o["name"],
        "data" : {"records" : o["data"]["records"][regionID]},
    })

## SOME CONSTANTS
## town profile data endpoints
endpoints = {
    "pdf" : "http://192.168.33.101/download"
}
## Region list
regions = [
    {"id" : "1", "name" : "Southwest Region"},
    {"id" : "2", "name" : "South Central Region"},
    {"id" : "3", "name" : "Eastern Region"},
    {"id" : "4", "name" : "North Central Region"},
    {"id" : "5", "name" : "Western Region"},
    {"id" : "6", "name" : "Central Region"},
    {"id" : "State", "name" : "Statewide"}
]

# Make sure our destination folders exist
if not isdir("requests"):
    mkdir("requests")

if not isdir("pdfs"):
    mkdir("pdfs")

# get whole request from file
with open("pdf-request.json", "r") as dataFile:
    data = json.load(dataFile)

# iterate through each region
for region in regions:

    print("Creating request - region: " + region["name"])
    #   Cull data down to just the one region (or state)
    request = {
        "objects": [filterdata(o, region["id"]) for o in data if filterdata(o, region["id"]) != False],
        "config": {
            "region": region["id"]
        },
        "template": "connect"
    }

    # write request to file, useful for testing later
    requestFileName = region["name"] + " Region"
    requestFileName = sluggify(requestFileName) + ".json"

    with open("requests/" + requestFileName, "w") as jsonFile:
        json.dump({"data" : request}, jsonFile)

    #   send request
    try:
        print("Sending request for PDF - region: " + region["name"])
        request = {"data" : json.dumps(request)}

        pdf = requests.get(endpoints["pdf"], data=request)

        # #   save file
        pdfFileName = region["name"] + " Connect Report"
        pdfFileName = sluggify(pdfFileName) + ".pdf"
        with open("pdfs/" + pdfFileName, "wb") as pdfFile:
            pdfFile.write(pdf.content)
    except Exception as e:
        print("Error!")
        print(region)
        print(e)
