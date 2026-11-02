from flask import Flask, render_template_string
import pandas as pd
import os

app = Flask(__name__)

# Load the student performance dataset
DATASET_PATH = os.path.join(
    os.path.dirname(__file__),
    "student_performance_dataset.csv"
)


def load_data():
    if not os.path.exists(DATASET_PATH):
        return pd.DataFrame()

    return pd.read_csv(DATASET_PATH)


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Academic Performance Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            margin: 0;
            padding: 20px;
        }

        h1 {
            color: #173b70;
            text-align: center;
        }

        .container {
            max-width: 1100px;
            margin: auto;
        }

        .cards {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin: 20px 0;
        }

        .card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            flex: 1;
            min-width: 150px;
            box-shadow: 0 2px 8px #ddd;
        }

        .card h3 {
            color: #475569;
        }

        .card p {
            font-size: 25px;
            color: #2563eb;
            font-weight: bold;
        }

        .table-box {
            background: white;
            padding: 15px;
            border-radius: 10px;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            padding: 10px;
            border: 1px solid #ddd;
            text-align: left;
        }

        th {
            background: #2563eb;
            color: white;
        }

        tr:nth-child(even) {
            background: #f8fafc;
        }

        .note {
            color: #475569;
            margin-top: 20px;
        }
    </style>
</head>

<body>
<div class="container">

    <h1>Student Academic Performance Dashboard</h1>

    <p>Overview of student academic performance and dataset information.</p>

    {% if error %}
        <h3>{{ error }}</h3>
    {% else %}

    <div class="cards">
        <div class="card">
            <h3>Total Records</h3>
            <p>{{ rows }}</p>
        </div>

        <div class="card">
            <h3>Total Columns</h3>
            <p>{{ cols }}</p>
        </div>

        <div class="card">
            <h3>Numeric Subjects / Fields</h3>
            <p>{{ numeric_count }}</p>
        </div>
    </div>

    <div class="table-box">
        <h2>Student Dataset Preview</h2>

        {% if headers %}
        <table>
            <thead>
                <tr>
                    {% for header in headers %}
                    <th>{{ header }}</th>
                    {% endfor %}
                </tr>
            </thead>

            <tbody>
                {% for row in data %}
                <tr>
                    {% for value in row %}
                    <td>{{ value }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <p>The dataset does not contain any columns.</p>
        {% endif %}
    </div>

    <p class="note">
        Showing up to 20 records from your student performance dataset.
    </p>

    {% endif %}

</div>
</body>
</html>
"""


@app.route("/")
def dashboard():
    try:
        df = load_data()

        if df.empty:
            return render_template_string(
                HTML,
                error="Your dataset is empty. Please check the CSV file.",
                rows=0,
                cols=0,
                numeric_count=0,
                headers=[],
                data=[]
            )

        df = df.fillna("Not Available")

        return render_template_string(
            HTML,
            error=None,
            rows=len(df),
            cols=len(df.columns),
            numeric_count=len(
                df.select_dtypes(include="number").columns
            ),
            headers=df.columns.tolist(),
            data=df.head(20).values.tolist()
        )

    except Exception as e:
        app.logger.exception("Dashboard loading failed")
        return (
            "Unable to load the dashboard. "
            "Please check the dataset and deployment logs.",
            500
        )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
