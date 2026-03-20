$pat = "sakshi programmer/123"
$username = "sakshiyadav4980-programmer"
$repo = "svm-deployment"

$headers = @{
    "Authorization" = "Bearer $pat"
    "Accept" = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
    "User-Agent" = "PowerShell-Deployment-Script"
}

Write-Host "Creating repository $repo..."
$bodyRepo = @{
    name = $repo
    private = $false
} | ConvertTo-Json

try {
    Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $bodyRepo -ContentType "application/json" | Out-Null
    Write-Host "Repository created successfully."
} catch {
    $err = $_.ErrorDetails.Message
    if (-not [string]::IsNullOrEmpty($err) -and $err -match "name already exists") {
        Write-Host "Repository already exists, continuing to file upload."
    } else {
        Write-Host "Error creating repository: $_"
        if ($err) { Write-Host "Details: $err" }
    }
}

$files = @("app.py", "Position_Salaries.csv", "support_vector_machine.ipynb", "requirements.txt")

foreach ($file in $files) {
    Write-Host "Uploading $file..."
    $content = [System.IO.File]::ReadAllBytes(".\$file")
    $base64 = [System.Convert]::ToBase64String($content)
    
    # Check if file already exists to get its SHA (needed for update)
    $fileUrl = "https://api.github.com/repos/$username/$repo/contents/$file"
    $sha = $null
    try {
        $existing = Invoke-RestMethod -Uri $fileUrl -Method Get -Headers $headers
        $sha = $existing.sha
    } catch {
        # File doesn't exist, ignore
    }

    $bodyFile = @{
        message = "Add $file"
        content = $base64
    }
    if ($sha) {
        $bodyFile.sha = $sha
        $bodyFile.message = "Update $file"
    }

    # Convert to JSON and handle large payloads by preventing depth truncation
    $bodyFileJson = ConvertTo-Json -InputObject $bodyFile -Depth 10

    try {
        Invoke-RestMethod -Uri $fileUrl -Method Put -Headers $headers -Body $bodyFileJson -ContentType "application/json" | Out-Null
        Write-Host "Successfully uploaded $($file)"
    } catch {
        Write-Host "Failed to upload $($file): $_"
        if ($_.ErrorDetails) { Write-Host $_.ErrorDetails.Message }
    }
}

Write-Host "Deployment completed. View repository at: https://github.com/$username/$repo"
