# GEEScan API Commands

## 1. Initialize GEE Authentication
```powershell
Invoke-RestMethod -Uri 'http://localhost:5000/api/auth/gee' -Method POST | ConvertTo-Json -Depth 10
```

## 2. Check Authentication Status
```powershell
Invoke-RestMethod -Uri 'http://localhost:5000/api/auth/gee/status' -Method GET | ConvertTo-Json -Depth 10
```

## 3. List All AOIs
```powershell
Invoke-RestMethod -Uri 'http://localhost:5000/api/aois' -Method GET | ConvertTo-Json -Depth 10
```

## 4. Get Single AOI (replace {id} with actual AOI ID)
```powershell
Invoke-RestMethod -Uri 'http://localhost:5000/api/aois/1' -Method GET | ConvertTo-Json -Depth 10
```

## 5. Create New AOI
```powershell
$geometry = @{
    type = "Polygon"
    coordinates = @(
        @(
            @(-74.0060, 40.7128),
            @(-74.0065, 40.7128),
            @(-74.0065, 40.7123),
            @(-74.0060, 40.7123),
            @(-74.0060, 40.7128)
        )
    )
} | ConvertTo-Json

$body = @{
    name = "New AOI"
    geometry = $geometry
} | ConvertTo-Json

Invoke-RestMethod -Uri 'http://localhost:5000/api/aois' -Method POST -Body $body -ContentType 'application/json' | ConvertTo-Json -Depth 10
```

## 6. Export AOI to Earth Engine Asset
```powershell
$body = @{
    start_date = '2024-01-01'
    end_date = '2024-01-30'
    polarization = @('VV','VH')
    orbit = 'ASCENDING'
} | ConvertTo-Json

Invoke-RestMethod -Uri 'http://localhost:5000/api/aois/1/export' -Method POST -Body $body -ContentType 'application/json' | ConvertTo-Json -Depth 10
```

## 7. Check Export Task Status (replace {task_id} with actual task ID)
```powershell
Invoke-RestMethod -Uri 'http://localhost:5000/api/export/status/G4IKWZ2NFUYCAZBYXTXQOP7G' -Method GET | ConvertTo-Json -Depth 10
```

## 8. Delete AOI (replace {id} with actual AOI ID)
```powershell
Invoke-RestMethod -Uri 'http://localhost:5000/api/aois/1' -Method DELETE | ConvertTo-Json -Depth 10
```

## Testing Order:
1. Start with authentication (1-2)
2. List existing AOIs (3)
3. Try creating a new AOI (5)
4. Verify the new AOI exists (3 or 4)
5. Start an export (6)
6. Check export status (7)
7. Clean up by deleting test AOIs if needed (8)
