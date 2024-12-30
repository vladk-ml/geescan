# GEEScan API Testing Commands

## Test GEE Authentication
```powershell
Invoke-RestMethod -Uri 'http://localhost:5000/api/test' -Method GET | ConvertTo-Json -Depth 10
```

## List All AOIs
```powershell
Invoke-RestMethod -Uri 'http://localhost:5000/api/aois' -Method GET | ConvertTo-Json -Depth 10
```

## Export AOI to Earth Engine Asset
```powershell
$body = @{start_date='2024-01-01'; end_date='2024-01-30'; polarization=@('VV','VH'); orbit='ASCENDING'} | ConvertTo-Json; Invoke-RestMethod -Uri 'http://localhost:5000/api/aois/1/export' -Method POST -Body $body -ContentType 'application/json' | ConvertTo-Json -Depth 10
```

## Check Export Task Status
```powershell
Invoke-RestMethod -Uri 'http://localhost:5000/api/export/status/G4IKWZ2NFUYCAZBYXTXQOP7G' -Method GET | ConvertTo-Json -Depth 10
