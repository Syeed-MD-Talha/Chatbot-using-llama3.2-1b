from flask import Flask, request, jsonify, send_from_directory
import subprocess



app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    try:
        # Run Ollama CLI with the Llama model
        response = subprocess.check_output(
            ['ollama', 'run', 'llama3.2:1b', f"summarize this text:{user_input}"],
            text=True
        )
        return jsonify({'response': response.strip()})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
