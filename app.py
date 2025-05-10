
from dotenv import load_dotenv

from flask import Flask, render_template, request, redirect, url_for
import os
import re
from groq import Groq

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Groq client
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if 'audio' not in request.files:
        return "No audio file provided", 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return "Empty filename", 400

    # Save the file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
    audio_file.save(filepath)

    # Transcribe the audio
    with open(filepath, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3-turbo",
            prompt="You are a doctor.Analyze the text propery specially medical related words.",
            response_format="text",
            language="en",
            temperature=0.0
        )

    transcribed_text = transcription
    
   

    # Get diagnosis and prediction from LLM
    chat_completion = client.chat.completions.create(
        messages=[
            
            {
  "role": "system",
  "content": "You are a world-class medical AI expert. Extract and format only the confirmed medical insights from the patient-doctor conversation. Follow the structure exactly as shown below. Use medically accurate, concise keywords only. Do NOT include any explanations in parentheses (e.g., remove terms like '(GI)' or '(ruled out)'). Only include confirmed and relevant medical terms, and exclude anything marked as 'ruled out'.\n\nAdverse Events:\n- item1\n- item2\n\nDiseases:\n- item1\n\nDiagnoses:\n- item1\n\nPrescriptions:\n- item1\n- item2"
}

           ,

      
            {
                "role": "user",
                "content": transcribed_text
            }
        ],
        model="llama3-70b-8192"
    )

    rst = chat_completion.choices[0].message.content
    
    

    def extract(label, text):
        pattern = rf"{label}[:]\s*((?:- .+\n?)*)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            items = [line.strip("- ").strip() for line in match.group(1).strip().split("\n") if line.strip()]
            return items if items else ["Not found"]
        return ["Not found"]
    
  

    print(rst)
    

    adverse_event = extract("Adverse Events", rst)
    disease = extract("Diseases", rst)
    diagnosis = extract("Diagnoses", rst)
    prescription = extract("Prescriptions", rst)
    print(adverse_event)
    print(disease)
    print(diagnosis)
    print(repr(rst))

    return render_template(
                "result.html",
                transcription=transcribed_text,
                adverse_event=adverse_event,
                disease=disease,
                diagnosis=diagnosis,
                prescription=prescription
            )

if __name__ == '__main__':
    app.run(debug=True)





