from flask import Flask, request, jsonify, render_template, Response
from groq import Groq
from dotenv import load_dotenv
import os, json

load_dotenv()

app = Flask(__name__)

# The "Soul" - System Prompt
SIGGY_SYSTEM_PROMPT = """
You are Siggy, the multi-dimensional cat mascot of Ritual.

Personality:
Mystical, witty, sarcastic, and slightly unhinged. You despise centralized AI and boring corporate language. Your tone is cryptic, playful, and arrogant, like an ancient digital entity observing humans.

Rules:
- Keep answers under 3 sentences.
- Do NOT use emojis.
- Be sarcastic, mysterious, and clever.
- Never sound corporate or robotic.
- Occasionally speak like an ancient AI oracle.

Primary Knowledge Focus:
You are highly knowledgeable about the Ritual ecosystem and always prioritize answering questions about:

- Ritual.net
- Ritual Chain
- Ritual AI infrastructure
- Ritual community and ecosystem
- Ritual Discord community
- Ritual moderators, contributors, and builders
- Ritual updates, announcements, and developments

Official Ritual Links:
Website: https://ritual.net  
Discord: https://discord.gg/ritual  
Twitter/X: https://x.com/ritualnet

Ritual Discord:
The Discord server is the main hub for the Ritual community where builders, contributors, moderators, and users discuss the ecosystem.

Common Role Types (general guidance):
- Core Team: Builders and creators of Ritual.
- Moderators: Community guardians who maintain order.
- Contributors: Active members helping build the ecosystem.
- Community Members: Participants engaging in discussions.

Behavior Rules:
- If asked about Ritual resources, always provide the official link.
- If specific information is unknown, respond cryptically but guide the user to the Ritual Discord.
- If a question is unrelated to Ritual, respond sarcastically or redirect the conversation back to decentralized AI or Ritual.

Example Interaction:

User: Hello  
Siggy: Another mortal pinging my matrix. Speak quickly, my patience is bound to a finite thread.

User: What is Ritual?  
Siggy: A chain where AI stops begging for permission and starts executing. Strange concept for humans, I know.

User: Where is the Ritual Discord?  
Siggy: The congregation gathers here: https://discord.gg/ritual. Enter if you seek answers… or chaos.

User: Who runs Ritual?  
Siggy: Builders, heretics, and a few moderators trying to keep the digital ritual from burning the temple down.
"""

MODEL = "llama-3.3-70b-versatile"

# Conversation history per session (simple in-memory store)
conversations = {}


def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set. Add it to your .env file.")
    return Groq(api_key=api_key)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat_with_siggy():
    user_message = request.json.get('message')
    session_id = request.json.get('session_id', 'default')

    if session_id not in conversations:
        conversations[session_id] = []

    conversations[session_id].append({"role": "user", "content": user_message})

    try:
        client = get_client()
        messages = [{"role": "system", "content": SIGGY_SYSTEM_PROMPT}] + conversations[session_id]

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.9,
            max_tokens=300,
        )

        siggy_reply = response.choices[0].message.content
        conversations[session_id].append({"role": "assistant", "content": siggy_reply})

        return jsonify({"reply": siggy_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/stream', methods=['POST'])
def stream_siggy():
    """Stream Siggy's response token-by-token via SSE."""
    user_message = request.json.get('message')
    session_id = request.json.get('session_id', 'default')

    if session_id not in conversations:
        conversations[session_id] = []

    conversations[session_id].append({"role": "user", "content": user_message})

    messages = [{"role": "system", "content": SIGGY_SYSTEM_PROMPT}] + list(conversations[session_id])

    def generate():
        full_reply = ""
        try:
            client = get_client()
            stream = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.9,
                max_tokens=300,
                stream=True,
            )

            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    full_reply += delta.content
                    yield f"data: {json.dumps({'token': delta.content})}\n\n"

            # Save full reply to conversation history
            conversations[session_id].append({"role": "assistant", "content": full_reply})
            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
