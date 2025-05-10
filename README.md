# Medical Conversation Analysis App

This application analyzes audio-based medical conversations between patients and healthcare professionals. Using powerful AI models, it transcribes conversations, extracts critical medical insights, and predicts possible adverse events.

The tool is designed to support early detection and documentation of patient symptoms, diagnoses, medications, and associated side effects.

---

## 🔍 Features

* ✨ **Automatic Transcription**: Converts voice recordings into accurate text (via Whisper or other ASR tools).
* ⚕️ **Medical Insight Extraction**: Detects and classifies mentions of:

  * Adverse Events
  * Diseases
  * Diagnoses
  * Prescriptions
* 🔍 **AI-Powered Summarization**: Uses OpenAI's GPT-4 for medical analysis.
* 🌐 **Web Interface**: Provides a clean, responsive UI for uploading audio and viewing results.
* 🔐 **Environment Variable Protection**: API keys are managed securely through a `.env` file.

---

## 🧱 Use Cases

* Hospitals and Clinics: Automate medical documentation
* Telemedicine Platforms: Enhance conversation analysis
* Medical Research: Track and study adverse reactions

---

## 📚 Technologies Used

* **Python 3.10+**
* **Flask**: Web framework
* **Jinja2**: Templating engine
* **OpenAI API**: GPT for insight extraction
* **Whisper (optional)**: Audio transcription
* **HTML/CSS**: UI design
* **Dotenv**: Secure config management

---

## 📁 Project Structure

```
medical-analysis-app/
├── app.py                   # Main Flask application
├── templates/              # HTML templates
│   ├── index.html          # Upload form
│   └── result.html         # Results display
├── static/                 # Optional CSS/JS files
├── .env                    # Secret API key (not pushed)
├── .gitignore              # Ignores sensitive files
├── requirements.txt        # Dependencies
└── README.md               # This file
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/medical-analysis-app.git
cd medical-analysis-app
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API Key

Create a `.env` file:

```ini
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the App

```bash
flask run
```

Navigate to: [http://localhost:5000](http://localhost:5000)

---

## 🔢 Sample Output

```
**Adverse Events:**
- Gastrointestinal distress
- Nausea
- Abdominal pain

**Diseases:**
- Type 2 Diabetes
- Hypertension

**Diagnoses:**
- Metformin-induced GI intolerance

**Prescriptions:**
- Glipizide 5 mg once daily
- Pantoprazole 40 mg daily
```

---

## 🚧 Security Best Practices

* Do **NOT** push `.env` files to public repositories
* Use `.gitignore` to exclude sensitive configs
* Always validate user inputs if expanding to file uploads

---

## 📊 Future Enhancements

* Upload audio file directly from UI
* PDF export of results
* Integration with EHR systems
* Multi-language transcription and extraction

---


