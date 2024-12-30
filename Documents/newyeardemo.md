# GEEScan API Testing Commands

## Test GEE Authentication
```powershell
Invoke-RestMethod -Uri 'http://localhost:5000/api/test' -Method GET | ConvertTo-Json -Depth 10
```
Output:
```json
{
    "gee_init": {
        "message": "Authentication successful",
        "status": "success"
    },
    "message": "GEE connection successful",
    "status": "success",
    "test_image_info": {
        "bands": [
            {
                "crs": "EPSG:4326",
                "crs_transform": [
                    0.0002777777777777778,
                    0,
                    -180.0001388888889,
                    0,
                    -0.0002777777777777778,
                    60.00013888888889
                ],
                "data_type": {
                    "max": 32767,
                    "min": -32768,
                    "precision": "int",
                    "type": "PixelType"
                },
                "dimensions": [
                    1296001,
                    417601
                ],
                "id": "elevation"
            }
        ],
        "id": "USGS/SRTMGL1_003",
        "type": "Image",
        "version": 1641990767055141
    }
}
```

## List All AOIs
```powershell
Invoke-RestMethod -Uri 'http://localhost:5000/api/aois' -Method GET | ConvertTo-Json -Depth 10
```
Output:
```json
{
    "aois": [
        {
            "geometry": "{\"type\":\"Polygon\",\"coordinates\":[[[-74.006,40.7128],[-74.0065,40.7128],[-74.0065,40.7123],[-74.006,40.7123],[-74.006,40.7128]]]}",
            "id": 1,
            "name": "Test AOI"
        },
        {
            "geometry": "{\"type\":\"Polygon\",\"coordinates\":[[[-74.006,40.7128],[-74.0065,40.7128],[-74.0065,40.7123],[-74.006,40.7123],[-74.006,40.7128]]]}",
            "id": 2,
            "name": "Test AOI"
        },
        {
            "geometry": "{\"type\":\"Point\",\"coordinates\":[-73.9857,40.758]}",
            "id": 9,
            "name": "PowerShell Created AOI"
        }
    ],
    "message": "Successfully fetched AOIs"
}
```

## Export AOI to Earth Engine Asset
```powershell
$body = @{start_date='2024-01-01'; end_date='2024-01-30'; polarization=@('VV','VH'); orbit='ASCENDING'} | ConvertTo-Json; Invoke-RestMethod -Uri 'http://localhost:5000/api/aois/1/export' -Method POST -Body $body -ContentType 'application/json' | ConvertTo-Json -Depth 10
```
Output:
```json
{
    "asset_id": "projects/ee-sergiyk1974/assets/AOI_1_export_20241230_014259",
    "message": "Export task started",
    "parameters": {
        "end_date": "2024-01-30",
        "orbit": "ASCENDING",
        "polarization": [
            "VV",
            "VH"
        ],
        "preset_id": null,
        "start_date": "2024-01-01"
    },
    "status": "success",
    "task_id": "G4IKWZ2NFUYCAZBYXTXQOP7G"
}
```

## Check Export Task Status
```powershell
Invoke-RestMethod -Uri 'http://localhost:5000/api/export/status/G4IKWZ2NFUYCAZBYXTXQOP7G' -Method GET | ConvertTo-Json -Depth 10
```
Output:
```json
{
    "status": "success",
    "task_status": "RUNNING"
}
