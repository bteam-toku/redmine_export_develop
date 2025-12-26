.\env.ps1

# バッチ実行関数
function Invoke-Batch {
    param (
        [string]$project
    )
    
    Set-Location -Path $PSScriptRoot
    Write-Host "$project Start"
    py -m redmine_export $project
    Write-Host "$project Completed"
}
function Invoke-Setup-Batch {
    Set-Location -Path $PSScriptRoot
    Write-Host "redmine_export_setup Start"
    py -m redmine_export_setup
    Write-Host "redmine_export_setup Completed"
}

# 初回のみ実行する
# # redmine_export_setupの実行
# Invoke-Setup-Batch

# # redmine_exportの実行
# Invoke-Batch -project "project_name"
