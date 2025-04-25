# libs 
import pandas as pd
import sqlite3

conn = sqlite3.connect('attendance.db')
# attendance input :
attendance_report = pd.read_sql_query("SELECT * FROM attendance", conn)
conn.close()

# convert csv
attendance_report.to_csv('attendance_report.csv', index=False)
print(" The Requested Report has been saved as : attendance_report.csv")