try:
    import json
    import time
    import os
    import sys
    import datetime
    from datetime import date
    import classeviva
    sys.path.append("modules")
    from classeviva.client import Client
    from classeviva.credentials import EnvCredentialsProvider
    from functions import *
except:
    print("Make sure you have installed all the dependencies")
    exit()

databaseId = input('\n Enter Your Notion Database ID=> ')

url = f"https://api.notion.com/v1/databases/{databaseId}/query"

token = input('\n Enter Your Notion Secret Token=>')

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

email = input('\n Enter Your Classeviva Email=> ')
password = input('\n Enter your Classeviva Password=> ')

setEnvVariables(email, password)

while True:
    newDBNotion = readDb(url, headers)
    
    with Client(EnvCredentialsProvider()) as client:
        dataClasseViva = client.list_agenda(
            since=date.today(), until=date.today()+datetime.timedelta(days=100))
        
        idList = []
        if len(newDBNotion['results']) == None:
            print('No assignments yet')
        else:
            for _ in range(len(newDBNotion['results'])):
                idAssignments = newDBNotion['results'][_]['properties']['ID']['rich_text'][0]['text']['content']
                idList.append(idAssignments)

            for n in range(len(dataClasseViva)):
                if dataClasseViva[n].subject == None:
                    subject = dataClasseViva[n].author
                else:
                    subject = dataClasseViva[n].subject
                deliveryDate = dataClasseViva[n].starts_at[0:10]
                delDate = getDeliveryDateFormatted(dataClasseViva[n])
                
                today = date.today()
                comDate = datetime.datetime.combine(today, datetime.time(0, 0))
                idClassAssignment = str(dataClasseViva[n].id)

                notes = dataClasseViva[n].notes

                if not comDate >= delDate:
                    if idClassAssignment not in idList:
                        status = addPage(databaseId, headers, deliveryDate,
                                subject, idObj, notes)
                        if (status != 200):
                            print("Something went wong.")
                            exit()
                else:
                    continue
        time.sleep(1800) # Set here the refresh time rate in seconds