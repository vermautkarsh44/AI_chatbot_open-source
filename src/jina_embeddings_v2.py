import json
import numpy as np
from transformers import AutoModel

class Jina_Embed_v2:
    def __init__(self):
         self.model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-en', trust_remote_code=True)

    def generate_pdf_embeddings(self, id, pdf_name, text_splits):
        print(f"id {id} inside generate_pdf_embeddings") # print

        with open(f"data/extracted_pdfs/{id}.json", "r") as file:
            extracted_pdf = json.load(file)

        embeddings = []

        try:
            print(f"id {id} generating embeddings") # print

            for text_chunk in text_splits:
                embeddings.append(self.model.encode([text_chunk])[0])

            print(f"id {id} generating embeddings SUCCESSFUL!!") # print

            embeddings = [embedding.tolist() for embedding in embeddings]

            print(f"id {id} embeddings conversion DONE!!") # print

            extracted_pdf["pdf_content"] = text_splits
            extracted_pdf["pdf_content_vector"] = embeddings

            with open(f"data/chunked_embedded_pdfs/{id}.json", "w") as file:
                json.dump(extracted_pdf, file)

            return id, pdf_name
        
        except:
            return False
    
    def generate_query_embeddings(self, conversation_id, rephrased_query):
        print(f"generating embeddings for query") # print
        embedded_query = self.model.encode([rephrased_query])[0]
        embedded_query = np.array(embedded_query)
        print("fetched embedded query") # print
        return embedded_query
