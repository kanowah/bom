import pandas as pd
from datetime import datetime
import os

# Get today's date for suffix
date_suffix = datetime.now().strftime("%d%b")  # e.g., "08Apr"

# Paths
original_file = "EZ_STMT.csv"
output_excel = f"EZ_Statement_Cleaned_{date_suffix}.xlsx"
renamed_source = f"EZ_STMT_{date_suffix}.csv"

# Step 1: Read and clean raw lines
all_lines = []
with open(original_file, "r", encoding="utf-8") as file:
    for line in file:
        stripped = line.strip()
        if not stripped or set(stripped) <= {"-", "|"}:
            continue  # Skip empty lines and separator lines
        all_lines.append(stripped)

# Step 2: Combine multiline records (starting with 1D, 2C, etc.)
combined_rows = []
current_row = ""

for line in all_lines:
    if line[:2] in ("1D", "2C"):  # Add more types if needed
        if current_row:
            combined_rows.append(current_row)
        current_row = line
    else:
        current_row += " " + line

if current_row:
    combined_rows.append(current_row)

# Step 3: Split into columns using pipe (|) delimiter
all_data = [row.split("|") for row in combined_rows]

# Step 4: Create a DataFrame
df = pd.DataFrame(all_data)

# Step 5: Clean DataFrame
df = df.dropna(axis=1, how="all")  # Drop columns that are entirely empty
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

# Step 6: Optional: Rename first few columns for clarity
df.rename(columns={
    0: "Type",
    1: "Amount",
    2: "TransactionID",
    3: "Details1",
    4: "Details2",
    5: "FromParty",
    6: "ToParty",
    7: "Code",
    8: "Debit",
    9: "Credit"
}, inplace=True)

# Step 7: Save to Excel with date-based name
df.to_excel(output_excel, index=False)

# Step 8: Rename the source CSV file with same suffix
os.rename(original_file, renamed_source)

print(f"Data saved to '{output_excel}'")
print(f"Original file renamed to '{renamed_source}'")
