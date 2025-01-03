import os
import pandas as pd
import sqlite3

# Define file paths
download_url = "https://www.skagitcounty.net/Assessor/Documents/DataDownloads/AssessorData.zip"
zip_file_path = "AssessorData.zip"
database_path = "/workspaces/skagit-regression/persistent_data.db"
table_name = "cleaned_assessors_data"

# Step 1: Download the file if it doesn't exist
if not os.path.exists(zip_file_path):
    import requests
    print("Downloading AssessorData.zip...")
    response = requests.get(download_url)
    with open(zip_file_path, "wb") as file:
        file.write(response.content)
    print("Download complete.")

# Step 2: Read and clean the data
print("Processing data...")
datadf = pd.read_csv(zip_file_path, sep="|", encoding="ISO 8859-1", on_bad_lines="skip")

# Drop unwanted columns
columns_to_drop = [
    "Account Number", "Legal Description", "Old Street Number", "Old Street Name",
    "Old City State Zip", "Owner Name", "Owner Add 1", "Owner Add 2", "Owner Add 3",
    "Owner City", "Owner State", "Owner Zip", "Exemptions", "Tot Special Assessments",
    "General Taxes", "Inactive Date", "Levy Code", "Senior Exemption Adjustment",
    "Township", "Range", "Section", "Quarter Section"
]
datadf = datadf.drop(columns=columns_to_drop, axis=1)

# Apply filters
datadf = datadf[
    (datadf['Appraisal Year'] >= 2025) &
    (datadf['Assessed Value'] > 0) &
    (datadf['Taxable Value'] > 0) &
    (datadf['Total Market Value'] > 0)
]

allowed_land_use = [
    "(110) HOUSEHOLD SFR OUTSIDE CITY",
    "(190) VACATION AND CABIN",
    "(111) HOUSEHOLD, SFR, INSIDE CITY",
    "(180) MOBILE HOMES",
    "(120) HOUSEHOLD, 2-4 UNITS",
    "(112) HOUSEHOLD SFR, WITH A DETACHED UNIT",
    "(113) HOUSEHOLD SFR, WITH 2+ DETACHED UNITS"
]
datadf = datadf[datadf['Land Use'].isin(allowed_land_use)]

# Step 3: Save the cleaned data to SQLite database
print(f"Saving cleaned data to SQLite database at {database_path}...")

# Connect to the SQLite database
conn = sqlite3.connect(database_path)

# Write the data to the specified table, replacing it if it already exists
datadf.to_sql(table_name, conn, if_exists='replace', index=False)

# Close the database connection
conn.close()

print(f"Cleaned data saved to table '{table_name}' in {database_path}.")
