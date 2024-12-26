# API Testing Guide

## 1. Health Check
**Endpoint**: `/api/health` (GET)

```powershell
Write-Host "--- Testing /api/health (GET) ---"
$uri = "http://localhost:5000/api/health"
try {
    $response = Invoke-WebRequest -Uri $uri -Method Get
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Content: $($response.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
Write-Host ""
```

## 2. Test Create AOI
**Endpoint**: `/api/test_create_aoi` (POST)

```powershell
Write-Host "--- Testing /api/test_create_aoi (POST) ---"
$uri = "http://localhost:5000/api/test_create_aoi"
try {
    $response = Invoke-WebRequest -Uri $uri -Method Post
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Content: $($response.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
Write-Host ""
```

## 3. Test Get AOIs
**Endpoint**: `/api/test_aois` (GET)

```powershell
Write-Host "--- Testing /api/test_aois (GET) ---"
$uri = "http://localhost:5000/api/test_aois"
try {
    $response = Invoke-WebRequest -Uri $uri -Method Get
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Content: $($response.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
Write-Host ""
```

## 4. Get All AOIs
**Endpoint**: `/api/aois` (GET)

```powershell
Write-Host "--- Testing /api/aois (GET) ---"
$uri = "http://localhost:5000/api/aois"
try {
    $response = Invoke-WebRequest -Uri $uri -Method Get
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Content: $($response.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
Write-Host ""
```

## 5. Create New AOI
**Endpoint**: `/api/aois` (POST)

```powershell
Write-Host "--- Testing /api/aois (POST) ---"
$uri = "http://localhost:5000/api/aois"
$body = ConvertTo-Json -Compress @{
    name = "PowerShell Created AOI"
    geometry = "SRID=4326;POINT(-73.9857 40.7580)"
}
try {
    $response = Invoke-WebRequest -Uri $uri -Method Post -Body $body -ContentType "application/json"
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Content: $($response.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
Write-Host ""
```

## 6. Update Existing AOI
**Endpoint**: `/api/aois/{id}` (PUT)

Note: Replace `{id}` with the actual AOI ID you want to update.

```powershell
Write-Host "--- Testing /api/aois/1 (PUT) ---"
$uri = "http://localhost:5000/api/aois/1"  # Replace 1 with an actual AOI ID
$body = ConvertTo-Json -Compress @{
    name = "PowerShell Updated AOI"
    geometry = "SRID=4326;POINT(-73.9712 40.7834)"
}
try {
    $response = Invoke-WebRequest -Uri $uri -Method Put -Body $body -ContentType "application/json"
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Content: $($response.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
Write-Host ""
```

## 7. Delete Existing AOI
**Endpoint**: `/api/aois/{id}` (DELETE)

Note: Replace `{id}` with the actual AOI ID you want to delete.

```powershell
Write-Host "--- Testing /api/aois/1 (DELETE) ---"
$uri = "http://localhost:5000/api/aois/1"  # Replace 1 with an actual AOI ID
try {
    $response = Invoke-WebRequest -Uri $uri -Method Delete
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Content: $($response.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
Write-Host ""
```

## 8. Get Single AOI
**Endpoint**: `/api/aois/{id}` (GET)

Note: Replace `{id}` with the actual AOI ID you want to retrieve.

```powershell
Write-Host "--- Testing /api/aois/1 (GET) ---"
$uri = "http://localhost:5000/api/aois/1"  # Replace 1 with an actual AOI ID
try {
    $response = Invoke-WebRequest -Uri $uri -Method Get
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Content: $($response.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
Write-Host ""

Explanation of Each Test:

/api/health (GET):

Sends a GET request to the health check endpoint.

Expects a status code of 200 and a JSON response like {"status": "healthy"}.

/api/test_create_aoi (POST):

Sends a POST request to trigger the creation of a test AOI on the backend.

Expects a status code of 201 and a JSON response confirming creation, including the new AOI's ID.

/api/test_aois (GET):

Sends a GET request to retrieve all AOIs for testing purposes.

Expects a status code of 200 and a JSON response containing a list of AOI objects.

/api/aois (GET):

Sends a GET request to retrieve all AOIs.

Expects a status code of 200 and a JSON response containing a list of AOI objects.

/api/aois (POST):

Sends a POST request to create a new AOI.

Includes a JSON body with the name and geometry for the new AOI.

Expects a status code of 201 and a JSON response confirming creation, including the new AOI's ID.

/api/aois/{aoi_id} (PUT):

Sends a PUT request to update an existing AOI.

Important: You need to replace 1 in the $uri with an actual ID of an AOI in your database.

Includes a JSON body with the updated name and geometry.

Expects a status code of 200 indicating successful update.

/api/aois/{aoi_id} (DELETE):

Sends a DELETE request to delete an existing AOI.

Important: You need to replace 1 in the $uri with an actual ID of an AOI in your database.

Expects a status code of 200 indicating successful deletion.

/api/aois/{aoi_id} (GET):

Sends a GET request to retrieve a specific AOI.

Important: You need to replace 1 in the $uri with an actual ID of an AOI in your database.

Expects a status code of 200 and a JSON response containing the details of the requested AOI, or a 404 if the AOI is not found.