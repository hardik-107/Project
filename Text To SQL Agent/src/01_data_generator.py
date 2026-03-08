import sqlite3
import json
import os

# Absolute path setup (bulletproof pathing)
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "data")

os.makedirs(data_dir, exist_ok=True)

db_path = os.path.join(data_dir, "company_data.db")
jsonl_path = os.path.join(data_dir, "synthetic_queries.jsonl")

def setup_database():
    """Creates a dummy database for the agent to interact with."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            emp_id INTEGER PRIMARY KEY,
            name TEXT,
            department TEXT,
            salary INTEGER,
            hire_date TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY,
            emp_id INTEGER,
            amount INTEGER,
            region TEXT,
            sale_date TEXT,
            FOREIGN KEY(emp_id) REFERENCES employees(emp_id)
        )
    """)

    cursor.execute("DELETE FROM employees")
    cursor.execute("DELETE FROM sales")
    
    employees_data = [
        (1, 'Rahul', 'Engineering', 120000, '2023-01-15'),
        (2, 'Priya', 'Sales', 85000, '2023-03-22'),
        (3, 'Amit', 'Sales', 90000, '2022-11-10'),
        (4, 'Neha', 'HR', 70000, '2024-01-05')
    ]
    
    sales_data = [
        (101, 2, 15000, 'North', '2025-01-10'),
        (102, 3, 20000, 'West', '2025-01-15'),
        (103, 2, 12000, 'North', '2025-02-20')
    ]

    cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?)", employees_data)
    cursor.executemany("INSERT INTO sales VALUES (?, ?, ?, ?, ?)", sales_data)
    
    conn.commit()
    conn.close()
    print(f"Database created successfully with data at: {db_path}")

def generate_training_data():
    """Generates a small synthetic dataset for fine-tuning."""
    training_examples = [
        {
            "instruction": "You are a SQL expert. Write a SQL query to answer the user's question based on the schema: employees(emp_id, name, department, salary, hire_date), sales(sale_id, emp_id, amount, region, sale_date).",
            "input": "How many employees work in the Sales department?",
            "output": "SELECT COUNT(*) FROM employees WHERE department = 'Sales';"
        },
        {
            "instruction": "You are a SQL expert. Write a SQL query to answer the user's question based on the schema: employees(emp_id, name, department, salary, hire_date), sales(sale_id, emp_id, amount, region, sale_date).",
            "input": "What is the total sales amount for the North region?",
            "output": "SELECT SUM(amount) FROM sales WHERE region = 'North';"
        },
        {
            "instruction": "You are a SQL expert. Write a SQL query to answer the user's question based on the schema: employees(emp_id, name, department, salary, hire_date), sales(sale_id, emp_id, amount, region, sale_date).",
            "input": "Find the name of the employee with the highest salary.",
            "output": "SELECT name FROM employees ORDER BY salary DESC LIMIT 1;"
        }
    ]

    with open(jsonl_path, "w") as f:
        for example in training_examples:
            f.write(json.dumps(example) + "\n")
            
    print(f"Training data generated successfully with data at: {jsonl_path}")

if __name__ == "__main__":
    setup_database()
    generate_training_data()