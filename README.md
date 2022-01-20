# productivity_assistant

Little Assistant i use for daily university tasks. 

# Setup 
In order to include Pictures into the fetching process, we need access to the Notion API to fetch these.


1. You need to have a Notion page that contains all pages, in which you want to search for 
2. generate a Notion API Key as described under point "Step 1: Create an integration." [here](https://developers.notion.com/docs/getting-started)
3. Share the page you created in step 1 as desribed under point "Step 2: Share a database with your integration" [here](https://developers.notion.com/docs/getting-started)
4. Setup secret.py as described in Assistant.py 
6. Install the AnkiConnect AddOn to Anki as described [here](https://foosoft.net/projects/anki-connect/)

# Rules to make this script work 
1. You need to have a Notion page that contains all pages, in which you want to search for toggles 
2. The page of point 1 must contain toggles which are not nested in any other block. Otherwise we wont find them. 

Your structure should look like this:
![image](https://user-images.githubusercontent.com/82976744/150239854-c721af8f-6320-4790-b32e-db7ded282007.png)
In this case, "Semester 5" is the page refered to, in point 1. <br>
The Page "IT-Security" is one example of a page that can be fetched.<br>
On the right you see that "IT-Security" contains non-nested toggles.

3. Anki has to be open during use of the script (due to AnkiConnect)



# Funcionalities
## Notion ToDo adding
When opening the script and just entering some text that is !="anki" this text is added as a new page to the ToDo in Notion. 

## Anki Cards from Notion 
The script can also parse Notion notes and add them into the learning app "Anki". 

Copy notes in the following format to your clipboard: 

![image](https://user-images.githubusercontent.com/82976744/143955277-61c34c95-3bac-45a8-9a73-8f65033c7327.png)

Start script, enter "anki". 

Choose deck.

Your clipboard will be read, parsed into card format and send to anki.

You can now add new cards to the selected deck by hitting enter. 

![image](https://user-images.githubusercontent.com/82976744/143955481-1a84427e-023c-4b87-8bef-d0f66dec8359.png)

# BPMN Process
![diagram (1)](https://user-images.githubusercontent.com/82976744/148691858-e93ce0a6-89c9-425a-8fb9-82d13386b690.jpg)
