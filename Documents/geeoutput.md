PS C:\Users\krasn\WindowsProjects\geescan> Invoke-RestMethod -Uri 'http://localhost:5000/api/auth/gee' -Method POST | ConvertTo-Json -Depth 10
{
    "init_count":  1,
    "initialized_at":  "2024-12-30T03:13:22.999084",
    "message":  "Connected to Google Earth Engine successfully",
    "status":  "success"
}
PS C:\Users\krasn\WindowsProjects\geescan> Invoke-RestMethod -Uri 'http://localhost:5000/api/auth/gee/status' -Method GET | ConvertTo-Json -Depth 10
{
    "init_count":  1,
    "initialized":  true,
    "last_init_time":  "2024-12-30T03:13:22.999084",
    "status":  "success"
}
PS C:\Users\krasn\WindowsProjects\geescan> Invoke-RestMethod -Uri 'http://localhost:5000/api/aois' -Method GET | ConvertTo-Json -Depth 10
{
    "aois":  [
                 {
                     "geometry":  "{\"type\":\"Polygon\",\"coordinates\":[[[-74.006,40.7128],[-74.0065,40.7128],[-74.0065,40.7123],[-74.006,40.7123],[-74.006,40.7128]]]}",
                     "id":  1,
                     "name":  "Test AOI"
                 },
                 {
                     "geometry":  "{\"type\":\"Polygon\",\"coordinates\":[[[-74.006,40.7128],[-74.0065,40.7128],[-74.0065,40.7123],[-74.006,40.7123],[-74.006,40.7128]]]}",
                     "id":  2,
                     "name":  "Test AOI"
                 },
                 {
                     "geometry":  "{\"type\":\"Polygon\",\"coordinates\":[[[-74.006,40.7128],[-74.0065,40.7128],[-74.0065,40.7123],[-74.006,40.7123],[-74.006,40.7128]]]}",
                     "id":  3,
                     "name":  "Test AOI"
                 },
                 {
                     "geometry":  "{\"type\":\"Polygon\",\"coordinates\":[[[-74.006,40.7128],[-74.0065,40.7128],[-74.0065,40.7123],[-74.006,40.7123],[-74.006,40.7128]]]}",
                     "id":  4,
                     "name":  "Test AOI"
                 },
                 {
                     "geometry":  "{\"type\":\"Polygon\",\"coordinates\":[[[-74.006,40.7128],[-74.0065,40.7128],[-74.0065,40.7123],[-74.006,40.7123],[-74.006,40.7128]]]}",
                     "id":  5,
                     "name":  "Test AOI"
                 },
                 {
                     "geometry":  "{\"type\":\"Polygon\",\"coordinates\":[[[-74.006,40.7128],[-74.0065,40.7128],[-74.0065,40.7123],[-74.006,40.7123],[-74.006,40.7128]]]}",
                     "id":  6,
                     "name":  "Test AOI"
                 },
                 {
                     "geometry":  "{\"type\":\"Polygon\",\"coordinates\":[[[-74.006,40.7128],[-74.0065,40.7128],[-74.0065,40.7123],[-74.006,40.7123],[-74.006,40.7128]]]}",
                     "id":  7,
                     "name":  "Test AOI"
                 },
                 {
                     "geometry":  "{\"type\":\"Polygon\",\"coordinates\":[[[-74.006,40.7128],[-74.0065,40.7128],[-74.0065,40.7123],[-74.006,40.7123],[-74.006,40.7128]]]}",
                     "id":  8,
                     "name":  "Test AOI"
                 },
                 {
                     "geometry":  "{\"type\":\"Point\",\"coordinates\":[-73.9857,40.758]}",
                     "id":  9,
                     "name":  "PowerShell Created AOI"
                 }
             ],
    "message":  "Successfully fetched AOIs"
}
PS C:\Users\krasn\WindowsProjects\geescan> Invoke-RestMethod -Uri 'http://localhost:5000/api/aois/1' -Method GET | ConvertTo-Json -Depth 10
{
    "aoi":  {
                "geometry":  "{\"type\":\"Polygon\",\"coordinates\":[[[-74.006,40.7128],[-74.0065,40.7128],[-74.0065,40.7123],[-74.006,40.7123],[-74.006,40.7128]]]}",
                "id":  1,
                "name":  "Test AOI"
            },
    "message":  "AOI fetched successfully"
}
PS C:\Users\krasn\WindowsProjects\geescan> $geometry = @{
>>     type = "Polygon"
>>     coordinates = @(
>>         @(
>>             @(-74.0060, 40.7128),
>>             @(-74.0065, 40.7128),
>>             @(-74.0065, 40.7123),
>>             @(-74.0060, 40.7123),
>>             @(-74.0060, 40.7128)
>>         )
>>     )
>> } | ConvertTo-Json
PS C:\Users\krasn\WindowsProjects\geescan> 
PS C:\Users\krasn\WindowsProjects\geescan> $body = @{
>>     name = "New AOI"
>>     geometry = $geometry
>> } | ConvertTo-Json
PS C:\Users\krasn\WindowsProjects\geescan> 
PS C:\Users\krasn\WindowsProjects\geescan> Invoke-RestMethod -Uri 'http://localhost:5000/api/aois' -Method POST -Body $body -ContentType 'application/json' | ConvertTo-Json -Depth 10
{
    "id":  null,
    "message":  "AOI created"
}
PS C:\Users\krasn\WindowsProjects\geescan> $body = @{
>>     start_date = '2024-01-01'
>>     end_date = '2024-01-30'
>>     polarization = @('VV','VH')
>>     orbit = 'ASCENDING'
>> } | ConvertTo-Json
PS C:\Users\krasn\WindowsProjects\geescan> 
PS C:\Users\krasn\WindowsProjects\geescan> Invoke-RestMethod -Uri 'http://localhost:5000/api/aois/1/export' -Method POST -Body $body -ContentType 'application/json' | ConvertTo-Json -Depth 10
{
    "asset_id":  "projects/ee-sergiyk1974/assets/AOI_1_export_20241230_031447",
    "message":  "Export task started",
    "parameters":  {
                       "end_date":  "2024-01-30",
                       "orbit":  "ASCENDING",
                       "polarization":  [
                                            "VV",
                                            "VH"
                                        ],
                       "preset_id":  null,
                       "start_date":  "2024-01-01"
                   },
    "status":  "success",
    "task_id":  "W5AR5XCRKI5SKTTDKWFWG7YF"
}
PS C:\Users\krasn\WindowsProjects\geescan> Invoke-RestMethod -Uri 'http://localhost:5000/api/export/status/G4IKWZ2NFUYCAZBYXTXQOP7G'
 -Method GET | ConvertTo-Json -Depth 10
{
    "status":  "success",
    "task_status":  "COMPLETED"
}
PS C:\Users\krasn\WindowsProjects\geescan> Invoke-RestMethod -Uri 'http://localhost:5000/api/aois/1' -Method DELETE | ConvertTo-Json
 -Depth 10
{
    "message":  "AOI deleted"
}