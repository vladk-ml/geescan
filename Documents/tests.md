# API Testing Guide

## 1. Health Check
Endpoint: `/health` (GET)

```powershell
$uri = "http://localhost:5000/health"

try {
    $response = Invoke-WebRequest -Uri $uri -Method Get
    Write-Host "Health Check Response:"
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Content: $($response.Content)"
} catch {
    Write-Host "Error:"
    Write-Host $_.Exception.Message
}
```

## 2. Test Create AOI
Endpoint: `/test_create_aoi` (POST)

Note: This endpoint doesn't require sending data in the request body as it creates a predefined test AOI.

```powershell
$uri = "http://localhost:5000/test_create_aoi"

try {
    $response = Invoke-WebRequest -Uri $uri -Method Post
    Write-Host "Test Create AOI Response:"
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Content: $($response.Content)"
} catch {
    Write-Host "Error:"
    Write-Host $_.Exception.Message
}
```

## 3. Test Get AOIs
Endpoint: `/test_aois` (GET)

```powershell
$uri = "http://localhost:5000/test_aois"

try {
    $response = Invoke-WebRequest -Uri $uri -Method Get
    Write-Host "Test Get AOIs Response:"
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Content: $($response.Content | ConvertFrom-Json | ConvertTo-String)"
} catch {
    Write-Host "Error:"
    Write-Host $_.Exception.Message
}
```

## 4. Get All AOIs
Endpoint: `/aois` (GET)

```powershell
$uri = "http://localhost:5000/aois"

try {
    $response = Invoke-WebRequest -Uri $uri -Method Get
    Write-Host "Get All AOIs Response:"
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Content: $($response.Content | ConvertFrom-Json | ConvertTo-String)"
} catch {
    Write-Host "Error:"
    Write-Host $_.Exception.Message
}
```

## 5. Create New AOI
Endpoint: `/aois` (POST)

```powershell
$uri = "http://localhost:5000/aois"

$aoiData = @{
    "name" = "AOI Created from PowerShell"
    "geometry" = "SRID=4326;POLYGON((-74.0050 40.7138, -74.0055 40.7138, -74.0055 40.7133, -74.0050 40.7133, -74.0050 40.7138))"
}

$headers = @{
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-WebRequest -Uri $uri -Method Post -Headers $headers -Body ($aoiData | ConvertTo-Json)
    Write-Host "Create New AOI Response:"
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Content: $($response.Content)"
} catch {
    Write-Host "Error:"
    Write-Host $_.Exception.Message
}
```

## 6. Update Existing AOI
Endpoint: `/aois/<aoi_id>` (PUT)

Note: Replace `<aoi_id>` with the actual ID of the AOI you want to update.

```powershell
$aoi_id = 1  # Replace with the actual AOI ID
$uri = "http://localhost:5000/aois/$aoi_id"

$aoiData = @{
    "name" = "Updated AOI Name from PowerShell"
    "geometry" = "SRID=4326;POLYGON((-74.0040 40.7148, -74.0045 40.7148, -74.0045 40.7143, -74.0040 40.7143, -74.0040 40.7148))"
}

$headers = @{
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-WebRequest -Uri $uri -Method Put -Headers $headers -Body ($aoiData | ConvertTo-Json)
    Write-Host "Update AOI Response:"
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Content: $($response.Content)"
} catch {
    Write-Host "Error:"
    Write-Host $_.Exception.Message
}
```

## 7. Delete Existing AOI
Endpoint: `/aois/<aoi_id>` (DELETE)

Note: Replace `<aoi_id>` with the actual ID of the AOI you want to delete.

```powershell
$aoi_id = 1 # Replace with the actual AOI ID
$uri = "http://localhost:5000/aois/$aoi_id"

try {
    $response = Invoke-WebRequest -Uri $uri -Method Delete
    Write-Host "Delete AOI Response:"
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Content: $($response.Content)"
} catch {
    Write-Host "Error:"
    Write-Host $_.Exception.Message
}
```

## 8. Get Single AOI
Endpoint: `/aois/<aoi_id>` (GET)

Note: Replace `<aoi_id>` with the actual ID of the AOI you want to retrieve.

```powershell
$aoi_id = 1 # Replace with the actual AOI ID
$uri = "http://localhost:5000/aois/$aoi_id"

try {
    $response = Invoke-WebRequest -Uri $uri -Method Get
    Write-Host "Get Single AOI Response:"
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Content: $($response.Content | ConvertFrom-Json | ConvertTo-String)"
} catch {
    Write-Host "Error:"
    Write-Host $_.Exception.Message
}