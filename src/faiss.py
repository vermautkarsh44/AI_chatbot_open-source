import faiss
import numpy as np
import json

class Faiss:
    def __init__(self):
        self.index_path = "faiss_index/id_map_index_c500.faiss"

    def create_index(self, vector_size):
        index = faiss.IndexIDMap(faiss.IndexFlatL2(vector_size))

        return index
    
    def save_index(self, index):
        try:
            faiss.write_index(index, self.index_path)
            return True
        except:
            return False
        
    def load_index(self):
        index = faiss.read_index(self.index_path)

        return index
    
    def append_index(self, id, pdf_name):
        print(f"id {id} loading index") # print

        index = self.load_index()

        print(f"id {id} index loaded") # print

        with open(f"data/chunked_embedded_pdfs/{id}.json", "r") as file:
            chunked_embedded_pdf = json.load(file)

        print(f"id {id} chunked_embedded_pdf read!") # print

        pdf_content_vector = chunked_embedded_pdf["pdf_content_vector"]

        start_id = index.ntotal

        ids = [start_id + count + 1 for count in range(len(pdf_content_vector))]

        chunk_ids = [f"{id}_{count}" for count in range(len(pdf_content_vector))]

        print("ids", ids, "\n")
        print("chunk_ids", chunk_ids)

        print("checking if len(ids) != len(pdf_content_vector)") # print

        if len(ids) != len(pdf_content_vector):
            return False
        
        print("checking if len(ids) != len(chunk_ids)") # print

        if len(ids) != len(chunk_ids):
            return False

        print("converting ids and pdf_content_vector to np.array!") # print

        try:
            print("populating index with chunks") # print

            index.add_with_ids(np.array(pdf_content_vector), np.array(ids))

            print("populating index SUCCESSFUL, now saving index!!") # print

            result = self.save_index(index)

            if result:
                print("saving index successful") # print
                
                print("updating id_uuid_chunk_mapping.json") # print
                try:
                    with open("data/id_uuid_chunk_mapping.json", 'r') as file:
                        id_uuid_chunk_mapping = json.load(file)
                except:
                    id_uuid_chunk_mapping = {}

                print("update loop running................") # print
                for id, chunk_id in zip(ids, chunk_ids):
                    id_uuid_chunk_mapping[str(id)] = chunk_id

                print("loop done") # print
                with open("data/id_uuid_chunk_mapping.json", 'w') as file:
                    json.dump(id_uuid_chunk_mapping, file)

                return pdf_name
            else:
                return False
        except:
            return False
        
    def search_index(self, conversation_id, embedded_query, k):
        print(f"searching index for conversation_id {conversation_id}") # print
        index = self.load_index()
        print("index loaded") # print
        distances, neighbors = index.search(embedded_query.reshape(1, -1), k)
        print("search successful")
        top_ids = neighbors[0]
        print(f"top_ids are {top_ids}")
        return top_ids
    
    def get_context(self, conversation_id, top_ids):
        context = []
        context_chunk_ids = []

        with open("data/id_uuid_chunk_mapping.json", "r") as file:
            id_uuid_chunk_mapping = json.load(file)

        print(f"fetching context_chunk_ids from context_chunk_ids") # print

        for top_id in top_ids:
            if str(top_id) in id_uuid_chunk_mapping:
                context_chunk_ids.append(id_uuid_chunk_mapping[str(top_id)])

        print(f"context_chunk_ids - {context_chunk_ids}")

        for top_chunk_id in context_chunk_ids:
            id = top_chunk_id.split("_")[0]
            chunk_id = top_chunk_id.split("_")[1]

            print(f"id - {id}, chunk_id - {chunk_id}")

            with open(f"data/chunked_embedded_pdfs/{id}.json", "r") as file:
                chunked_embedded_pdf = json.load(file)

            print("appending context") 

            context.append(chunked_embedded_pdf["pdf_content"][int(chunk_id)])

            print('\n\n', f'context - {context}', '\n\n')

        return context
