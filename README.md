# Scam Shield AI — Complete Local Project

A single-laptop Flask application that brings together a web interface, five detection modules, a local demonstration report file, automated tests, and an optional local Gemma Safety Coach.

## Features

- **LinkGuard:** Checks URLs for configured warning patterns such as HTTP, raw IP addresses, embedded credentials, and sensitive-looking URL terms.
- **QR Shield:** Decodes uploaded QR images with OpenCV. If the QR contains a website URL, LinkGuard analyses it. `sample_qr.png` is a demo QR code containing `https://example.com` for a quick UI test.
- **Job Detector:** Looks for warning phrases in job-offer or recruiter text, including requests for upfront fees.
- **Scam Network:** Checks submitted phone numbers and URLs against `data/scam_reports.json`.
- **Call Shield:** Analyses call-transcript text for potential OTP requests, payment demands, urgency, and sensitive-data requests. It does not monitor or record live calls.
- **Scam Scanner UI:** One responsive web interface for the five tools.
- **Safety Coach:** Uses a local rule-based fallback by default. If Ollama and a Gemma model are running locally, it can request extra guidance from that local model.
- **AI Voice Companion:** In-browser voice conversation using browser microphone speech recognition and spoken replies. Lets users talk with the assistant and hear a response in English (India), Telugu, or Hindi where supported by the browser/device. The assistant identifies itself as AI; this is not a telephone-network call. Browser speech recognition may rely on browser/platform services, so avoid sharing sensitive personal information.
- **Tests:** Pytest tests for module behaviours and Flask routes.

## Project Structure

```text
ScamShieldAI_Complete/
├── app.py
├── requirements.txt
├── README.md
├── sample_qr.png
├── run_app.bat
├── install_and_run.bat
├── modules/
│   ├── __init__.py
│   ├── common.py
│   ├── link_guard.py
│   ├── qr_shield.py
│   ├── job_detector.py
│   ├── scam_network.py
│   ├── call_shield.py
│   └── safety_coach.py
├── data/
│   └── scam_reports.json
├── tests/
│   └── test_modules.py
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js
```

## Run on Windows

1. Extract the ZIP folder to Desktop or another location.
2. Open the extracted `ScamShieldAI_Complete` folder.
3. Click the address bar in File Explorer, type `powershell`, and press Enter. Or open VS Code terminal in this folder.
4. Install dependencies once:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Start the application:

   ```powershell
   python app.py
   ```

6. Open `http://127.0.0.1:5000` in your browser.
7. To stop the server, focus the terminal and press `Ctrl+C`.

You can also double-click `install_and_run.bat` to install the listed dependencies and launch the local app. After packages are installed, `run_app.bat` starts the app directly.

## Voice Companion: How to Use

1. Start the Flask application and open it in a current Chrome or Edge browser.
2. Scroll to **AI Voice Companion** or click **Voice AI** in the top navigation.
3. Select English (India), Telugu, or Hindi, depending on browser/device support.
4. Click **Start voice chat** and allow microphone permission. Speak after the status shows that it is listening.
5. The assistant replies in text and through browser speech synthesis, then listens for the next turn. Click **End chat** to stop.

The assistant is explicitly presented as AI. This feature is an in-browser conversational voice interface, not a real phone call to a mobile/landline number and not live call monitoring. A real telephone integration would require a separate telephony provider, configuration, and appropriate consent.

## Run Tests

From the project folder, run:

```powershell
python -m pytest tests -v
```

One QR encoder-based automated test may be skipped if the installed OpenCV build does not expose a QR encoder. QR decoding in the application uses OpenCV's QR decoder. The Flask route test is skipped only when Flask has not been installed yet; install dependencies before running the full suite.

## Optional Local Gemma Safety Coach

The application works without Gemma. By default, Safety Coach provides built-in rule-based guidance. To enable the local model option:

1. Install and start Ollama on your computer.
2. Download a Gemma model using the model name supported by your Ollama installation. For example, after installing Ollama, use its documented model-pull command for a Gemma model.
3. Ensure its local service is accessible at `http://127.0.0.1:11434`.
4. Set the model name before launching the app if you use a different tag:

   ```powershell
   $env:OLLAMA_MODEL="gemma3"
   python app.py
   ```

   You may change `OLLAMA_HOST` if your local Ollama service uses another local endpoint. The integration only makes a request to the configured local Ollama endpoint; no external AI API key is built into this project.

If Ollama is not reachable, the Coach falls back to local rule-based safety guidance.

## Demo Record

`data/scam_reports.json` contains one deliberately artificial record for testing: phone `+910000000000` and URL `https://reported-example.invalid`. It is a sample placeholder only, not a real-world report and not evidence that a real person or service is fraudulent.

You can add records only when you have a reliable source and a process for validation. Keep the `reports` property as a JSON list.

## Important Limitations

- Risk scores come from simple configured rules. They are not a verified probability of fraud.
- A low score or an absent local report match does not mean a link, phone number, job offer, or caller is safe.
- This project does not query a verified worldwide threat-intelligence database.
- QR Shield decodes an image and analyses any extracted website URL; it does not visit the destination website.
- Call Shield analyses text supplied by the user. The separate Voice Companion can listen to speech through browser microphone permission and speak a response, but it does not call telephone numbers, listen to phone-network calls, or record calls. Browser speech recognition and available voice languages vary by browser/device. Browser speech recognition may process audio through browser/platform services.
- Optional Gemma output can be wrong. Always verify independently before taking action.
- The local Flask development server is intended for a student demonstration on your own machine, not direct public deployment.

## Current Validation Checklist

- Five Python detection modules plus the AI Voice Companion are wired into one Flask application.
- Twelve automated tests are included in `tests/test_modules.py` (one may be skipped if the OpenCV QR encoder API is unavailable).
- A sample QR decode can be performed from the QR Shield tab.
- The web UI calls the local Flask endpoints and renders results.
- The Voice Companion uses `/api/voice-coach` for safety guidance; speech recognition and spoken output are handled by the browser.
- Voice interaction needs a current browser that supports speech recognition (usually Chrome or Edge) and microphone permission. Available spoken voices/languages vary by device.
- This is browser-based voice chat, not a real phone call to a mobile or landline number. Actual phone-network calling would require a separate telephony provider and configuration.
- Final testing on your own Windows machine and review of the complete application is still recommended before a formal demonstration.
