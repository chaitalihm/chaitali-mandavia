from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Single standalone dashboard route
@app.route('/')
def index():
    return render_template('index.html')

# Backend calculation API endpoint matched to your custom layout keys
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json() or {}
    
    # 1. Parse keys sent directly by your custom JavaScript sliders
    use_case = data.get('use_case', 'document-extraction')
    volume = float(data.get('volume', 5000))
    minutes = float(data.get('minutes', 45))
    wage = float(data.get('wage', 60))
    
    # 2. Establish task-specific baseline assumptions
    if use_case == "document-extraction":
        input_tokens_per_unit = 45000
        output_tokens_per_unit = 1500
        human_fallback_rate = 0.15
        upfront_base = 35000
    elif use_case == "support-routing":
        input_tokens_per_unit = 4000
        output_tokens_per_unit = 500
        human_fallback_rate = 0.08
        upfront_base = 25000
    else:  # knowledge-search (RAG)
        input_tokens_per_unit = 15000
        output_tokens_per_unit = 800
        human_fallback_rate = 0.05
        upfront_base = 40000

    # 3. Core Economic & Financial Modeling Logic
    # Legacy Baseline Cost (Pure human labor hours)
    legacy_baseline_val = (volume * (minutes / 60.0)) * wage
    
    # AI Utility Infrastructure Cost
    total_input_tokens = volume * input_tokens_per_unit
    total_output_tokens = volume * output_tokens_per_unit
    token_cost = ((total_input_tokens * 0.005) + (total_output_tokens * 0.015)) / 1000.0
    
    # Human Audit Safeguard Overhead Cost
    human_audit_cost = (volume * human_fallback_rate * (minutes / 60.0)) * wage
    
    # Total AI Operational Cost (TCO)
    ai_tco_val = token_cost + human_audit_cost
    
    # Financial Yield Realization Metrics
    monthly_savings_val = legacy_baseline_val - ai_tco_val
    upfront_cost_val = upfront_base + (volume * 0.50)
    
    # Calculate amortization payback threshold
    if monthly_savings_val > 0:
        payback_val = max(0.1, upfront_cost_val / monthly_savings_val)
        payback_str = f"{payback_val:.1f}"
    else:
        payback_str = "Infinite"

    # 4. Return clean formatted outputs straight to your frontend view cards
    return jsonify({
        "legacy_baseline": f"${legacy_baseline_val:,.0f}",
        "ai_tco": f"${ai_tco_val:,.0f}",
        "monthly_savings": f"${monthly_savings_val:,.0f}",
        "upfront_cost": f"${upfront_cost_val:,.0f}",
        "payback_period": payback_str
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)