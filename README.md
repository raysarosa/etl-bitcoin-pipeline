# 📊 ETL Bitcoin Pipeline

This project implements a simple ETL (Extract, Transform, Load) pipeline that collects real-time Bitcoin price data from the Coinbase API and loads it into a PostgreSQL database.

---

## ⚙️ Technologies Used

- **Python 3**
- **Poetry** (for dependency management)
- **Requests** (to access the Coinbase API)
- **psycopg2** (to connect with PostgreSQL)
- **python-dotenv** (to manage environment variables)
- **TinyDB** (optional: for testing or lightweight storage)
- **PostgreSQL**

---

## 🧠 Project Structure
```bash
etl-bitcoin-pipeline/
├── src/
│ └── pipeline01.py # Main ETL pipeline script
├── .env # Environment variables (not uploaded)
├── .gitignore # Files to exclude from Git
├── pyproject.toml # Poetry configuration and dependencies
└── README.md # This file
```

---

## 📥 How It Works

1. **Extract**: Real-time BTC price is pulled from Coinbase API.
2. **Transform**: The raw JSON is cleaned and formatted (value, currency, timestamp).
3. **Load**: The data is saved into a PostgreSQL database (table created if not exists).

---

## 🛠 How to Run

1. **Clone the repository**
```bash
git clone https://github.com/raysarosa/etl-bitcoin-pipeline.git
cd etl-bitcoin-pipeline
```

2. **Install dependencies using Poetry**
```bash
poetry install
```

3. **Create a .env file in the root directory with your database credentials:**
```dotenv
DB_NAME=your_db_name
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

4. **Run the pipeline**
```bash
poetry run python src/pipeline01.py
```
The script runs in an infinite loop every 12 seconds. Press Ctrl + C to stop.

---

## 🛡️ .env and Security

This project uses a `.env` file to store sensitive database credentials (like password and user).  
This file is excluded from version control via `.gitignore`, keeping your information safe.

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) – feel free to use and adapt it.