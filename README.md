# Siggy The Multi-Dimensional Cat

A blazing-fast, real-time streaming chatbot built with Flask, Groq (Llama 3.3 70B), and a sleek, Gemini-inspired minimalist UI.

Meet **Siggy** — the sarcastic, cryptic, and completely unhinged mascot of Ritual who despises centralized AI.

![Siggy Avatar](static/_avatar.webp)


## Features
* **Real-time Streaming**: Token-by-token response streaming using Server-Sent Events (SSE) for that instant ChatGPT/Gemini feel.
* **Groq Powered**: Uses `llama-3.3-70b-versatile` on Groq's LPU inference engine for ridiculously fast response times.
* **Minimalist UI**: A clean, light-mode interface inspired by Gemini. Features a frosted-glass header, dynamic visual viewport resizing for mobile keyboards, and a subtle watermark background.
* **Mobile Optimized**: Custom JavaScript and CSS to perfectly handle the mobile virtual keyboard, preventing the page from shifting or the input field from hiding. No annoying autofill suggestions.
* **Optimized Assets**: Uses WebP formatting for images (avatar + watermark) for near-instant load times (< 20KB total).
* **Vercel Ready**: Comes with a `vercel.json` and properly structured Flask app ready for serverless deployment out of the box.

## Getting Started Locally

### 1. Clone the repository
```bash
git clone https://github.com/Tarvel/siggy-bot.git
cd siggy-bot
```

### 2. Set up the environment
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add your API Key
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Then open `.env` and add your [Groq API Key](https://console.groq.com):
```
GROQ_API_KEY=gsk_your_actual_api_key_here
```

### 4. Run the application
```bash
python siggy_bot.py
```
Visit `http://127.0.0.1:5001` in your browser.

## Deploying to Vercel

This project is already configured for Vercel deployment.

1. Push your code to a GitHub repository.
2. Go to your [Vercel Dashboard](https://vercel.com/dashboard) and click **Add New... > Project**.
3. Import your GitHub repository.
4. **Important:** Under "Environment Variables", add:
   * Name: `GROQ_API_KEY`
   * Value: `gsk_your_actual_api_key_here`
5. Click **Deploy**. Vercel will automatically use `vercel.json` to configure the Python Serverless Functions.

## Tech Stack
* **Backend:** Python, Flask
* **Frontend:** Vanilla HTML/CSS/JS (Zero framework overhead)
* **AI:** Groq API (Llama-3.3-70b-versatile)

---
*powered by chaos & Groq*
