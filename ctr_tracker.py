from flask import Flask, render_template_string
app = Flask(__name__)

@app.route('/')
def dashboard():
    try:
        with open("track.log") as f:
            logs = f.readlines()[-100:]
    except:
        logs = []
    return render_template_string("""
    <h2>CTR Tracker Log (Last 100)</h2>
    <table border=1>
        <tr><th>Time</th><th>Proxy</th><th>Status</th><th>User-Agent</th></tr>
        {% for row in logs %}
        {% set parts = row.strip().split(" | ") %}
        <tr>
            <td>{{ parts[0] }}</td>
            <td>{{ parts[1] if parts|length > 1 else '' }}</td>
            <td>{{ parts[2] if parts|length > 2 else '' }}</td>
            <td>{{ parts[3] if parts|length > 3 else '' }}</td>
        </tr>
        {% endfor %}
    </table>
    """, logs=logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
