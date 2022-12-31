try:
    import requests
    import os
    import datetime
    from datetime import date
except:
    print("Make sure you have installed all the dependencies")

def setEnvVariables(email, password):
    os.environ['CLASSEVIVA_USERNAME'] = email
    os.environ['CLASSEVIVA_PASSWORD'] = password

def readDb(url, headers):
    response = requests.post(url, headers=headers)

    return response.json()

def recompilePage(databaseId, headers, deliveryDate, subject, idObj, notes,data):
    data["parent"]["database_id"] = databaseId
    data["properties"]["Delivery Date"]["date"]["start"] = deliveryDate
    data["properties"]["ID"]["rich_text"][0]["text"]["content"] = idObj
    data["properties"]["ID"]["rich_text"][0]["plain_text"]= idObj
    data["properties"]["Name"]["title"][0]["text"]["content"] = subject
    data["properties"]["Name"]["title"][0]["plain_text"] = subject
    data["children"][1]["callout"]["rich_text"][0]["text"]["content"] = notes
    data["children"][1]["callout"]["rich_text"][0]["plain_text"] = notes

    return data

def addPage(databaseId, headers, deliveryDate, subject, idObj, notes):
    createUrl = 'https://api.notion.com/v1/pages'
    try:
        with open("pageData.json","r") as pageData : 
                    newPageData  = json.loads(pageData.read())
                    newPageData = recompilePage(databaseId, headers, deliveryDate, subject, idObj, notes,newPageData)
    except :
        print("Read the documentation for set up the files correctly")
        exit()
    dataToSend = json.dumps(newPageData)

    res = requests.post(createUrl, headers=headers, data=dataToSend)

    return res.status_code

def getDeliveryDateFormatted(dataClasseViva):
    year = int(dataClasseViva.starts_at[0:4])
    month = int(dataClasseViva.starts_at[5:7])
    day = int(dataClasseViva.starts_at[8:10])
    return datetime.datetime(year, month, day)
