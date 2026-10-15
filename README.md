# 📋 Cultural OS Simulator & Communication Diagnostics

A polished, minimalist, interactive two-column web application designed to simulate high-stakes cross-cultural and interpersonal communication scenarios. The app allows users to practice navigating complex dialogue with distinct personas and provides a deep, multi-turn diagnostic evaluation powered by Gemini.

---

## ✨ Features

- **2-Column Workspace:**
  - **Left Panel (Interactive Arena):** Engaging chat console with turn counters, real-time feedback, and safety input locks. Includes a prominent **Reset** action to easily clear state and change personas.
  - **Right Panel (Diagnostics Dashboard):** Displays a comprehensive **Responsible Communication Diagnostics** matrix at the end of the 3-turn exchange, detailing contextual harmony, risk alignment, and actionable takeaways.
- **Robust State Control:** Built-in safeguards preventing double-submits, visual infinite loops (e.g. counter bugs), or API hammering.
- **Clean Architecture:** Simple Flask backend integrated with Gemini (`gemini-3.5-flash`), paired with a pristine, vanilla HTML5/CSS3/JS frontend.

---

## 🛠️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone <your-repository-url>
   cd cultural-os-simulator

   cd cultural-os-simulator
Create a Virtual Environment & Activate It:

Bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
Install Dependencies:

Bash
pip install -r requirements.txt
Configure Environment Variables:
Create a file named .env in the root directory and add your Gemini API key:

GEMINI_API_KEY=your_actual_api_key_here

Run the Application:

Bash
python app.py
Open your browser and navigate to http://127.0.0.1:5000 to start using the simulator.

🎮 How It Works
Select / Load a Persona: Provide a situational prompt (such as the polite neighbor Mrs. Margaret Vance, or busy supplier Dan).

The 3-Turn Exchange: Chat naturally with the persona. The left-side status bar will dynamically track your turn progress (e.g., Turn: 1 / 3 up to 3 / 3).

Automatic Lock & Evaluation: Upon sending your 3rd message, the frontend safely locks the input bar. The app triggers a comprehensive Gemini diagnostic call and renders the detailed scoring matrix directly in the right-side dashboard.

Iterate: Click the Reset button on the left panel to wipe the slate clean and try a new persona on teh front page.

### 🤖 Model Selection (Gemini 3.5 vs 2.5)

By default, this application is configured to use **`gemini-3.5-flash`**. 
If you prefer a highly stable, fast conversational flow with generous free-tier API quotas, change it to **`gemini-2.5-flash`**. It is perfect for rapid testing and out-of-the-box runnability.

1. Open `app.py`.
2. Locate the model configuration in the `/start_simulation` and `/send_message` routes. 
3. Change `model="gemini-3.5-flash"` to `model="gemini-2.5-flash"`.

```

---
## 🛡️ License
This project is licensed under the MIT License. See the LICENSE file for details.
"""
