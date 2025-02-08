from flask import Flask, render_template, send_file, request, redirect, url_for
from main import save_csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download():
    file_path = save_csv()
    return send_file(file_path, as_attachment=True)

# @app.route('/subscribe', methods=['POST'])
# def subscribe():
#     email = request.form.get("email")
#     if email:
#         with open("subscribers.txt", "a") as f:
#             f.write(email + "\n")
#     return redirect(url_for("index"))

# if __name__ == '__main__':
#     app.run()
