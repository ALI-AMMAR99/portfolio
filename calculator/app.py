from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

def safe_eval(expression: str):
    expression = expression.replace('×', '*').replace('÷', '/')
    expression = expression.replace('^', '**')
    
    allowed = {
        'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos,
        'tan': math.tan, 'log': math.log, 'log10': math.log10,
        'abs': abs, 'pi': math.pi, 'e': math.e, 'exp': math.exp,
        'factorial': math.factorial, 'pow': pow, 'round': round
    }
    
    try:
        result = eval(expression, {"__builtins__": {}}, allowed)
        return result
    except ZeroDivisionError:
        return "خطأ: القسمة على صفر"
    except Exception as e:
        return f"خطأ: تعبير غير صالح"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression', '').strip()
    
    if not expression:
        return jsonify({'result': '0'})
    
    result = safe_eval(expression)
    return jsonify({'result': str(result)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)