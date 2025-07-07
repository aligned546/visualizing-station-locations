import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import re

# ---------------------------
# 1. Set working directory
# ---------------------------
folder = os.path.dirname(os.path.abspath(__file__))

input_dir = os.path.join(folder, "filtered_analytes")
output_csv_dir = os.path.join(folder, "unique_stations")
output_shp_dir = os.path.join(folder, "unique_station_shapefiles")

os.makedirs(output_csv_dir, exist_ok=True)
os.makedirs(output_shp_dir, exist_ok=True)

# ---------------------------
# 2. List of analyte files
# ---------------------------
analyte_files = [
    "Coliform,Fecal.csv",
    "Coliform,Total.csv",
    "E. coli.csv",
    "Enterococcus.csv",
    "Lead, Total.csv",
    "Nickel, Dissolved.csv",
    "Selenium, Dissolved.csv",
    "Total Suspended Solids, Total.csv",
    "Turbidity, Total.csv",
    "Zinc, Dissolved.csv"
]

# ---------------------------
# 3. Loop through analyte files
# ---------------------------
for analyte_file in analyte_files:
    input_path = os.path.join(input_dir, analyte_file)
    
    if not os.path.isfile(input_path):
        print(f"⚠️ File not found: {analyte_file}")
        continue

    # Load the file
    df = pd.read_csv(input_path, dtype=str)
    df.columns = df.columns.str.strip()

    # Keep only needed columns
    keep_cols = ['StationName', 'latitude', 'longitude']
    missing = [col for col in keep_cols if col not in df.columns]
    if missing:
        print(f"⚠️ Missing columns in {analyte_file}: {missing}")
        continue

    # Drop duplicates on StationName
    unique_stations = df[keep_cols].drop_duplicates(subset=['StationName'])

    # ---------------------------
    # Save CSV
    # ---------------------------
    safe_name = re.sub(r'[^\w]+', '-', analyte_file.replace('.csv', '')).strip('-').lower()
    output_csv_name = f"{safe_name}-stations.csv"
    output_csv_path = os.path.join(output_csv_dir, output_csv_name)
    unique_stations.to_csv(output_csv_path, index=False)

    # ---------------------------
    # Create GeoDataFrame
    # ---------------------------
    unique_stations['latitude'] = pd.to_numeric(unique_stations['latitude'], errors='coerce')
    unique_stations['longitude'] = pd.to_numeric(unique_stations['longitude'], errors='coerce')
    unique_stations = unique_stations.dropna(subset=['latitude', 'longitude'])

    geometry = [Point(xy) for xy in zip(unique_stations['longitude'], unique_stations['latitude'])]
    gdf = gpd.GeoDataFrame(unique_stations, geometry=geometry, crs="EPSG:4326")

    # ---------------------------
    # Save Shapefile
    # ---------------------------
    output_shp_name = f"{safe_name}-stations.shp"
    output_shp_path = os.path.join(output_shp_dir, output_shp_name)
    gdf.to_file(output_shp_path)

    print(f"✅ Saved: {output_csv_name} and {output_shp_name}")

print("\n🎉 All unique station CSVs and shapefiles saved.")
