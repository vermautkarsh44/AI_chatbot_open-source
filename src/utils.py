from src.fitz import Fitz
from src.llama_tokenize import Llama_Tokenizer
from src.jina_embeddings_v2 import Jina_Embed_v2
from src.faiss import Faiss
from src.conversation_history import Manage_Conversation_History
from src.prompt import Prompt
from src.llama2 import Llama2
import time

fitz = Fitz()
llama_tokenizer = Llama_Tokenizer()
jina_embed_v2 = Jina_Embed_v2()
faiss_indexer = Faiss()
conv_hist = Manage_Conversation_History()
prompt_generator = Prompt()
llama2_model = Llama2()

def upload_pdf(pdf_path):
    # extract pdf using Fitz.extract_pdf_content()
    result = fitz.extract_pdf_content(pdf_path)

    if result:
        id, pdf_name = result
    else:
        return "extract_pdf_content() failed!"
    
    # split text content into chunks using Llama_Tokenizer.tokenize_split_text()
    start_time = time.time()

    result = llama_tokenizer.tokenize_split_text(id, pdf_name)

    end_time = time.time()
    time_took = end_time-start_time
    print(f"time took to tokenize = {time_took}") # print

    if result:
        id, pdf_name, text_splits = result
    else:
        return "tokenize_split_text() failed!"
    
    # generate chunk embeddings using Jina_Embed_v2.generate_pdf_embeddings()
    start_time = time.time()

    result = jina_embed_v2.generate_pdf_embeddings(id, pdf_name, text_splits)

    end_time = time.time()
    time_took = end_time-start_time
    print(f"time took to embed = {time_took}") # print

    if result:
        id, pdf_name = result
    else:
        return "generate_pdf_embeddings() failed!"
    
    # append index with new pdf id & embeddings using Faiss.append_index()
    result = faiss_indexer.append_index(id, pdf_name)

    if result:
        return f"Indexing completed, {pdf_name} ready for QnA!"
    else:
        return f"append_index() failed!"

def qna(conversation_id, user_query):
    # fetching previous conversations from Manage_Conversation_History.fetch_last_conversations()
    last_conversations = conv_hist.fetch_last_conversations(conversation_id, 1)
    # return last_conversations

    # generating the user_query rephrasing prompt using Prompt.generate_query_rephrasing_prompt()
    query_rephrasing_prompt = prompt_generator.generate_query_rephrasing_prompt(conversation_id, user_query, last_conversations)
    # return query_rephrasing_prompt

    # rephrasing the user_query using Llama2.fetch_response()
    rephrased_query = llama2_model.fetch_response(conversation_id, query_rephrasing_prompt)
    # return rephrased_query
    if "Not a follow-up question" in rephrased_query:
        rephrased_query = user_query

    # generate query embedding using Jina_Embed_v2.generate_query_embeddings()
    embedded_rephrased_query = jina_embed_v2.generate_query_embeddings(conversation_id, rephrased_query)

    # perform simmilarity search on index using Faiss.search_index()
    top_ids = faiss_indexer.search_index(conversation_id, embedded_rephrased_query, 2)

    # fetching context using Faiss.get_context()
    context = faiss_indexer.get_context(conversation_id, top_ids)

    # generating the final prompt for rephrased_query and context using Prompt.generate_final_query_prompt()
    final_query_prompt = prompt_generator.generate_final_query_prompt(conversation_id, rephrased_query, context)
    # return final_query_prompt

    # generating the response using Llama2.fetch_response()
    response = llama2_model.fetch_response(conversation_id, final_query_prompt)

    # appending the response in conversation_history using Manage_Conversation_History.append_conversation_history()
    result = conv_hist.append_conversation_history(conversation_id, rephrased_query, response)

    return response
