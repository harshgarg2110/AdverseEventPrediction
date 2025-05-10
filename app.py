# import os
# import re
# from flask import Flask, render_template, request, redirect
# from groq import Groq

# app = Flask(__name__)
# client = Groq(api_key="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")  # Replace with your actual key

# # Ensure 'uploads' directory exists
# if not os.path.exists('uploads'):
#     os.makedirs('uploads')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route("/result", methods=["GET", "POST"])
# def result():  # Renamed this function to avoid conflict with the index route
#     if request.method == "POST":
#         file = request.files["audio"]
#         if file:
#             filepath = os.path.join("uploads", file.filename)
#             file.save(filepath)

#             # Transcribe the audio
#             with open(filepath, "rb") as audio_file:
#                 transcription = client.audio.transcriptions.create(
#                     file=audio_file,
#                     model="whisper-large-v3-turbo",
#                     prompt="You are a doctor. Analyze the text.",
#                     response_format="text",
#                     language="en",
#                     temperature=0.0
#                 )

#             transcribed_text = transcription.text  # Access the text of transcription

#             # Get prediction
#             chat_completion = client.chat.completions.create(
#                 messages=[
#                     {
#                         "role": "system",
#                         "content": "You are a world-class medical expert. From the patient conversation, extract:\n"
#                                    "- Adverse Events\n- Diseases\n- Diagnoses\n- Prescriptions\n"
#                                    "Provide them clearly labeled so they can be parsed."
#                     },
#                     {
#                         "role": "user",
#                         "content": transcribed_text
#                     }
#                 ],
#                 model="llama3-70b-8192"  # Ensure this model exists in Groq
#             )

#             raw_output = chat_completion.choices[0].message.content

#             # Simple regex-based parsing (ensure LLM outputs in predictable format)
#             def extract(label):
#                 pattern = rf"{label}[:\-]\s*(.*?)(?=(\n[A-Z][a-z]+[:\-]|$))"
#                 match = re.search(pattern, raw_output, re.DOTALL | re.IGNORECASE)
#                 return match.group(1).strip() if match else "Not found"

#             adverse_event = extract("Adverse Events")
#             disease = extract("Diseases")
#             diagnosis = extract("Diagnoses")
#             prescription = extract("Prescriptions")

#             return render_template(
#                 "result.html",
#                 transcription=transcribed_text,
#                 adverse_event=adverse_event,
#                 disease=disease,
#                 diagnosis=diagnosis,
#                 prescription=prescription
#             )

#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)




































from flask import Flask, render_template, request, redirect, url_for
import os
import re
from groq import Groq

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Groq client
client = Groq(api_key="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")

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
    
    "You are a medical AI. Extract and format the insights exactly as shown below:\n\n"
    "Adverse Events:\n- item1\n- item2\n\n"
    "Diseases:\n- item1\n\n"
    "Diagnoses:\n- item1\n\n"
    "Prescriptions:\n- item1\n- item2"

    # Get diagnosis and prediction from LLM
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a world-class medical Ai expert. Extract and format the insights exactly as shown below and Ensure your prediction must be medically accurate, reliable and written in very precise and in keywords or bullet point format:\n\n" 
                            "Adverse Events:\n- item1\n- item2\n\n"
                            "Diseases:\n- item1\n\n"
                            "Diagnoses:\n- item1\n\n"
                            "Prescriptions:\n- item1\n- item2"
                
            },
            {
                "role": "user",
                "content": transcribed_text
            }
        ],
        model="llama3-70b-8192"
    )

    rst = chat_completion.choices[0].message.content
    
    

          # Simple regex-based parsing (ensure LLM outputs in predictable format)
    # def extract(label):
    #     pattern = rf"{label}[:\-]\s*(.*?)(?=(\n[A-Z][a-z]+[:\-]|$))"
    #     match = re.search(pattern, rst, re.DOTALL | re.IGNORECASE)
    #     return match.group(1).strip() if match else "Not found"
    def extract(label, text):
        pattern = rf"{label}[:]\s*((?:- .+\n?)*)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            items = [line.strip("- ").strip() for line in match.group(1).strip().split("\n") if line.strip()]
            return items if items else ["Not found"]
        return ["Not found"]

    print(rst)
    print(repr(rst))

    adverse_event = extract("Adverse Events", rst)
    disease = extract("Diseases", rst)
    diagnosis = extract("Diagnoses", rst)
    prescription = extract("Prescriptions", rst)
    print(adverse_event)
    print(disease)
    print(diagnosis)

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





