import json
from transformers import LlamaTokenizer
from langchain.text_splitter import RecursiveCharacterTextSplitter

class Llama_Tokenizer:

    def tokenized_len(self, text):
        tokenizer = LlamaTokenizer.from_pretrained("model/tokenizer.model")
        tokens = tokenizer.tokenize(text)
    
        return len(tokens)
    
    def get_text_splitter(self):
        text_splitter = RecursiveCharacterTextSplitter(
                                                        chunk_size = 500,
                                                        chunk_overlap  = 25,
                                                        length_function = self.tokenized_len
                                                    )
        
        return  text_splitter
    
    def tokenize_split_text(self, id, pdf_name):
        print(f"id - {id} called tokenize_split_text()") # print

        with open(f"data/extracted_pdfs/{id}.json", "r") as file:
            extracted_pdf = json.load(file)

        text_splitter = self.get_text_splitter()

        try:
            print(f"id - {id} - splitting text begin") # print
            text_splits = text_splitter.split_text(extracted_pdf["pdf_content"])
            print(f"id - {id} - splitting text SUCCESSFUL!!") # print
            return id, pdf_name, text_splits
        
        except:
            return False
