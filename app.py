from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini_service import GeminiService

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


gemini_service = GeminiService()

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Finance Quiz Bot!"})

# ✅ Route to receive a finance-related question from the user
@app.route('/receive-question', methods=['POST'])
def receive_question():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    response = gemini_service.receive_question(question)
    return jsonify({"message": response})

# ✅ Route to get Gemini’s generated answer for the given question
@app.route('/bot-answer', methods=['GET'])
def bot_answer():
    answer = gemini_service.generate_answer()
    return jsonify({"bot_answer": answer})

# ✅ Route to submit user's answer
@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    data = request.json
    user_answer = data.get('answer')
    if not user_answer:
        return jsonify({"error": "No answer provided"}), 400

    response = gemini_service.submit_user_answer(user_answer)
    return jsonify({"message": response})

# ✅ Route to evaluate user's answer and get a score (1-10)
@app.route('/evaluate', methods=['GET'])
def evaluate_answer():
    evaluation = gemini_service.evaluate_answer()
    return jsonify({"evaluation": evaluation})

# ✅ Route to get user's current total score
@app.route('/score', methods=['GET'])
def get_score():
    return jsonify({"score": gemini_service.get_score()})

if __name__ == '__main__':
    app.run(debug=True)
