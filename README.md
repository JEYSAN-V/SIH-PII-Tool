# PII Detection Tool

A web-based tool for detecting and categorizing Personally Identifiable Information (PII) in text files. This tool helps identify sensitive information and distinguishes between PII and non-PII data.

## Features

- Upload and analyze text files for PII detection
- Real-time highlighting of detected PII and non-PII data
- Visual differentiation between PII and non-PII information
- Support for multiple PII types:
  - Personal Information (Names, Addresses)
  - Contact Information (Email, Phone Numbers)
  - Government IDs (SSN, Passport Numbers)
  - Financial Information (Bank Account Numbers, Credit Cards)
- Detection of non-PII data:
  - Product IDs
  - Transaction Amounts
  - Timestamps
  - Device Information
  - Browser Information

## Installation

1. Clone the repository:
```bash
git clone https://github.com/JEYSAN-V/SIH-PII-Tool.git
cd SIH-PII-Tool
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload a text file containing potential PII data

4. View the results:
   - PII data will be highlighted in red
   - Non-PII data will be highlighted in green
   - Results will be categorized in separate sections

## Dependencies

- Flask
- Presidio Analyzer
- Python 3.7+

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 