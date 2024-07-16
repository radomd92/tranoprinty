from flask import Flask, request, render_template_string
import cups

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Trano Printy Chaville</title>
</head>
<body>
    <h1>Atontan-taratasy ho aprinty</h1>
    <form action="/atonta" method="post" enctype="multipart/form-data">
    <p>
        <label for="file">Rakitra ho atonta (PDF ihany):</label>
        <input type="file" id="file" name="file" accept=".pdf">
    </p>
        <br>
        <p>
        <label for="printer">Printera :</label>
        <select id="printer" name="printer">
            {% for printer in printers %}
            <option value="{{ printer }}">{{ printer }}</option>
            {% endfor %}
        </select>
        </p>
        <br>
        <input type="submit" value="Atonta printy">
    </form>
</body>
</html>
"""


@app.route('/')
def form():
    conn = cups.Connection()
    printers = conn.getPrinters()
    return render_template_string(HTML_FORM, printers=printers.keys())


@app.route('/atonta', methods=['POST'])
def print_file():
    file = request.files['file']
    printer_name = request.form['printer']

    if file and file.filename.endswith('.pdf'):
        filepath = f'/tmp/{file.filename}'
        file.save(filepath)

        # Printing options
        options = {
            "copies": "1",
            "media": "A4",
            "sides": "two-sided-long-edge"
        }

        # Send to printer
        try:
            conn = cups.Connection()
            conn.printFile(printer_name, filepath, "", options)
            return f"Lasa soa aman-tsra any amin'ny {printer_name} ny {file.filename}."
        except Exception as e:
            return f'Tsy nahatonta printy: {str(e)}'
    else:
        return "Rakitra tsy azo raisina. Mampidiran PDF azafady."


if __name__ == '__main__':
    app.run(debug=True)
