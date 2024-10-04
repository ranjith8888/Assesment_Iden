from playwright.sync_api import sync_playwright   #playwright.sync_api-It is used For browser automation to log into Notion and navigate through the web interface.
import os
import datetime
from notion_client import Client
import requests
import json
from notion_client import Client

def login_to_notion(page, email, password):                    #login_to_notion function- It Automates the login process to Notion by navigating to the login page, It autofills the given email and passwords at he login page and hits the nessesary buttons to automatically login at notion.and later on it waits for the page to load.
    page.goto('https://www.notion.so/login')
    page.fill('input[type="email"]', email)
    page.fill('input[type="password"]', password)
    page.locator('"Continue"').click()
    page.locator('"Continue with password"').click()
    page.wait_for_load_state('networkidle',timeout=60000)      #wait_for_load_state-it waits for the page to load untill 1 minute

def extract_members(page,idsCreatedAt):                        #This function is used for extracting the team members data
    members = []
    
    for row in range(0,len(page)-1):
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

def getIdsCreatedAt(userDetails):                          #This function Returns a dictionary mapping user IDs to their join times
    joinedIds=userDetails['joinedMemberIds']
    admins={}
    for i in userDetails['users']:
        admins[i['userId']]=i['firstJoinedSpaceTime']
    return admins

def fetch_all_team_members(base_url,headers,aemail):       #this function Fetches all team members from the Notion API in a paginated manner and it also Handles pagination to ensure all members are retrieved
    team_members = []
    has_more = True
    next_cursor = None  

    while has_more:
        payload = {
            'page_size': 50  
        }
        if next_cursor:
            payload['start_cursor'] = next_cursor

        response = requests.get(base_url, headers=headers, params=payload)   # requests -it is for  making HTTP requests.
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

def save_to_json(team_members):                                 #This function Saves the team members' data into a JSON file called team_members.json
    with open('team_members.json', 'w') as f:
        json.dump(team_members, f, indent=4)

def main():
    email = input("Enter your Notion email: ")                   #Asks the user to enter hin notion credentials
    password = input("Enter your Notion password: ")

    with sync_playwright() as p:                                  #Initializes Playwright to launch a browser and navigate to Notion
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login_to_notion(page, email, password)        
        page.wait_for_load_state('networkidle')
        page.locator('"Settings"').click()
        page.wait_for_load_state('networkidle')
        page.wait_for_load_state('networkidle')
        base_url = 'https://api.notion.com/v1/users'
        headers = {
            'Authorization': 'Bearer secret_wA6ezpIBzyvXxIh9FoPwr6NMOzokcFgROyfwS5gxKcP',  #this api token should be users notion integration key
            'Notion-Version': '2022-06-28', 
            'Content-Type': 'application/json'
        }
        team_members = fetch_all_team_members(base_url,headers,email)
        save_to_json(team_members)

        print("Data saved to team_members.json")
        browser.close()

if __name__ == '__main__':
    main()
