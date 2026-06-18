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
    
    # 1. Base Configuration Models
    if use_case == "document-extraction":
        input_tokens_per_unit, output_tokens_per_unit = 45000, 1500
        human_fallback_rate, upfront_base = 0.15, 35000
    elif use_case == "support-routing":
        input_tokens_per_unit, output_tokens_per_unit = 4000, 500
        human_fallback_rate, upfront_base = 0.08, 25000
    else:
        input_tokens_per_unit, output_tokens_per_unit = 15000, 800
        human_fallback_rate, upfront_base = 0.05, 40000

    # 2. Monthly Point Calculations
    legacy_monthly = (volume * (minutes / 60.0)) * wage
    total_input = volume * input_tokens_per_unit
    total_output = volume * output_tokens_per_unit
    token_cost = ((total_input * 0.005) + (total_output * 0.015)) / 1000.0
    human_audit_cost = (volume * human_fallback_rate * (minutes / 60.0)) * wage
    
    ai_tco_monthly = token_cost + human_audit_cost
    monthly_savings = legacy_monthly - ai_tco_monthly
    upfront_cost = upfront_base + (volume * 0.50)
    
    payback_period = f"{max(0.1, upfront_cost / monthly_savings):.1f}" if monthly_savings > 0 else "Infinite"

    # 3. Time-Series Progression Array for the Dynamic Break-Even Chart
    months_timeline = list(range(0, 13))
    cumulative_human = [0]
    cumulative_ai = [upfront_cost]
    
    for m in range(1, 13):
        cumulative_human.append(legacy_monthly * m)
        cumulative_ai.append(upfront_cost + (ai_tco_monthly * m))

    # 4. Sensitivity Multi-scenario data points
    fallback_scenarios = [0.10, 0.15, 0.20]
    sensitivity_data = {}
    for f in fallback_scenarios:
        f_audit = (volume * f * (minutes / 60.0)) * wage
        f_tco = token_cost + f_audit
        f_savings = legacy_monthly - f_tco
        roi = (f_savings * 12) / upfront_cost if upfront_cost > 0 else 0
        sensitivity_data[f"{int(f*100)}%"] = round(max(0, roi), 2)

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
            "donut": [token_cost * 0.4, token_cost * 0.2, token_cost * 0.4, human_audit_cost],
            "sensitivity": sensitivity_data
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)