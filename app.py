"""Scam Shield AI — unified Flask application.

Run locally with: python app.py
This app provides rule-based checks plus an optional local Gemma Safety Coach via Ollama.
"""
from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from modules.call_shield import analyze_call_transcript
from modules.job_detector import analyze_job_offer
from modules.link_guard import analyze_url
from modules.qr_shield import analyze_qr_bytes
from modules.safety_coach import coach
from modules.scam_network import check_scam_network

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB upload limit


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/voice-ai")
def voice_ai():
    return render_template("voice.html")


@app.get("/how-it-works")
def how_it_works():
    return render_template("how_it_works.html")


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "application": "Scam Shield AI",
        "modules": ["LinkGuard", "QR Shield", "Job Detector", "Scam Network", "Call Shield"],
        "safety_coach": "Optional local Gemma model through Ollama; a local rule-based fallback is built in.",
        "voice_companion": "Browser-based speech conversation. It is not a telephone-network call; browser microphone permission is required.",
        "note": "Risk results are warning signals, not proof of safety or fraud."
    })


@app.post("/api/analyze/<kind>")
def analyze(kind: str):
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form

    if kind == "url":
        output = analyze_url(data.get("url", ""))
    elif kind == "qr":
        upload = request.files.get("image")
        if upload is None or not upload.filename:
            return jsonify({"module": "QR Shield", "status": "error", "risk_score": 0,
                            "risk_level": "Unknown", "summary": "Choose a QR-code image first.",
                            "reasons": [], "recommendations": ["Select a PNG, JPG, or JPEG image containing a QR code."],
                            "extracted_data": {}}), 400
        extension = upload.filename.rsplit(".", 1)[-1].lower() if "." in upload.filename else ""
        if extension not in {"png", "jpg", "jpeg", "webp"}:
            return jsonify({"module": "QR Shield", "status": "error", "risk_score": 0,
                            "risk_level": "Unknown", "summary": "Unsupported image file type.",
                            "reasons": [], "recommendations": ["Upload a PNG, JPG, JPEG, or WEBP image."],
                            "extracted_data": {}}), 400
        output = analyze_qr_bytes(upload.read(), upload.filename)
    elif kind == "job":
        output = analyze_job_offer(data.get("text", ""))
    elif kind == "network":
        output = check_scam_network(data.get("phone", ""), data.get("url", ""))
    elif kind == "call":
        output = analyze_call_transcript(data.get("transcript", ""))
    else:
        return jsonify({"error": "Unknown analysis type."}), 404

    status_code = 400 if output.get("status") == "error" else 200
    return jsonify(output), status_code


@app.post("/api/coach")
def safety_coach():
    data = request.get_json(silent=True) or {}
    return jsonify(coach(str(data.get("message", ""))))


@app.post("/api/voice-coach")
def voice_safety_coach():
    """Return a concise, speakable reply for the in-browser AI voice assistant.

    The browser handles microphone speech recognition and spoken output. This is
    an AI voice chat inside the web app, not a telephone-network call.
    """
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()[:3000]
    if not message:
        return jsonify({"status": "error", "message": "Please say or type what you need help with."}), 400

    language = str(data.get("language", "en-IN"))
    result = coach(message)
    provider = str(result.get("provider", "local safety rules"))
    if provider.startswith("local Ollama"):
        reply = str(result.get("message", "")).strip()
        tips = result.get("tips", [])
        if tips:
            reply = (reply + " " + str(tips[0]).strip()).strip()
    elif language == "te-IN":
        reply = ("నేను Scam Shield AI, ఒక AI భద్రతా సహాయకుడిని. మీరు చెప్పిన విషయం అనుమానాస్పదం కావచ్చు, కాబట్టి తొందరపడి డబ్బు పంపకండి లేదా లింక్ తెరవకండి. OTP, పాస్‌వర్డ్, PIN ఎవరికీ చెప్పకండి. సంబంధిత సంస్థ అధికారిక వెబ్‌సైట్ లేదా మీకు తెలిసిన అధికారిక నంబర్ ద్వారా స్వతంత్రంగా ధృవీకరించండి.")
    elif language == "hi-IN":
        reply = ("मैं Scam Shield AI, एक AI सुरक्षा सहायक हूँ। आपने जो बताया है उसमें जोखिम के संकेत हो सकते हैं, इसलिए जल्दबाज़ी में पैसे न भेजें और संदिग्ध लिंक न खोलें। अपना OTP, पासवर्ड या PIN किसी को न बताएं। संबंधित संस्था की आधिकारिक वेबसाइट या सत्यापित नंबर से स्वतंत्र रूप से जाँच करें।")
    else:
        reply = ("I’m Scam Shield AI, an AI digital-safety assistant. What you described may contain warning signs, so pause before sending money or opening a suspicious link. Never share an OTP, password, or PIN. Verify the request using the organisation’s official website or a trusted contact method you find independently.")
    return jsonify({
        "status": result.get("status", "success"),
        "provider": provider,
        "reply": reply[:1800],
        "note": result.get("note", "I am an AI assistant. Please independently verify important information."),
    })


@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": "The uploaded image is too large. Maximum file size is 5 MB."}), 413


@app.errorhandler(500)
def server_error(_error):
    return jsonify({"error": "An internal error occurred. Check the terminal for details."}), 500


if __name__ == "__main__":
    # Local development server. Do not expose the debug server to the public internet.
    app.run(host="127.0.0.1", port=5000, debug=False)
