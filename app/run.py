from app import create_app

app = create_app()
from flask import Flask

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, port=5001)
# app = Flask(__name__)
# if __name__ == '__main__':   
#     print("Starting Flask server...")
#     app.run(debug=True, port=5001)
