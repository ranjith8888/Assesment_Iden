Overview OF THE Assesment


This Python script uses Playwright to automate the login process to Notion and fetches the list of team members, including their details such as name, email, role, admin status, and creation date. The gathered information is then saved to a JSON file.

Detail Overview of How this Code works:

1) User Input: The user is prompted to enter their Notion email and password.
   Screenshot - ![Screenshot 2024-10-04 001938](https://github.com/user-attachments/assets/ab4eb46b-e38b-4325-bb5f-c99fd58c8667)

Browser Automation:

2) The script uses Playwright to open a Chromium browser and navigate to Notion's login page.
It fills in the email and password and clicks the necessary buttons to log in.
Screenshot - ![Screenshot (116)](https://github.com/user-attachments/assets/7d027e85-d3ef-4750-8ef9-09af0a2b9aa8)

API Interaction:

4) After logging in, the script prepares to make requests to the Notion API.
It constructs the base URL for fetching user data and sets the required headers, including an authorization token.
Fetching Data:

5) The script repeatedly calls the Notion API in a loop to handle pagination until all team member data is fetched.
It processes the retrieved data to extract relevant details for each team member.
Data Storage:
Screenshot - ![Screenshot 2024-10-04 002219](https://github.com/user-attachments/assets/def268a3-8bda-488c-84d2-55b226d0e6c8)


7) Finally, the script saves the collected team member data in a formatted JSON file (team_members.json).
Completion: The script prints a confirmation message and closes the browser.


Code Overview

code is written example.py file
To run the script we need to use below command
cmd: python example.python
After succesfull run of the script we need to given the below notion login credentials
Enter your notion email: goudp1234@gmail.com
Enter your notion Password:123456
After entering this credentials ,then it opens a Chromium browser and navigate to Notion's login page.It autologins and populates 100 team members
