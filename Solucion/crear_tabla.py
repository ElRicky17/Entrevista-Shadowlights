import duckdb

con = duckdb.connect('ads_warehouse.duckdb')

con.execute("""
CREATE TABLE IF NOT EXISTS ads_spend (
  date DATE,
  platform TEXT,
  account TEXT,
  campaign TEXT,
  country TEXT,
  device TEXT,
  spend DOUBLE,
  clicks INTEGER,
  impressions INTEGER,
  conversions INTEGER,
  load_date TIMESTAMP,
  source_file_name TEXT
);
""")

print("Tablas disponibles:", con.execute("SHOW TABLES").fetchall())
