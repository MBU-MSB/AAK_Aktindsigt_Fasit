"""API kald til Fasit"""
import json
import os
from datetime import datetime
import requests


def get_journalnotes_for_citizenid(citizenid: str, bearer_token: str, start_date: str, end_date: str):
    """Finder journaler på et citizenid"""

    url = "https://jobcenter-bff.schultzfasit.dk/api/citizen/journal/queries/getjournalnotesforcitizenid"

    payload = json.dumps({
      "citizenId": citizenid,
      "filterRequest": {
        "contentTypes": [],
        "cases": [],
        "createdBy": [],
        "sources": [],
        "hasAttachments": []
      },
      "pageRequest": {
        "pageNumber": 0,
        "pageSize": 50
      },
      "sortRequest": {
        "sortBy": "eventDate",
        "sortOrder": "descending"
      }
    })

    headers = {
      'accept': 'application/json',
      'accept-language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',
      'authorization': f'Bearer {bearer_token}',
      'content-type': 'application/json',
      'origin': 'https://aarhus.schultzfasit.dk',
      'priority': 'u=1, i',
      'referer': 'https://aarhus.schultzfasit.dk/',
      'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
      'x-tenant': 'aarhus'
    }

    response = requests.request("POST", url, headers=headers, data=payload, timeout=30)

    # Parse the JSON response
    response_data = json.loads(response.text)

    # Convert start_date and end_date strings to datetime.date objects
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Filter journal notes based on the createdAt date
    filtered_journal_notes = [
        note for note in response_data.get('journalNotes', [])
        if start_date_dt <= datetime.strptime(note['createdAt'].split('T')[0], "%Y-%m-%d").date() <= end_date_dt
    ]

    # Extract attachment IDs from filtered journal notes
    attachments = [
        attachment
        for note in filtered_journal_notes
        for attachment in note.get('attachments', [])
    ]

    print("Attachment IDs:", attachments)
    for attachment in attachments:
        print(attachment['mimeType'])

    return attachments


def get_attached_file(queue_dict: dict, attachment: dict, bearer_token: str):
    """Download attachment"""
    url = "https://jobcenter-bff.schultzfasit.dk/api/citizen/journal/queries/downloadjournalnoteattachment"

    payload = json.dumps({
    "attachmentId": attachment["id"],
    "citizenId": queue_dict['Citizenid']
    })
    headers = {
    'accept': 'application/octet-stream',
    'accept-language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': f'Bearer {bearer_token}',
    'content-type': 'application/json',
    'origin': 'https://aarhus.schultzfasit.dk',
    'priority': 'u=1, i',
    'referer': 'https://aarhus.schultzfasit.dk/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-tenant': 'aarhus'
    }

    response = requests.request("POST", url, headers=headers, data=payload, timeout= 30)

    # Define the directory path
    directory_path = rf"\\srvsql46\INDBAKKE\AAK_Aktindsigt\{queue_dict['Serial']}_{queue_dict['CPR']}\Fasit"

    # Create the directory if it does not exist
    os.makedirs(directory_path, exist_ok=True)

    # Save the file content to a local file
    file_save_path = os.path.join(directory_path, attachment['fileName'])
    with open(file_save_path, 'wb') as file:
        file.write(response.content)

    print(f"File downloaded successfully as '{attachment['fileName']}'.")
