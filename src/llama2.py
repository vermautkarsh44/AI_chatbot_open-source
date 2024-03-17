from langchain.llms import CTransformers

class Llama2:
    def __init__(self):
        self.llama2 = CTransformers(model='model/llama-2-7b-chat.ggmlv3.q8_0.bin', 
                    model_type='llama',
                    # n_ctx=4096,
                    config={'max_new_tokens': 500, 
                            'temperature': 0.01,
                            'context_length': 4096
                            }
                    )
        
    def fetch_response(self, conversation_id, prompt):
        print(f"fetching llm response for conversation_id {conversation_id} and prompt", "\n\n", f"{prompt}") # print
        response = self.llama2(prompt)
        print("llm response \n\n", f"{response}") # print
        return response
