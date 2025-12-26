# バッチ実行関数
function Invoke-Batch {
    param (
        [string]$project
    )
    
    Set-Location -Path $PSScriptRoot
    Write-Host "$project Start"

    docker run -it --rm `
        -v "$(PWD)/inifile:/app/inifile" `
        -v "$(PWD)/output:/app/output" `
        -v "$(PWD)/holiday:/app/holiday" `
        -v "$(PWD)/custom:/app/custom" `
        redmine_export redmine_export $project

    Write-Host "$project Completed"
}
function Invoke-Setup-Batch {
    Set-Location -Path $PSScriptRoot
    Write-Host "redmine_export_setup Start"

    docker run -it --rm `
        -v "$(PWD)/inifile:/app/inifile" `
        -v "$(PWD)/holiday:/app/holiday" `
        -v "$(PWD)/custom:/app/custom" `
        redmine_export redmine_export_setup

    Write-Host "redmine_export_setup Completed"
}

# 初回のみ実行する
# # redmine_export_setupの実行
# Invoke-Setup-Batch

# # redmine_exportの実行
# Invoke-Batch -project "project_name"