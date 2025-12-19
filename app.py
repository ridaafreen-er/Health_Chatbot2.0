from flask import Flask, render_template, request, jsonify 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def chatbot_response(user_input):
    user_input = user_input.lower().strip()

    if any(word in user_input for word in ["hello", "hi", "hey"]):
        return "Hello! I am Symptom Checker. How can I help you today?"
    if any(word in user_input for word in ["okay", "yeah", "ok", "ohh", "oh", "alright"]):
        return "Yeah! Anything else?"
    if any(word in user_input for word in ["how are you", "sup", "wassup"]):
        return "I'm doing great! Any symptoms bothering you?"

    
    disease_info = {

# ===== Viral Infections =====
"common cold": ["runny nose","sneezing","sore throat","cough","congestion"],
"flu": ["fever","chills","body aches","fatigue","headache","cough"],
"covid-19": ["fever","dry cough","tiredness","loss of taste","loss of smell","breathing difficulty"],
"dengue": ["high fever","headache","eye pain","joint pain","muscle pain","rash"],
"chikungunya": ["high fever","joint pain","muscle pain","headache","fatigue"],
"malaria": ["fever","chills","sweating","headache","nausea"],
"zika": ["fever","rash","joint pain","red eyes"],
"chickenpox": ["itchy rash","blisters","fever","fatigue"],
"measles": ["fever","rash","cough","runny nose","red eyes"],
"mumps": ["swollen cheeks","jaw pain","fever","headache"],
"hepatitis a": ["jaundice","fatigue","nausea","abdominal pain"],
"hepatitis b": ["jaundice","dark urine","fatigue","joint pain"],
"hepatitis c": ["fatigue","loss of appetite","jaundice"],

# ===== Bacterial Infections =====
"typhoid": ["high fever","weakness","stomach pain","diarrhea","constipation"],
"tuberculosis": ["chronic cough","weight loss","night sweats","fever"],
"pneumonia": ["cough","chest pain","fever","shortness of breath"],
"cholera": ["severe diarrhea","dehydration","vomiting"],
"urinary tract infection": ["burning urination","frequent urination","lower abdominal pain"],
"strep throat": ["sore throat","fever","swollen lymph nodes"],
"sinusitis": ["facial pain","nasal congestion","headache"],

# ===== Digestive Disorders =====
"acid reflux": ["heartburn","chest pain","regurgitation"],
"gastritis": ["stomach pain","nausea","bloating"],
"food poisoning": ["vomiting","diarrhea","stomach cramps","fever"],
"irritable bowel syndrome": ["abdominal pain","bloating","diarrhea","constipation"],
"ulcer": ["burning stomach pain","nausea","weight loss"],
"constipation": ["hard stools","abdominal discomfort"],
"diarrhea": ["loose stools","dehydration","stomach cramps"],

# ===== Respiratory Disorders =====
"asthma": ["shortness of breath","wheezing","chest tightness"],
"bronchitis": ["cough","mucus","fatigue","chest discomfort"],
"copd": ["chronic cough","breathlessness","wheezing"],
"allergic rhinitis": ["sneezing","itchy nose","runny nose"],

# ===== Heart & Blood =====
"hypertension": ["headache","dizziness","blurred vision"],
"hypotension": ["dizziness","fainting","fatigue"],
"heart attack": ["chest pain","shortness of breath","jaw pain","sweating"],
"anemia": ["fatigue","pale skin","shortness of breath"],
"stroke": ["face drooping","arm weakness","speech difficulty"],

# ===== Endocrine & Metabolic =====
"diabetes": ["frequent urination","increased thirst","fatigue","blurred vision"],
"hypothyroidism": ["weight gain","fatigue","cold intolerance"],
"hyperthyroidism": ["weight loss","anxiety","tremors","palpitations"],
"obesity": ["weight gain","joint pain","breathlessness"],

# ===== Skin Conditions =====
"eczema": ["itchy skin","dry patches","redness"],
"psoriasis": ["scaly skin","itching","red patches"],
"acne": ["pimples","oily skin","blackheads"],
"fungal infection": ["itching","red rash","scaling"],
"scabies": ["intense itching","skin burrows","rash"],

# ===== Neurological =====
"migraine": ["severe headache","nausea","light sensitivity"],
"epilepsy": ["seizures","loss of consciousness"],
"parkinson's disease": ["tremors","slow movement","muscle stiffness"],
"alzheimer's disease": ["memory loss","confusion","behavior changes"],

# ===== Mental Health =====
"anxiety disorder": ["nervousness","rapid heartbeat","sweating"],
"depression": ["sadness","loss of interest","fatigue","sleep problems"],
"panic attack": ["chest pain","fear","shortness of breath"],
"insomnia": ["difficulty sleeping","daytime fatigue"],

# ===== Bone & Muscle =====
"arthritis": ["joint pain","stiffness","swelling"],
"osteoporosis": ["bone weakness","fractures"],
"back pain": ["lower back pain","stiffness"],
"muscle strain": ["muscle pain","swelling","limited movement"],

# ===== Eye & ENT =====
"conjunctivitis": ["red eyes","itching","eye discharge"],
"ear infection": ["ear pain","fever","hearing loss"],
"tonsillitis": ["sore throat","swollen tonsils","fever"],
"glaucoma": ["eye pain","blurred vision","headache"],

# ===== Others =====
"dehydration": ["thirst","dry mouth","dark urine"],
"heat stroke": ["high body temperature","confusion","dizziness"],
"motion sickness": ["nausea","vomiting","dizziness"],
"food allergy": ["rash","swelling","breathing difficulty"]
}


    if "symptoms of" in user_input:
        disease = user_input.split("symptoms of")[-1].strip()
        if disease in disease_info:
            return f"The symptoms of {disease} are: {', '.join(disease_info[disease])}."
        else:
            return f"Sorry, I don't have information about that disease."
    matched_diseases = []

    for disease, symptoms in disease_info.items():
        for symptom in symptoms:
            if symptom in user_input:
                matched_diseases.append(disease)
                break   # avoid duplicate disease entry

    if matched_diseases:
        return (
            f"The symptom you mentioned is seen in multiple diseases: "
            f"{', '.join(matched_diseases)}. "
            f"For accurate diagnosis, consult a doctor."
        )

    if any(word in user_input for word in ["thank you","thanks","thx", "thanku","thankyou","bye","goodbye","see you later","c ya"]):
        return f"You're welcome! Take care and stay healthy."

    return f"I didn't understand. Try 'symptoms of dengue' or 'I have fever'."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"reply": "Invalid request"}), 400
        user_message = data["message"]
        bot_reply = chatbot_response(user_message)
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": "Server error"}), 500

if __name__ == "__main__":
    app.run(debug=True) 