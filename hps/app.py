from flask import Flask, request, render_template_string
import boto3

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Lecture DynamoDB</title>
</head>
<body>
    <h1>Rechercher un élément DynamoDB</h1>
    <form method="POST">
        <label>Région AWS :</label><br>
        <input type="text" name="region" placeholder="ex: eu-west-1" required><br><br>

        <label>Nom de la table :</label><br>
        <input type="text" name="table" required><br><br>

        <label>Nom de la clé primaire :</label><br>
        <input type="text" name="primary_key_name" required><br><br>

        <label>Valeur de la clé :</label><br>
        <input type="text" name="primary_key_value" required><br><br>

        <input type="submit" value="Rechercher">
    </form>

    {% if item %}
        <h2>Résultat :</h2>
        <ul>
        {% for key, value in item.items() %}
            <li><strong>{{ key }}</strong> : {{ value }}</li>
        {% endfor %}
        </ul>
    {% elif item is not none %}
        <p>Aucun élément trouvé.</p>
    {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    item = None
    if request.method == "POST":
        region = request.form["region"]
        table_name = request.form["table"]
        key_name = request.form["primary_key_name"]
        key_value = request.form["primary_key_value"]

        try:
            dynamodb = boto3.resource('dynamodb', region_name=region)
            table = dynamodb.Table(table_name)
            response = table.get_item(Key={key_name: key_value})
            item = response.get("Item", {})
            if not item:
                item = {}
        except Exception as e:
            item = {"Erreur": str(e)}

    return render_template_string(HTML_FORM, item=item)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
