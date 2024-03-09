from openpyxl import Workbook

# Create a new Workbook
wb = Workbook()

# Select the active worksheet
ws = wb.active

# Write "HELLO WORLD" to cell A1
ws['A1'] = "HELLO WORLD"

# Save the workbook
wb.save("Monitoring.xlsx")
