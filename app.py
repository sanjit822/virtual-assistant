from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import webbrowser

app = Flask(__name__)

# Your futuristic HTML (the same frontend you have)
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Futuristic AI Assistant</title>
<style>
/* [same CSS as before, or shorten here for clarity] */
body {
    font-family: 'Poppins', sans-serif;
    height: 100vh;
    background: url('https://images.unsplash.com/photo-1604079629972-8f30c1a3c379?auto=format&fit=crop&w=1400&q=80') no-repeat center center fixed;
    background-size: cover;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #fff;
    text-align: center;
    padding: 20px;
}
#assistant {
    background: rgba(0, 0, 0, 0.7);
    padding: 30px;
    border-radius: 20px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 0 20px #00fff0, 0 0 30px #00c2ff, 0 0 40px #009dff;
}
input, button {
    padding: 10px;
    margin: 10px;
    font-size: 16px;
}
button {
    cursor: pointer;
}
button:active {
    transform: scale(0.98);
}
</style>
</head>
<body>

<div id="assistant">
    <h1>🚀 AI Assistant</h1>
    <h2 id="greeting"></h2>
    <input type="text" id="userInput" placeholder="Type or Speak...">
    <br>
    <button onclick="sendCommand()">Send</button>
    <button onclick="startListening()">🎤 Speak</button>
    <div id="response"></div>
</div>

<script>
function greetUser() {
    const now = new Date();
    const hour = now.getHours();
    let greeting = '';
    if (hour < 12) greeting = 'Good Morning!';
    else if (hour < 18) greeting = 'Good Afternoon!';
    else greeting = 'Good Evening!';
    document.getElementById('greeting').innerText = greeting;
}
greetUser();

function sendCommand() {
    const userInput = document.getElementById('userInput').value;
    if (userInput.trim() === '') return;

    fetch('/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: userInput })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').innerText = data.response;
        speak(data.response);
    });
    document.getElementById('userInput').value = '';
}

function startListening() {
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.lang = "en-US";
        recognition.start();

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript.toLowerCase();
            document.getElementById('userInput').value = transcript;
            sendCommand();
        };
        recognition.onerror = function(event) {
            alert('Speech recognition error: ' + event.error);
        };
    } else {
        alert('Speech Recognition not supported');
    }
}

function speak(message) {
    const utterance = new SpeechSynthesisUtterance(message);
    utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
}
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/command', methods=['POST'])
def command():
    user_input = request.json['command'].lower()
    response = ""

    # Open specific apps or websites based on the command
    if user_input.startswith("open"):
        app_name = user_input.replace("open", "").strip()
        urls = {
            "whatsapp": "https://web.whatsapp.com",
            "instagram": "https://www.instagram.com",
            "facebook": "https://www.facebook.com",
            "playstore": "https://play.google.com/store",
            "chatgpt": "https://chat.openai.com",
            "gemini": "https://gemini.google.com",
            "deepseek": "https://www.deepseek.com",
            "calculator": "https://www.google.com/search?q=calculator",
            "calendar": "https://calendar.google.com",
            "gmail": "https://mail.google.com",
            "maps": "https://www.google.com/maps",
            "chrome": "https://www.google.com/chrome/",
            "youtube": "https://www.youtube.com",
        }
        if app_name in urls:
            webbrowser.open(urls[app_name])
            response = f"Opening {app_name.capitalize()}..."
        else:
            response = "I couldn't find that application."

    # Search for a query on Google
    elif user_input.startswith("search"):
        query = user_input.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        response = f"Searching for {query} on Google..."

    # Play a video on YouTube
    elif user_input.startswith("play"):
        video = user_input.replace("play", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={video}")
        response = f"Playing {video} on YouTube..."

    # Respond with the current date and time
    elif any(word in user_input for word in ["date", "day", "month"]):
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        response = f"Today is {date_str}"

    # Respond with information about the AI assistant
    elif "who are you" in user_input or "your name" in user_input or "who created you" in user_input:
        response = "I am your futuristic AI Assistant, created by an awesome developer!"

    else:
        response = "Sorry, I didn't understand that. Try open, search, or play commands!"

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
