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

# Single standalone dashboard route
@app.route('/')
def index():
    return render_template('index.html', use_cases=USE_CASES)

# Backend calculation API endpoint
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    use_case = data.get('use_case')
    monthly_requests = float(data.get('monthly_requests', 0))
    input_tokens = float(data.get('input_tokens', 0))
    output_tokens = float(data.get('output_tokens', 0))
    
    # Core mathematical modeling logic
    total_tokens = ((input_tokens + output_tokens) * monthly_requests) / 1_000_000.0
    cloud_costs = total_tokens * 12.50
    variance_delta = 14.2
    
    return jsonify({
        "total_tokens": f"{total_tokens:.1f}M",
        "cloud_costs": f"${cloud_costs:,.2f}",
        "variance_delta": f"+{variance_delta}%"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)