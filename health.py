import pandas as pd
from fastapi import FastAPI

app = FastAPI()

# 1. Load your separate raw files once when the server starts
data1 = pd.read_csv('cleaned_Health_indicator_data.csv') 
data2 = pd.read_csv('cleaned_country_data.csv') 
data      

# 2. Clean column typography layout
data1.columns = data1.columns.str.strip().str.lower()
data2.columns = data2.columns.str.strip().str.lower()

# 3. Perform the Master Merge 
# This attaches country_name, region, and income_level to every health record
merged_df = pd.merge(data1, data2, on='country_code', how='left')

@app.get("/api/dashboard/{country_code}")
def get_dashboard_data(country_code: str):
    # Filter the master merged dataset for the requested country
    country_df = merged_df[merged_df['country_code'] == country_code.upper()]
    
    # Sort chronologically so your line and stacked bar charts animate correctly
    country_df = country_df.sort_values(by='year')
    
    # Convert to a clean JSON array of objects to feed your frontend charts directly
    return country_df.to_dict(orient='records')
