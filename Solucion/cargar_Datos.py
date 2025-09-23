import duckdb
import pandas as pd
from datetime import datetime
import os


con = duckdb.connect('ads_warehouse.duckdb')


file_path = "C:/Users/david/Downloads/File.csv" 
df = pd.read_csv(file_path)

df['load_date'] = datetime.now()
df['source_file_name'] = os.path.basename(file_path)

con.register("df_view", df)
con.execute("""
INSERT INTO ads_spend
SELECT * FROM df_view
""")

print("Filas en ads_spend:", con.execute("SELECT COUNT(*) FROM ads_spend").fetchone()[0])
print("Primeras filas:", con.execute("SELECT * FROM ads_spend LIMIT 5").fetchdf())
