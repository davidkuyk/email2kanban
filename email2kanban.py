#! python3

# email2kanban.py - A Python program that takes the contents of an email and converts them to a Kanban card on notion.so

import os
import re
import subprocess
from notion.client import NotionClient
from notion.block import TextBlock
import pyautogui
import time

# replace this with your computer's path to the email2kanban folder (include slash at the end)
wd = "/path/to/your/email2kanban/folder/"

try:
	# opens the email file
	subprocess.run(["open", f"{wd}email.txt"])

# IMPORTANT: paste the contents of the email into the email.txt file and Save the file before continuing

	# this pauses the program until the user presses "Enter" so the user can paste in the email.
	input('Press Enter to continue')

	# reads text from email.txt file
	doc = open(f'{wd}email.txt')
	body = doc.read()
	doc.close()
	print('Collecting email text...')

	# clicks on the text file and quits it
	pyautogui.click(941, 462)
	pyautogui.hotkey('command', 'q')

# IMPORTANT: replace the below regex with your desired info to extract from the email
	dateRe = re.compile(r'Date: (\d{4})-(\d{2})-(\d{2})')
	tutorRe = re.compile(r'Tutor: (\w*)')
	studentnameRe = re.compile(r'Student: (\w*) ([a-zA-Z ]+)')

	date = dateRe.search(body).group(2) + '/' + dateRe.search(body).group(3)
	tutor = tutorRe.search(body).group(1)
	studentname = studentnameRe.search(body).group(1) + ' ' + studentnameRe.search(body).group(2)
	studentname = studentname.lower()

	# creates a new kanban item on your board under the initial column
# IMPORTANT: replace yourNotionToken with your Notion v2 token. If you don't know how to find this, google "how to find your notion v2 token"
	client = NotionClient(token_v2="yourNotionToken")
# IMPORTANT: replace yourPageURL with the URL of your Kanban page on notion
	cv = client.get_collection_view("https://www.notion.so/yourPageURL")

	# titles the kanban item using the extracted info
	row = cv.collection.add_row()
	row.name = date + ': ' + tutor + ": " + studentname
	for row in cv.collection.get_rows():
		if row.name == date + ': ' + tutor + ": " + studentname:
			page = client.get_block(row.id)

	# creates paragraphs inside the kanban card with more information
	page.children.add_new(TextBlock, title='client requested session via online form')
	page.children.add_new(TextBlock, title='waiting for tutor email response...')

	print('Note added.')

except Exception as err:
	print(str(err))