from flask import Flask, render_template, request, send_file
import os
import pandas as pd
import uuid
import clickhouse_connect

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Connect to ClickHouse
client = clickhouse_connect.get_client(
    host='localhost',      # Change if you're using Docker with a different IP
    port=8123,
    username='default',
    password='',
    database='default'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    table_name = request.form.get('table_name')

    if not file or not table_name:
        return "Missing file or table name", 400

    file_ext = os.path.splitext(file.filename)[1].lower()
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}{file_ext}")
    file.save(filepath)

    try:
        # Handle both JSON array and JSON lines
        if file_ext == '.csv':
            df = pd.read_csv(filepath)
        elif file_ext == '.json':
            try:
                df = pd.read_json(filepath)  # Try JSON array
            except ValueError:
                df = pd.read_json(filepath, lines=True)  # Try JSON lines
        else:
            return "Unsupported file type. Use .csv or .json", 400
    except Exception as e:
        os.remove(filepath)
        return f"Error reading file: {str(e)}", 500

    os.remove(filepath)

    # Create ClickHouse table if it doesn't exist
    try:
        columns = ', '.join([f'`{col}` String' for col in df.columns])
        create_query = f"""
            CREATE TABLE IF NOT EXISTS `{table_name}` ({columns})
            ENGINE = MergeTree()
            ORDER BY tuple()
        """
        client.command(create_query)
        client.insert_dataframe(table_name, df)
    except Exception as e:
        return f"ClickHouse error: {str(e)}", 500

    return f"Successfully uploaded {len(df)} rows to '{table_name}'"

@app.route('/download', methods=['POST'])
def download():
    table_name = request.form.get('table_name')
    file_format = request.form.get('format', 'csv').lower()
    filename = f"{table_name}_export.{file_format}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        df = client.query_df(f"SELECT * FROM `{table_name}`")
    except Exception as e:
        return f"Error fetching data: {str(e)}", 500

    try:
        if file_format == 'csv':
            df.to_csv(filepath, index=False)
        elif file_format == 'json':
            df.to_json(filepath, orient='records', lines=True)
        else:
            return "Unsupported format. Choose 'csv' or 'json'.", 400
    except Exception as e:
        return f"Error writing file: {str(e)}", 500

    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)