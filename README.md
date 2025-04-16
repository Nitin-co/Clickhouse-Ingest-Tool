
#  ClickHouse & Flat File Ingestion Tool

A lightweight Flask-based web application that supports **bidirectional ingestion** between flat files (`.csv`, `.json`) and a **ClickHouse database**.

This tool is designed to streamline the import/export of structured data for analytics and testing.

---

##  Features

✅ Upload `.csv` or `.json` files  
✅ Automatically create corresponding tables in ClickHouse  
✅ Insert uploaded data into ClickHouse  
✅ Export ClickHouse tables back to CSV or JSON  
✅ Built-in browser interface  
✅ Lightweight, clean, and testable

---

## Technologies Used

- Python 3
- Flask (Web Framework)
- Pandas (Data Parsing)
- [ClickHouse Connect](https://github.com/ClickHouse/clickhouse-connect) (Python client)
- HTML (Minimal Frontend)

---

##  Project Structure

```
clickhouse-flask-ingestion/
├── app.py                  # Main application
├── sample_data.csv         # Example CSV upload file
├── sample_data.json        # Example JSON upload file
├── requirements.txt        # Python dependencies
├── README.md               # You're here!
└── uploads/                # Temporary file upload folder
```

---

##  Installation & Setup

1. **Clone this repository**

```bash
git clone https://github.com/your-username/clickhouse-flask-ingestion.git
cd clickhouse-flask-ingestion
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Start ClickHouse**

Make sure ClickHouse is running locally (port `9000`).

- On Windows, you can run `clickhouse-server.exe`  
- Or install via Docker if needed (optional)

4. **Run the App**

```bash
python app.py
```

Visit: [http://localhost:5000](http://localhost:5000)

---

##  License

MIT License. Feel free to reuse, modify, and contribute!
