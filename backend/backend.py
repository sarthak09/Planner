from chain import AIPlanner
import os
from flask_cors import CORS
from Logger import Logger
from flask import Flask, request, jsonify, Response, send_from_directory


app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
CORS(app, resources={r"/*": {"origins": "*"}})


llm_model = "groq:llama-3.1-8b-instant"
rag_chain = None 

def initialize_rag():
    global rag_chain, logger
    logger = Logger.get_logger(__name__)
    print("Initializing AI Planner...")
    rag_chain = AIPlanner(logger=logger, city="India", interests="art, history, food", model_name=llm_model)
    print("AI Planner initialized successfully!")
    
    return True

@app.route('/aiplanner', methods=['POST'])
def query_endpoint():
    try:
        global rag_chain, logger
        
        logger.info("Received request for /aiplanner endpoint")
        data = request.json
        city = data['city']
        interest = data['interest']
        logger.info(f"Received city: {city}, interest: {interest}")
        
        response = rag_chain.runAi(city=city, interests=interest)
        return jsonify({"status": "success", "response": response.content})
    except Exception as e:
        print("QUERY ERROR:", e, flush=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/')
def serve_react():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    print("Starting AI Travel Planner Backend Server...")
    initialize_rag()
    app.run(host='0.0.0.0', port=5000, debug=True)