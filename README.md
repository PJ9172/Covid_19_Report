# 🦠 COVID-19 Report Application

This is a full-stack COVID-19 reporting tool built with a Go web server on the frontend and a Python (Flask + PySpark) microservice on the backend. It visualizes COVID-19 stats for a given country using a pie chart and a summary section.

---

## 📌 Features

- 🔍 Input a country name and get COVID-19 statistics.
- 📊 Pie chart showing breakdown of deaths and recoveries.
- 📄 Summary section with numeric data.
- ⚙️ PySpark processes large CSV files for accurate reporting.
---

## 🏗️ Tech Stack

| Layer          | Tech Used              |
|----------------|------------------------|
| Frontend       | Go, HTML, Chart.js     |
| Backend        | Python (Flask), PySpark|
| Data Source    | Johns Hopkins COVID-19 time series CSVs |

---
## 📁 Project Structure
```
COVID-19-REPORT/
│
├── go-webapp/             # Frontend (Go)
│   ├── handlers/          # Go handlers
│   ├── routers/           # Routing
│   ├── templates/         # HTML templates
│   └── main.go            # Main server entry point
│
├── py-service/            # Backend (Python Flask + PySpark)
│   ├── data/              # CSV data files
│   └── main.py            # Flask API using PySpark
│
├── Screenshots/           # Output previews
└── .gitignore
```

---

## 🚀 Getting Started

### 1. Clone the Project

```bash
git clone https://github.com/PJ9172/Covid_19_Report.git
cd COVID-19-REPORT
```

### 2. Install Libraries
```bash
pip install pyspark flask
```

### 3. Start the Go Web App
```bash
cd go-webapp
go run main.go
```

### 4. Start the Flask API
```bash
cd py-service
python main.py
```

---

## 🔍 Usage

- Visit http://localhost:3000/

- Enter a Country name (e.g., India)

---

## 📸 Screenshots
   ![landing_page](/Screenshots/landing_page.png)
   ![result_page](/Screenshots/result_page.png)

---

## 🤝 Credits
- Go + Gorilla Mux for clean server-side routing

- Flask API for fast Python microservice

- PySpark for fast processing CSV & Parquet

- Johns Hopkins for open COVID-19 data