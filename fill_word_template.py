from docx import Document

# Funktion zum Füllen eines Word-Templates
def fill_template(template_path, output_path, replacements):
    # Vorlage laden
    doc = Document(template_path)

    # Platzhalter ersetzen
    for paragraph in doc.paragraphs:
        for key, value in replacements.items():
            if key in paragraph.text:
                paragraph.text = paragraph.text.replace(key, value)

    # Dokument speichern
    doc.save(output_path)
    print(f"Dokument gespeichert als {output_path}")

# Beispiel-Daten
replacements = {
    "{{Firma}}": "Musterfirma GmbH",
    "{{Datum}}": "10.01.2025",
    "{{Ansprechpartner}}": "Max Mustermann"
}

# Template füllen
fill_template("template.docx", "filled_document.docx", replacements)
