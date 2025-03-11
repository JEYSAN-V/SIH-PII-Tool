from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import re
from werkzeug.utils import secure_filename
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
ALLOWED_EXTENSIONS = {'txt'}

# Define PII and non-PII patterns
PII_PATTERNS = {
    'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'PHONE_NUMBER': r'\b(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
    'SSN': r'\b\d{3}[-.]?\d{2}[-.]?\d{4}\b',
    'CREDIT_CARD': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
    'PASSPORT': r'\b[A-Z][0-9]{8}\b',
    'BANK_ACCOUNT': r'\b\d{8,12}\b'
}

NON_PII_PATTERNS = {
    'PRODUCT_ID': r'\b[A-Z]{2}\d{5}\b',
    'AMOUNT': r'\$\d+(?:\.\d{2})?',
    'ZIP_CODE': r'\b\d{5}(?:-\d{4})?\b',
    'TIMESTAMP': r'\b\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\b',
    'BROWSER_INFO': r'\b[A-Za-z]+\s\d+\.\d+\b',
    'DEVICE_MODEL': r'\b[A-Za-z]+\s[A-Za-z]+\s[A-Za-z0-9]+\b'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_pii(text):
    results = []
    
    # Check for PII patterns
    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.finditer(pattern, text)
        for match in matches:
            results.append({
                'entity': pii_type,
                'text': match.group(),
                'start': match.start(),
                'end': match.end(),
                'isPII': True
            })
    
    # Check for non-PII patterns
    for non_pii_type, pattern in NON_PII_PATTERNS.items():
        matches = re.finditer(pattern, text)
        for match in matches:
            results.append({
                'entity': non_pii_type,
                'text': match.group(),
                'start': match.start(),
                'end': match.end(),
                'isPII': False
            })
    
    # Use Presidio for additional entity types
    analyzer = AnalyzerEngine()
    presidio_results = analyzer.analyze(
        text=text,
        entities=[
            "PERSON",
            "LOCATION",
            "DATE_TIME",
            "NRP",
            "URL",
            "US_DRIVER_LICENSE",
            "US_BANK_NUMBER",
            "LOCATION",
            "ADDRESS"
        ],
        language="en"
    )
    
    # Add Presidio results (all considered PII)
    for result in presidio_results:
        results.append({
            'entity': result.entity_type,
            'text': text[result.start:result.end],
            'start': result.start,
            'end': result.end,
            'isPII': True
        })
    
    # Sort results by start position
    results.sort(key=lambda x: x['start'])
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            pii_result = detect_pii(text)
            
            # Count PII and non-PII items
            pii_count = sum(1 for r in pii_result if r['isPII'])
            non_pii_count = len(pii_result) - pii_count
            
            # Clean up the uploaded file after processing
            os.remove(filepath)
            
            return jsonify({
                'message': f'File processed successfully. Found {pii_count} PII and {non_pii_count} non-PII items.',
                'pii_result': pii_result,
                'total_findings': len(pii_result)
            }), 200
        except Exception as e:
            return jsonify({'message': f'Error processing file: {str(e)}'}), 500
    else:
        return jsonify({'message': 'Only text files are allowed'}), 400

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
