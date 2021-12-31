from .secret import secret
import json
import requests
class picture_fetcher:

    


    def __init__(self):
        self.has_loaded_semester = False
        self.page_id =secret.semester_page_id
        self.token = secret.token
        self.headers = {
            "Authorization": "Bearer " + self.token,
            "Notion-Version": "2021-08-16"
        }

        self.loaded_subpage = None
    
    def get_picture_of_block(self,row):
        if self.has_loaded_semester:
            low = row.find("(") +1
            high = row.find(")")
            pic_url = row[low:high]

            #TODO you know have the subpage you want. This subpage has many toggle objects. You have to look if the text in the toggle matches, what you were searching for and only then fetch this toggle. 
            # you have to adapt, so that this script knows the title of the toggle 

        else:
            self.load_semester()
            self.get_picture_of_block(row)

    # returns a json object, fetched from the notion api with the block id 
    def fetch_block(self, block_id):
        url = f"https://api.notion.com/v1/blocks/{block_id}/children"
        response = requests.request("GET", url, headers=self.headers)
        return json.loads(response.text)
        

    #returns an int corresponding to the index of the chosen subpage 
    def choose_subpage(self,names_of_subpages):
        print("Choose Notion Subpage:")

        for index, subpage_name in enumerate(names_of_subpages): print(f"{index}: {subpage_name}")
        chosen_one = input()
        try:
            ret = int(chosen_one)
            if ret >= len(names_of_subpages) or ret < 0 :
                return self.choose_subpage(names_of_subpages)
            else: 
                return ret 
        except: 
            return self.choose_subpage(names_of_subpages)
    
    def load_semester(self):
        json_semester = self.fetch_block(self.page_id)
        print("Hi")

        semester_page = json_semester["results"]
        ids_of_subpages = [result["id"] for result in semester_page if (result["type"] =="child_page" )] #get all ids ob the subpages
        names_of_subpages = [result["child_page"]["title"] for result in semester_page if (result["type"] =="child_page" )] #get all ids ob the subpages 

        choosen_subpage_index = self.choose_subpage(names_of_subpages)        
        self.loaded_subpage = self.fetch_block(ids_of_subpages[choosen_subpage_index]) #here we now have the real subpage we want. 
        

        self.has_loaded_semester = True
