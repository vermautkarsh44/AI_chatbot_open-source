import json

class Manage_Conversation_History:
    def __init__(self):
        self.conversation_history_path = "data/conversation_history.json"

    def fetch_last_conversations(self, conversation_id, num_entries):
        print("opening conversation_history.json") # print
        try:
            with open(self.conversation_history_path, 'r') as file:
                conversation_history = json.load(file)
        except:
            conversation_history = []

        print(f"fetching conversation history of conversation_id {conversation_id}") # print
        last_conversations = []
        matching_entries = [entry for entry in reversed(conversation_history) if entry['conversation_id'] == conversation_id]
        print(f"fetched matching entries for conversation_ id {conversation_id}") # print

        if matching_entries == []:
            print(f"0 matching entries found for conversation_id {conversation_id} returning []") # print
            return []
        
        print(f"fetching last {num_entries} entries for conversation_id {conversation_id} from matching entries") # print
        for entry in matching_entries[:num_entries]:
            last_conversations.append(entry) # (entry.get('Q'), entry.get('A'))
        print(f"last conversation for conversation_id {conversation_id} - {last_conversations}") # print

        return last_conversations
    
    def append_conversation_history(self, conversation_id, query, response):
        print(f"appending conversation_history for {conversation_id}") # print

        try:
            with open(self.conversation_history_path, "r") as file:
                conversation_history = json.load(file)
        except:
            conversation_history = []

        conversation_history.append(
                                        {"conversation_id": conversation_id,
                                         "Q": query,
                                         "A": response
                                        }
                                    )
        
        with open(self.conversation_history_path, "w") as file:
            json.dump(conversation_history, file)

        print("conversation_history appended")

        return True
       