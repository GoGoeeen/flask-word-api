from flask import Flask, request, jsonify
from docx import Document

app = Flask(__name__)

# Route zum Erstellen eines Word-Dokuments
@app.route('/create-document', methods=['POST'])
def create_document():
    # Die Daten vom API-Call erhalten
    data = request.json
    replacements = data.get('replacements', {})

    # Word-Template öffnen und Platzhalter ersetzen
    doc = Document("template.docx")
    for paragraph in doc.paragraphs:
        for key, value in replacements.items():
            if key in paragraph.text:
                paragraph.text = paragraph.text.replace(key, value)

    # Dokument speichern
    file_name = "filled_document.docx"
    doc.save(file_name)

    return jsonify({"message": f"Document {file_name} created successfully!"})

# Hauptfunktion zum Starten der Flask-App
if __name__ == '__main__':
    app.run(debug=True)
