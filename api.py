from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from chatbot import Chatbot
import os
import tempfile

os.environ["OPENAI_API_KEY"] = ""

app = Flask(__name__)
CORS(app)

# Instantiate chatbot once
bot = Chatbot()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    result = bot.generate_response(user_input)
    # result is a dict with keys: summary, chunks, sources
    return jsonify(result)

@app.route('/api/add', methods=['POST'])
def add_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    filepath = os.path.join('Data', file.filename)
    file.save(filepath)
    bot.add_document(filepath)
    return jsonify({'message': 'File added', 'filename': file.filename})
@app.route('/api/list', methods=['GET'])
def list_documents():
    docs = bot.list_documents()
    # If docs is a string, split it into a list
    if isinstance(docs, str):
        docs = [doc.strip() for doc in docs.splitlines() if doc.strip()]
    return jsonify({'documents': docs})

@app.route('/api/clear', methods=['POST'])
def clear_database():
    bot.clear_database()
    return jsonify({'message': 'Database cleared'})

@app.route('/api/reload', methods=['POST'])
def reload_database():
    bot.reload_database()
    return jsonify({'message': 'Database reloaded'})

@app.route('/api/analyze', methods=['POST'])
def analyze_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    
    # Create a temporary file for analysis
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        file.save(temp_file.name)
        temp_filepath = temp_file.name
    
    try:
        # Analyze the file without adding it to the database
        result = bot.analyze_file_similarity(temp_filepath)
        return jsonify({'response': result, 'filename': file.filename})
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filepath):
            os.unlink(temp_filepath)

@app.route('/api/delete', methods=['POST'])
def delete_document():
    data = request.json
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    result = bot.delete_document(filename)
    if result.startswith('File') and 'deleted' in result:
        return jsonify({'message': result})
    else:
        return jsonify({'error': result}), 400

@app.route('/')
def root():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
