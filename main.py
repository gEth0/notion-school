import requests
import json
import time
import os
import datetime
from datetime import date
import classeviva
from classeviva.client import Client
from classeviva.credentials import EnvCredentialsProvider


databaseId = input('\n Enter Your Notion Database ID=> ')

url = f"https://api.notion.com/v1/databases/{databaseId}/query"

token = input('\n Enter Your Notion Secret Token=>')

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def setEnvVariables(email, password):
    os.environ['CLASSEVIVA_USERNAME'] = email
    os.environ['CLASSEVIVA_PASSWORD'] = password


def readDb(url, headers):
    response = requests.post(url, headers=headers)
    data = response.json()
    # with open('./db.json', 'w', encoding='utf8') as f:
    #     json.dump(data, f, ensure_ascii=False)
    return data


def addPage(databaseId, headers, deliveryDate, subject, idObj, notes):
    createUrl = 'https://api.notion.com/v1/pages'
    newPageData = {
        "parent": {"database_id": databaseId},
        "cover": {
            "type": "external",
            "external": {
                "url": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSXYd3tiW8TOkyafdryAlq0SyXcJyWjieARFIfEd5HVChaEFu7h",

            }
        },

        "icon": {
            "type": "emoji",
            "emoji": "📘"
        },
        "properties": {
            "Status": {
                "id": "%3DsKL",
                "type": "status",
                "status": {
                        "id": "7e74914d-ba67-4e1d-a6b1-47b84d6c3ae2",
                        "name": "Not started",
                        "color": "default"
                }
            },
            "Delivery Date": {
                "id": "V%5E%5Dv",
                "type": "date",
                "date": {
                        "start": deliveryDate,
                        "end": None,
                        "time_zone": None
                }
            }, "ID": {
                "id": "WKLl",
                "type": "rich_text",
                "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": idObj,
                                "link": None
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": idObj,
                            "href": None
                        }
                ]
            },
            "Name": {
                "id": "title",
                "type": "title",
                "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": subject,
                                "link": None
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": subject,
                            "href": None
                        }
                ]
            }
        }, "children": [{
            "object": "block",
            "id": "710d21ea-abd7-4807-9f5d-761646f8e286",
            "parent": {
                "type": "page_id",
                "page_id": "b4b30faf-d9e0-4127-ad10-db9196167918"
            },
            "has_children": False,
            "archived": False,
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Page: ",
                            "link": None
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": "Page: ",
                        "href": None
                    }
                ],
                "is_toggleable": False,
                "color": "default"
            }
        },
            {
            "object": "block",
            "id": "3d380591-a12f-46b8-8b95-8122d2c580b6",
            "parent": {
                "type": "page_id",
                "page_id": "b4b30faf-d9e0-4127-ad10-db9196167918"
            },
            "has_children": False,
            "archived": False,
            "type": "callout",
            "callout": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": notes,
                            "link": None
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": notes,
                        "href": None
                    }
                ],
                "icon": {
                    "type": "emoji",
                    "emoji": "📗"
                },
                "color": "gray_background"
            }
        },
            {
            "object": "block",
            "id": "988903b2-e63b-4260-83be-2a1c7d599fe5",
            "parent": {
                "type": "page_id",
                "page_id": "b4b30faf-d9e0-4127-ad10-db9196167918"
            },
            "has_children": False,
            "archived": False,
            "type": "divider",
            "divider": {}
        }, ],

    }

    data = json.dumps(newPageData)

    res = requests.post(createUrl, headers=headers, data=data)

    print(res.status_code)
    print(res.text)


email = input('\n Enter Your Classeviva Email=> ')
password = input('\n Enter your Classeviva Password=> ')

setEnvVariables(email, password)
while True:
    newReadDb = readDb(url, headers)
    with Client(EnvCredentialsProvider()) as client:
        data = client.list_agenda(
            since=date.today(), until=date.today()+datetime.timedelta(days=100))

        idList = []
        if len(newReadDb['results']) == None:
            print('No assignments yet')
        else:
            for el in range(len(newReadDb['results'])):
                idDb = newReadDb['results'][el]['properties']['ID']['rich_text'][0]['text']['content']
                idList.append(idDb)

            print(idList)
            print(data)
            print(len(data))
            for n in range(len(data)):
                if data[n].subject == None:
                    subject = data[n].author
                else:
                    subject = data[n].subject
                deliveryDate = data[n].starts_at[0:10]
                year = int(data[n].starts_at[0:4])
                month = int(data[n].starts_at[5:7])
                day = int(data[n].starts_at[8:10])
                d1 = datetime.datetime(year, month, day)
                today = date.today()
                d2 = datetime.datetime.combine(today, datetime.time(0, 0))
                idObj = str(data[n].id)
                notes = data[n].notes
                if not d2 >= d1:
                    if idObj not in idList:
                        addPage(databaseId, headers, deliveryDate,
                                subject, idObj, notes)

                else:
                    continue

        time.sleep(1800)
