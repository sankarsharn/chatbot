from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini_service import GeminiService

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Initialize GeminiService
gemini_service = GeminiService()

# Home route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Finance Quiz Bot!"})

# Route to receive a finance-related question
@app.route('/receive-question', methods=['POST'])
def receive_question():
    # Parse JSON data from the request
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Extract the question from the JSON data
    question = data.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    # Pass the question to GeminiService
    response = gemini_service.receive_question(question)
    return jsonify({"message": response})

# Route to get Gemini’s generated answer
@app.route('/bot-answer', methods=['GET'])
def bot_answer():
    # Generate and return the bot's answer
    answer = gemini_service.generate_answer()
    return jsonify({"bot_answer": answer})

# Route to submit user's answer or follow-up
@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    # Parse JSON data from the request
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Extract the user's answer from the JSON data
    user_input = data.get('answer')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Pass the user's answer to GeminiService
    response = gemini_service.submit_user_answer(user_input)
    return jsonify({"message": response})

# Route to evaluate user's answer
@app.route('/evaluate', methods=['GET'])
def evaluate_answer():
    # Evaluate the user's answer and return the score
    evaluation = gemini_service.evaluate_answer()
    return jsonify({"evaluation": evaluation})

# Route to continue the conversation
@app.route('/continue', methods=['POST'])
def continue_conversation():
    # Parse JSON data from the request
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Extract the user's follow-up input from the JSON data
    user_input = data.get('input')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Pass the follow-up input to GeminiService
    response = gemini_service.continue_conversation(user_input)
    return jsonify({"bot_response": response})

# Route to get user's current total score
@app.route('/score', methods=['GET'])
def get_score():
    # Return the user's current score
    return jsonify({"score": gemini_service.get_score()})

# Route to reset the conversation
@app.route('/reset', methods=['POST'])
def reset_conversation():
    # Reset the conversation in GeminiService
    response = gemini_service.reset_conversation()
    return jsonify({"message": response})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)