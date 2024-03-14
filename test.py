from openpyxl import Workbook

# Create a new Workbook
wb = Workbook()

# Select the active worksheet
ws = wb.active

# Write "Hello world" in uppercase to cell A1
# ws['C4'] = "Hello world"
ws.cell(row=3, column=4).value = "Hello world"

# Write "Hello world" in lowercase to cell A2

# Save the workbook
wb.save("monitoring.xlsx")
