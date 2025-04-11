import pandas as pd
import matplotlib.pyplot as plt
import openpyxl

# Load the Excel file
file_path = r"C:\Users\kaveri.s\Desktop\Macro\Integrationof MacrowithPython.xlsm"
wb = openpyxl.load_workbook(file_path)
ws = wb.active

# Read data from Excel
data = []
for row in ws.iter_rows(min_row=2, max_row=6, min_col=1, max_col=2, values_only=True):
    data.append(row)

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Student", "Marks"])

# Generate bar chart
plt.figure(figsize=(8, 5))
plt.bar(df["Student"], df["Marks"], color="skyblue", edgecolor="black")
plt.xlabel("Student")
plt.ylabel("Marks")
plt.title("Student Marks Comparison")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Save chart
chart_path = r"C:\Users\kaveri.s\Desktop\Macro\marks_chart.png"
plt.savefig(chart_path)
plt.show()

print("Chart generated successfully!")
