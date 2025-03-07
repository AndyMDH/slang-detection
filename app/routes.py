from flask import render_template, request, jsonify
from app import app
from app.detector import analyze_text


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    text = ""

    if request.method == 'POST':
        text = request.form.get('text', '')
        result = analyze_text(text)

    return render_template('index.html', result=result, text=text)


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.get_json()
    text = data.get('text', '')
    result = analyze_text(text)
    return jsonify(result)