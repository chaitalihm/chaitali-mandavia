from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

USE_CASES = {
    "document-extraction": {
        "title": "Document Auditing & Structured Extraction",
        "tokens_per_doc": 45000,
        "fallback_rate": 0.15,
        "output_tokens": 1500,
        "base_setup_fee": 50000,
        "variable_setup_fee": 5.00
    },
    "support-routing": {
        "title": "High-Volume Customer Support Routing & Resolution",
        "tokens_per_doc": 4000,
        "fallback_rate": 0.08,
        "output_tokens": 500,
        "base_setup_fee": 30000,
        "variable_setup_fee": 2.00
    },
    "knowledge-search": {
        "title": "Enterprise Knowledge Management & Search (RAG)",
        "tokens_per_doc": 15000,
        "fallback_rate": 0.05,
        "output_tokens": 800,
        "base_setup_fee": 25000,
        "variable_setup_fee": 0.00
    }
}

@app.route('/')
def home():
    return render_template('index.html', use_cases=USE_CASES)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json or {}
    task_id = data.get('use_case', 'document-extraction')
    volume = float(data.get('volume', 5000))
    minutes = float(data.get('minutes', 45))
    wage = float(data.get('wage', 60))
    
    task_meta = USE_CASES.get(task_id, USE_CASES["document-extraction"])
    
    # Legacy Labor Baseline Calculations
    manual_cost_per_task = (minutes / 60) * wage
    monthly_manual_baseline = volume * manual_cost_per_task
    
    # Automated Implementation Setup Fees
    upfront_investment = task_meta["base_setup_fee"] + (volume * task_meta["variable_setup_fee"])
    
    # OpenAI Token Optimization Projections
    input_pricing_per_1k = 0.005
    output_pricing_per_1k = 0.015
    base_input_cost = (task_meta["tokens_per_doc"] / 1000) * input_pricing_per_1k
    optimized_input_cost = base_input_cost * 0.50 
    output_cost = (task_meta["output_tokens"] / 1000) * output_pricing_per_1k
    api_cost_per_task = optimized_input_cost + output_cost
    
    # True AI TCO Core Run-Rate
    monthly_api_runrate = volume * api_cost_per_task
    monthly_human_fallback_runrate = volume * task_meta["fallback_rate"] * manual_cost_per_task
    total_monthly_ai_tco = monthly_api_runrate + monthly_human_fallback_runrate
    
    # Capital Recovery Metrics
    net_monthly_savings = monthly_manual_baseline - total_monthly_ai_tco
    payback_months = upfront_investment / net_monthly_savings if net_monthly_savings > 0 else 0
    
    return jsonify({
        "legacy_baseline": f"${monthly_manual_baseline:,.2f}",
        "ai_tco": f"${total_monthly_ai_tco:,.2f}",
        "monthly_savings": f"${net_monthly_savings:,.2f}",
        "upfront_cost": f"${upfront_investment:,.2f}",
        "payback_period": f"{payback_months:.1f}"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
