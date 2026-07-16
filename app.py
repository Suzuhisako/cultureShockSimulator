import os
import time
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)
# A secret key is required by Flask to securely track the user's session state
app.secret_key = "cultural_os_secret_simulation_key_2026"

client = genai.Client()

DIAGNOSTIC_PROMPT = (
    "You are a Cultural OS Diagnostics expert. Analyze the preceding conversation history between the user "
    "and the defined persona. Provide a sharp, brief 'Cultural OS Diagnostic Report' that respects and incorporates "
    "Responsible AI foundations (promoting safe, ethical, and empathetic communication). "
    "Break your analysis down into these three short points:\n\n"
    "1. Contextual Harmony (Did the user communicate with empathy and adapt to the counterpart's environment?)\n"
    "2. Risk Alignment (Did the user handle friction safely, ethically, and responsibly?)\n"
    "3. Practical Actionable Takeaway (One clear, constructive technique for improvement.)"
)

def send_chat_with_retry(chat_session, message_text):
    for attempt in range(1, 4):
        try:
            return chat_session.send_message(message_text)
        except Exception as e:
            if ("503" in str(e) or "UNAVAILABLE" in str(e)) and attempt < 3:
                time.sleep(attempt * 2)
            else:
                raise e

@app.route('/')
def index():
    # Clear any previous session history when loading fresh
    session.clear()
    return render_template('index.html')

@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    persona = request.json.get('persona', '').strip()
    if not persona:
        return jsonify({'error': 'Please provide a persona description.'}), 400

    # Save setup variables to the session
    session['persona'] = persona
    session['turn_count'] = 0
    session['history'] = []

    # Initialize the Gemini Chat using the user's custom persona input

    system_msg = (
        f"You are playing the following role: {persona}. Stay in character but adhere strictly "
        "to professional, safe, and ethical communication guardrails. Do not generate abusive, "
        "harmful, or unsafe dialogue. If the scenario involves a high-stress crisis, respond in a way "
        "that allows the user to practice professional de-escalation, empathy, and safe problem-solving."
    )
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_msg,
            temperature=0.4
        )
    )
    
    # Let the character open the meeting organically
    try:
        # NEW DYNAMIC CODE:
        opening_prompt = (
            "Based on the defined persona and scenario, initiate the conversation naturally. "
            "If you are an interviewer, greet the candidate and ask your first interview question. "
            "If you are a retail manager, open the business meeting. Keep it to 2-3 sentences max."
        )
        response = send_chat_with_retry(chat, opening_prompt)        
        session['history'].append({'role': 'ai', 'text': response.text})
        return jsonify({'history': session['history'], 'turn_count': 0})
    except Exception as e:
        # 🚨 ADD THIS LINE BELOW to print the exact error straight to your terminal log!
        print("\n💥 DETAILED ERROR IN START_SIMULATION:")
        import traceback
        traceback.print_exc()
        
        return jsonify({'error': f"Failed to connect to backend: {str(e)}"}), 500

@app.route('/send_message', methods=['POST'])
def send_message():
    user_text = request.json.get('message', '').strip()
    if not user_text:
        return jsonify({'error': 'Message cannot be empty.'}), 400

    persona = session.get('persona')
    turn_count = session.get('turn_count', 0)
    history = session.get('history', [])
    
    # Reconstruct the running chat session context natively
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=f"You are the following persona: {persona}. Stay strictly in character. Keep responses brief.",
            temperature=0.4
        )
    )
       
    # Catch the chat instance back up with what has happened so far
    for msg in history:
        # Simplistic sync mechanism for stateful recreation over stateless HTTP
        pass 

    # Advance the conversation turn counter
    turn_count += 1
    history.append({'role': 'user', 'text': user_text})

    try:
        # Fetch the persona's live response
        ai_response = send_chat_with_retry(chat, user_text)
        history.append({'role': 'ai', 'text': ai_response.text})
        
        diagnostic_report = None
        # Once the user hits 3 interactive turns, trigger the evaluation phase
        if turn_count == 3:
            try:
                history_text = "\n".join([f"{msg['role']}: {msg['text']}" for msg in history])
                evaluation_payload = f"{DIAGNOSTIC_PROMPT}\n\nHere is the transcript to evaluate:\n{history_text}"
                
                # Use your clean, isolated model generation call
                report_response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=evaluation_payload,
                    config={'temperature': 0.2}
                )
                diagnostic_report = report_response.text
                        
            except Exception as e:
                        print(f"Gemini Diagnostic Error: {e}")
                        diagnostic_report = "The diagnostic evaluation experienced a temporary connection timeout. Please try again."         
          
        session['turn_count'] = turn_count
        session['history'] = history

        return jsonify({
            'history': history,
            'turn_count': turn_count,
            'diagnostic_report': diagnostic_report
        })
    except Exception as e:
        return jsonify({'error': f"Communication error: {str(e)}"}), 500
    
@app.route('/reset_simulation', methods=['POST'])
def reset_simulation():
    # Clear out the REAL active session keys so the chat starts completely fresh
    session.pop('history', None)      
    session.pop('turn_count', None)
    session.pop('persona', None)
    
    return jsonify({"status": "success", "message": "Arena cleared successfully."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)