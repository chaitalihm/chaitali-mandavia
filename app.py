from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json() or {}
    use_case = data.get('use_case', 'document-extraction')
    volume = float(data.get('volume', 5000))
    minutes = float(data.get('minutes', 45))
    wage = float(data.get('wage', 60))
    
    # 1. Base Assumptions Meta Logic Matrix
    if use_case == "document-extraction":
        input_tokens_per_unit, output_tokens_per_unit = 45000, 1500
        human_fallback_rate, upfront_base = 0.15, 35000
    elif use_case == "support-routing":
        input_tokens_per_unit, output_tokens_per_unit = 4000, 500
        human_fallback_rate, upfront_base = 0.08, 25000
    else:
        input_tokens_per_unit, output_tokens_per_unit = 15000, 800
        human_fallback_rate, upfront_base = 0.05, 40000

    # 2. Financial Modeling Equations
    legacy_monthly = (volume * (minutes / 60.0)) * wage
    total_input = volume * input_tokens_per_unit
    total_output = volume * output_tokens_per_unit
    token_cost = ((total_input * 0.005) + (total_output * 0.015)) / 1000.0
    human_audit_cost = (volume * human_fallback_rate * (minutes / 60.0)) * wage
    
    ai_tco_monthly = token_cost + human_audit_cost
    monthly_savings = legacy_monthly - ai_tco_monthly
    upfront_cost = upfront_base + (volume * 0.50)
    
    payback_period = f"{max(0.1, upfront_cost / monthly_savings):.1f}" if monthly_savings > 0 else "Infinite"

    # 3. Generating Time-series Curves for Frontend Graph Ingestion
    months_timeline = list(range(0, 13))
    cumulative_human = []
    cumulative_ai = []
    
    for m in months_timeline:
        cumulative_human.append(round(legacy_monthly * m, 2))
        cumulative_ai.append(round(upfront_cost + (ai_tco_monthly * m), 2))

    return jsonify({
        "legacy_baseline": f"${legacy_monthly:,.0f}",
        "ai_tco": f"${ai_tco_monthly:,.0f}",
        "monthly_savings": f"${monthly_savings:,.0f}",
        "upfront_cost": f"${upfront_cost:,.0f}",
        "payback_period": payback_period,
        "chart_data": {
            "months": months_timeline,
            "human_line": cumulative_human,
            "ai_line": cumulative_ai,
            "donut": [round(token_cost * 0.35, 2), round(token_cost * 0.15, 2), round(token_cost * 0.25, 2), round(human_audit_cost, 2)],
            "fallback_10": round((legacy_monthly - (token_cost + ((volume * 0.10 * (minutes / 60.0)) * wage))) * 12 / upfront_cost, 2) if upfront_cost > 0 else 0,
            "fallback_15": round((legacy_monthly - (token_cost + ((volume * 0.15 * (minutes / 60.0)) * wage))) * 12 / upfront_cost, 2) if upfront_cost > 0 else 0,
            "fallback_20": round((legacy_monthly - (token_cost + ((volume * 0.20 * (minutes / 60.0)) * wage))) * 12 / upfront_cost, 2) if upfront_cost > 0 else 0
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)