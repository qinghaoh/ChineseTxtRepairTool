<#
.SYNOPSIS

Call GBK Decoder to txt files recursively in the specified path.

.PARAMETER Path

Specifies a path to one or more locations. Wildcards are accepted. The default location is the current directory (.).

.PARAMETER Confirm

Prompts you for confirmation before running the cmdlet.

.EXAMPLE

PS> Decode-Files -Path "D:\docs"

.EXAMPLE

PS> Decode-Files -Path "D:\docs" -Confirm
#>

[CmdletBinding()]
Param(
    [string[]]
    $Path,
    [switch]
    $Recurse,
    [switch]
    $Confirm
)

Begin {
    $GbkDecoder = "D:\gbk_decoder\gbk_decoder.exe"
    $Mark = "__GBK_DECODED__"
}

Process {
    Get-ChildItem -Path $Path -File -Recurse:$Recurse -Filter "*.txt" | ForEach-Object -Process {
        & $GbkDecoder --infile $_.FullName --outfile "$($_.FullName.Trim()).$Mark.txt"
    }

    Get-ChildItem -Path $Path -File -Recurse:$Recurse -Filter "*.txt" | ForEach-Object -Process {
        if (Test-Path -LiteralPath "$($_.FullName.Trim()).$Mark.txt" -PathType leaf) {
            Remove-Item -LiteralPath $_.FullName -Confirm:$Confirm

            Rename-Item -LiteralPath "$($_.FullName.Trim()).$Mark.txt" -NewName $_

            Write-Host Processed $_
        }
    }
}



