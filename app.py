from flask import Flask, request, jsonify
from fill_word_template import fill_template
from upload_to_sharepoint import upload_to_sharepoint
import re

app = Flask(__name__)

# Route zum Erstellen eines Dokuments
@app.route('/create-document', methods=['POST'])
def create_document():
    # JSON-Daten aus dem Request extrahieren
    data = request.get_json()

    # Überprüfen, ob alle erforderlichen Daten vorhanden sind
    if not data or not all(k in data for k in ("Firma", "Datum", "Ansprechpartner")):
        return jsonify({"error": "Invalid data"}), 400

    # Dynamischer Dateiname basierend auf dem Firmennamen
    firm_name_cleaned = re.sub(r'[^\w\s]', '', data["Firma"]).replace(" ", "_")
    document_name = f"filled_document_{firm_name_cleaned}.docx"

    # Daten aus dem Request verwenden
    replacements = {
        "{{Firma}}": data["Firma"],
        "{{Datum}}": data["Datum"],
        "{{Ansprechpartner}}": data["Ansprechpartner"]
    }

    # Word-Template füllen
    fill_template("template.docx", document_name, replacements)

    # Dokument auf SharePoint hochladen
    upload_to_sharepoint(document_name, document_name)

    return jsonify({"message": f"Document {document_name} created successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)