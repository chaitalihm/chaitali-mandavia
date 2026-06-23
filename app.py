from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/simulator')
def index():
    return render_template('index.html')

@app.route('/deployment-playbook')
def project2():
    return render_template('project2.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/blog/what-is-an-llm')
def post1():
    return render_template('post1.html')

@app.route('/blog/ai-native-vs-ai-enabled')
def post2():
    return render_template('post2.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json() or {}
    use_case = data.get('use_case', 'document-extraction')
    volume = float(data.get('volume', 5000))
    minutes = float(data.get('minutes', 45))
    wage = float(data.get('wage', 60))

    if use_case == "document-extraction":
        input_tokens, output_tokens = 45000, 1500
        human_fallback_rate, upfront_base = 0.15, 35000
    elif use_case == "support-routing":
        input_tokens, output_tokens = 4000, 500
        human_fallback_rate, upfront_base = 0.08, 25000
    else:
        input_tokens, output_tokens = 15000, 800
        human_fallback_rate, upfront_base = 0.05, 40000

    legacy_monthly = (volume * (minutes / 60.0)) * wage
    token_cost = ((volume * input_tokens * 0.003) + (volume * output_tokens * 0.015)) / 1000.0
    human_audit_cost = (volume * human_fallback_rate * (minutes / 60.0)) * wage
    ai_tco_monthly = token_cost + human_audit_cost
    monthly_savings = legacy_monthly - ai_tco_monthly
    upfront_cost = upfront_base + (volume * 0.50)
    payback_period = f"{max(0.1, upfront_cost / monthly_savings):.1f}" if monthly_savings > 0 else "Infinite"

    months = list(range(0, 13))
    human_line = [round(legacy_monthly * m, 2) for m in months]
    ai_line = [round(upfront_cost + (ai_tco_monthly * m), 2) for m in months]

    sens_10, sens_15, sens_20 = [], [], []
    for scale in [0.5, 1.0, 1.5, 2.0]:
        s_vol = volume * scale
        s_legacy = (s_vol * (minutes / 60.0)) * wage
        s_token = ((s_vol * input_tokens * 0.003) + (s_vol * output_tokens * 0.015)) / 1000.0
        s_upfront = upfront_base + (s_vol * 0.50)
        for rate, lst in [(0.10, sens_10), (0.15, sens_15), (0.20, sens_20)]:
            s_tco = s_token + ((s_vol * rate * (minutes / 60.0)) * wage)
            roi = ((s_legacy - s_tco) * 12) / s_upfront * 100 if s_upfront > 0 else 0
            lst.append(round(roi, 1))

    return jsonify({
        "legacy_baseline": f"${legacy_monthly:,.0f}",
        "ai_tco": f"${ai_tco_monthly:,.0f}",
        "monthly_savings": f"${monthly_savings:,.0f}",
        "upfront_cost": f"${upfront_cost:,.0f}",
        "payback_period": payback_period,
        "chart_data": {
            "months": months, "human_line": human_line, "ai_line": ai_line,
            "donut": [round(token_cost*0.5,2), round(token_cost*0.2,2), round(token_cost*0.3,2), round(human_audit_cost,2)],
            "sens_10": sens_10, "sens_15": sens_15, "sens_20": sens_20
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
