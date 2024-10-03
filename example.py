from playwright.sync_api import sync_playwright
import os
import datetime
from notion_client import Client
import requests
import json
from notion_client import Client

def login_to_notion(page, email, password):
    page.goto('https://www.notion.so/login')
    page.fill('input[type="email"]', email)
    page.fill('input[type="password"]', password)
    page.locator('"Continue"').click()
    page.locator('"Continue with password"').click()
    page.wait_for_load_state('networkidle',timeout=60000)   

def extract_members(page,idsCreatedAt):
    members = []
    #rows = page.query_selector_all('div.member-row')
    #print(len(page))
    for row in range(0,len(page)-1):
        #print(row['person'],row['person']['email'])
        name = page[row]['name']
        email = page[row]['person']['email']
        role = 'Worksapce Owner'
        is_admin = False
        created_at = idsCreatedAt[page[row]['id']]
        members.append({
            'name': name,
            'email': email,
            'role': role,
            'is_admin': is_admin,
            'created_at': datetime.datetime.fromtimestamp(created_at)
        })
    return members

def getIdsCreatedAt(userDetails):
    #print(userDetails['users'])
    joinedIds=userDetails['joinedMemberIds']
    admins={}
    for i in userDetails['users']:
        admins[i['userId']]=i['firstJoinedSpaceTime']
    return admins

def fetch_all_team_members(base_url,headers,aemail):
    team_members = []
    has_more = True
    next_cursor = None  

    while has_more:
        payload = {
            'page_size': 50  
        }
        if next_cursor:
            payload['start_cursor'] = next_cursor

        response = requests.get(base_url, headers=headers, params=payload)
        data = response.json()
        print(data)
        for user in data.get('results', []):
            name = user.get('name', 'Unknown')
            email = user.get('person', {}).get('email', 'No email available')
            role=""
            if(email == aemail):
                role = user.get('role', 'Webspace Owner')
            else:
                role = user.get('role', 'Webspace Member')
            is_admin = email == aemail
            created_at = user.get('created_time', datetime.datetime.now().isoformat())
            team_members.append({
                'Name': name,
                'Email': email,
                'IsAdmin': is_admin,
                'CreatedAt': created_at,
                'Role': role
            })

        
        has_more = data.get('has_more', False)
        next_cursor = data.get('next_cursor', None)

    return team_members

def save_to_json(team_members):
    with open('team_members.json', 'w') as f:
        json.dump(team_members, f, indent=4)

def main():
    email = input("Enter your Notion email: ")
    password = input("Enter your Notion password: ")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login_to_notion(page, email, password)
        page.wait_for_load_state('networkidle')
        page.locator('"Settings"').click()
        page.wait_for_load_state('networkidle')
        #page.locator('"People"').click()
        page.wait_for_load_state('networkidle')
        base_url = 'https://api.notion.com/v1/users'
        headers = {
            'Authorization': 'Bearer secret_wA6ezpIBzyvXxIh9FoPwr6NMOzokcFgROyfwS5gxKcP',  
            'Notion-Version': '2022-06-28', 
            'Content-Type': 'application/json'
        }
        team_members = fetch_all_team_members(base_url,headers,email)
        save_to_json(team_members)

        print("Data saved to team_members.json")
        browser.close()

if __name__ == '__main__':
    main()
