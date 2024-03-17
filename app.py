from flask import Flask, request, jsonify
from src.utils import upload_pdf, qna
import time

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to open-source AI Chatbot!'

@app.route('/upload_pdf', methods = ['POST'])
def upload_pdf_api():
    start_time = time.time()

    data = request.get_json()

    pdf_path = data["pdf_path"]

    upload_pdf_response = upload_pdf(pdf_path)

    end_time = time.time()
    time_took = end_time-start_time
    print(f"time took to upload pdf = {time_took}") # print

    return upload_pdf_response

@app.route('/qna', methods = ['POST'])
def qna_api():
    data = request.get_json()

    conversation_id = data["conversation_id"]
    user_query = data["user_query"]

    qna_response = qna(conversation_id, user_query)

    return qna_response

if __name__ == '__main__':
    app.run(debug=True, port=8000, use_reloader=False)
