import sqlite3
import pandas as pd

# load csv into pandas
df = pd.read_csv("train.csv")

# remove space from column names
df.columns = df.columns.str.strip()

# Convert 'Sales' column to a numeric type by removing '$' and ','
df["Sales"] = df["Sales"].replace('[\$,]', '', regex=True).astype(float)

# Convert 'Order Date' to a standard datetime format (YYYY-MM-DD)
df["Order Date"] = pd.to_datetime(df["Order Date"], format='%d/%m/%Y', errors='coerce').dt.strftime('%Y-%m-%d')

# connect SQlite "creates a local DB file"
conn = sqlite3.connect("sales.db")

# Write dataframe into a SQL table
df.to_sql("orders", conn, if_exists="replace", index=False)

# Read SQL queries from file
with open("queries.sql", "r") as f:
    sql_script = f.read()

# Split queries by semicolon (;) and run each
for i, query in enumerate(sql_script.split(";"), start=1):
    query = query.strip()
    if query:  # avoid empty lines
        print(f"\n Running Query {i}:\n{query}\n")
        try:
            result = pd.read_sql_query(query, conn)
            print(result.head())  # show preview in terminal

            # Save results to outputs folder
            output_path = f"outputs/query_{i}.csv"
            result.to_csv(output_path, index=False)
            print(f" Saved results to {output_path}")

        except Exception as e:
            print(f" Error: {e}")

# Close DB connection
conn.close()
print("\nAll queries executed and saved successfully! ")