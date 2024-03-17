import fitz
import re
import uuid
import os
import json

class Fitz:

    def extract_pdf_content(self, pdf_path):
        texts=[]
        doc = fitz.open(pdf_path)

        for page in doc:
            text_in_page = page.get_text()
            links_in_page = page.get_links()

            for link in links_in_page:
                try:
                    hyperlink_text = page.get_textbox(link['from'])
                    hyperlink_url = link['uri']

                    replacement_text = f"{hyperlink_text} ({hyperlink_url})"

                    if (hyperlink_text.strip()!=''):
                        text_in_page = re.sub(re.escape(hyperlink_text), replacement_text, text_in_page)

                except:
                    pass

            texts.append(text_in_page)

        pdf_name = (pdf_path.split("\\")[-1]).split(".")[0] #(pdf_path.strip('/')[-1]).strip('.')[0]

        print(f"pdf_name - {pdf_name}")  # print 

        id = self.assign_id()

        print(f"id - {id}") # print

        with open(f"data/extracted_pdfs/{id}.json", 'w') as file:
            json.dump({
                        "pdf_name": pdf_name,
                        "pdf_content": '\n\n'.join(texts)
                    }, file)
        
        print(f"{id}.json dumped") # print

        result = self.make_entry_in_uuid_source_mapping(id, pdf_name)

        print(f"id - {id} - added to uuid_source_mapping.json!") # print

        if result:
            return id, pdf_name
        else:
            return False

    def assign_id(self):
        id = uuid.uuid4().hex

        ids = set(os.listdir("data/extracted_pdfs/"))

        while id in ids:
            id = uuid.uuid4().hex

        return id
    
    def make_entry_in_uuid_source_mapping(self, id, pdf_name):
        try:
            with open("data/uuid_source_mapping.json", "r") as file:
                uuid_source_mapping = json.load(file)
        except:
            print("uuid_source_mapping.json is initially empty!") # print
            uuid_source_mapping = {}

        uuid_source_mapping[id] = pdf_name

        with open("data/uuid_source_mapping.json", "w") as file:
            json.dump(uuid_source_mapping, file)

        return True
