from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = "friday_secret_key"  # change this in production

# ====== GROQ CONFIG (OpenAI-compatible) ======
client = OpenAI(
    api_key=os.getenv("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") or "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",
    base_url="https://api.groq.com/openai/v1"
)

# ====== LOGIN PAGE ======
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Simple admin login (change as needed)
        if username == "admin" and password == "friday":
            session["user"] = username
            return redirect(url_for("chat"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# ====== CHAT PAGE ======
@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("chat.html")

# ====== ASK AI ======
@app.route("/ask", methods=["POST"])
def ask():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    user_message = data.get("message", "")

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # current Groq model
            messages=[
                {"role": "system", "content": "You are FRIDAY, a smart AI assistant."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )

        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)})

# ====== LOGOUT ======
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ====== RUN ======
if __name__ == "__main__":
    app.run()
