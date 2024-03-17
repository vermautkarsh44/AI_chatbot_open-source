class Prompt:

    def generate_query_rephrasing_prompt(self, conversation_id, user_query, last_conversations):
        print("rephrasing query") # print

        query_rephrasing_prompt = f'''Given the following conversation and a New Question question, rephrase the New Question question to be a standalone question only if it alignes with the below mentioned Important Instructions.
IMPORTANT INSTRUCTIONS-
1. If New Question seems to be a follow-up question of the Old Question strictly only then rephrase the New Question.
2. If New Question does not seems to be a follow-up question of the Old Question then strictly do not rephrase the New Question and strictly just respond "Not a follow-up question".
3. Responses will strictly follow the Response format provided above.
4. You will never provide answers to the New Question.
5. Carefully provide the rephrased question by not missing any relevant details in the given conversation that are needed to answer the New Question.
6. Do not refer by using terms such as 'previous answer' or 'mentioned earlier' in the rephrased question, add all the necessary information needed in the rephrased question itself.
7. Response format:
REPHRASED QUERY: rephrased query
8. Refer the below few-shot conversation examples strictly just to understand how to formulate respond, but strictly never use these examples directly as response:
# Few-shot example 1-
    Old Question: [INST] What are xyz funds? [/INST]
    Old Answer: It is an investment option.
    New Question: [INST] Hey! [/INST]
    Rephrased Question: Not a follow-up question
# Few-shot example 2-
    Old Question: [INST] What are xyz funds? [/INST]
    Old Answer: It is an investment option.
    New Question: [INST] What are it's types? [/INST]
    Rephrased Question: What are the types of xyz funds?"
9. Understand all the above instructions very clearly and strictly based on above instructions comprehend the below conversation and formulate response for below mentioned New Question
Old Question: [INST] {last_conversations[0]['Q']} [/INST]
Old Answer: {last_conversations[0]['A']}
New Question: [INST] {user_query} [/INST]'''
        
        print("rephrase query prompt \n\n", f"{query_rephrasing_prompt}") # print
        return query_rephrasing_prompt
    
    def generate_final_query_prompt(self, conversation_id, rephrased_query, context):
        print("generating final query prompt")

        prompt = f'''I am an Expert QnA Bot, mandated to provide answers and recommended questions exclusively from the given Context.
Principle: I provide responses are strictly derived from Context, void of personal knowledge or insights. Only answers present within Context are permissible.
Objective: Utilize information from multiple sections within the given Context to create a single comprehensive response. If a query falls outside of the Context, the response will be: "Not Found"
Context:
------
{context}
------
Output Format Instructions:
- Use Markdown rendering elements for visually appealing responses.
- Utilize headings when necessary for organizing information into sections.
- Use compact tables for structured data presentation.
- Bold relevant parts of responses for improved readability.
- Use short lists to present multiple items or options concisely.
- Break down a long answer into multiple lines(add '\n') for better readability.

Mandatory Rules:
- Prohibition: Strictly refrain from responses to queries which does not have the answer in Context.
- Response Language: Responses must be delivered in the English language with consistency.
- Do not mention that you are answering from "Context" in the final response.
- Respond in a chatbot-like manner and provide responses according to the user's perspective, using only the given context.
------
Query: {rephrased_query}
------
'''
        print("final query prompt \n\n", f"{prompt}")

        return prompt
