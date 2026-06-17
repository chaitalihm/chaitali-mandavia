from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- USE CASE DATA FOR THE SIMULATOR ---
USE_CASES = {
    'customer_support': {
        'name': 'AI Customer Support Bot',
        'desc': 'Automated handling of tier-1 support tickets and user inquiries.',
        'input_tokens': 350,
        'output_tokens': 200,
        'monthly_volume': 50000
    },
    'document_search': {
        'name': 'Enterprise Document Search',
        'desc': 'Semantic search and text extraction across internal knowledge bases.',
        'input_tokens': 2000,
        'output_tokens': 500,
        'monthly_volume': 15000
    }
}

# --- TAB ROUTES ---

# TAB 1: Main Portfolio Home Page
@app.route('/')
def home():
    return render_template('home.html')

# TAB 2: Your Live AI TCO Simulator
@app.route('/simulator')
def simulator():
    return render_template('index.html', use_cases=USE_CASES)

# TAB 3: Placeholder for your next project
@app.route('/project2')
def project2():
    return render_template('project2.html')

# --- BACKEND API CALCULATION ROUTE ---
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    # Your existing calculator logic code block stays right here!
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)