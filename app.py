from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import bcrypt
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

try:
    mongo = PyMongo(app)
    print("MongoDB connection status:", mongo.cx)  # Check the connection status
except Exception as e:
    print("Failed to connect to MongoDB:", e)

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_GEN_AI_API_KEY"))  # Replace OpenAI with Google API key

@app.route('/')
def index():
    action = request.args.get('action')
    return render_template('index.html', action=action)  # Pass action to the template

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    mongo.db.users.insert_one({'username': username, 'password': hashed_password})
    return render_template('index.html')  # Redirect to login after signup

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    user = mongo.db.users.find_one({'username': username})

    if user and bcrypt.checkpw(password, user['password']):
        session['username'] = username
        return redirect(url_for('dashboard'))

    return "Invalid credentials"

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('index'))

@app.route('/recommend', methods=['POST'])
def recommend():
    if 'username' not in session:
        return redirect(url_for('login'))

    skill = request.form['skill']
    chat = request.form['skill']

    try:
        # Use Google Gemini API to generate recommendations
        model = genai.GenerativeModel("gemini-1.5-flash")  # Specify the Gemini model
        response = model.generate_content(f"What job roles are suitable for someone skilled in {skill}? Provide a list of 6 job roles and descriptions in HTML table format with the following CSS: table {{ width: 100%; border-collapse: collapse; font-family: sans-serif; }} th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }} th {{ background-color: #3498db; color: white; }}")
        recommendations = response.text.strip()
        
        response = model.generate_content(f"Recommend online courses including YouTube courses for {chat} without links. Provide a list of 6 famous courses from the internet in bullet points in HTML format with the following CSS for cards: .card {{ width: 300px; margin: 10px; background-color: #fff; border-radius: 10px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); overflow: hidden; }} .card-header {{ background-color: #3498db; }}. Add a copy button in the header.")
        chats = response.text.strip()

    except Exception as e:
        recommendations = f"Error generating recommendations: {e}"
        chats = ""

    return render_template('dashboard.html', username=session['username'], recommendations=recommendations, chats=chats)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=int(os.getenv("PORT", 3001)), debug=True)
