## visualizing-station-locations
I made this script for processing different water quality analyte CSV files (generated through the `clip-tsv-to-shapefileclip-tsv-to-shapefile` and `splitting-csv-to-column-values` scripts on my github). For each analyte file, it:

- Extracts unique monitoring stations (`StationName`, `latitude`, `longitude`).
- Generates a shapefile of station points (EPSG:4326) into a `unique_station_shapefiles` folder.

## Requirements
`pandas`, `geopandas`, `shapely`
