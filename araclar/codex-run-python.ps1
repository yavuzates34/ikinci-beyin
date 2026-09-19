param(
    [Parameter(Mandatory = $true)]
    [string]$Script,

    [ValidateSet("", "claude", "codex")]
    [string]$Format = ""
)

$ErrorActionPreference = "Stop"

$candidates = @(
    @{ Command = "python.exe"; Prefix = @() },
    @{ Command = "py.exe"; Prefix = @("-3") },
    @{ Command = "C:\Program Files\LibreOffice\program\python.exe"; Prefix = @() }
)

$selected = $null
foreach ($candidate in $candidates) {
    $resolved = Get-Command $candidate.Command -ErrorAction SilentlyContinue
    if (-not $resolved) {
        continue
    }

    $oldErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "SilentlyContinue"
    & $resolved.Source @($candidate.Prefix) --version *> $null
    $probeExitCode = $LASTEXITCODE
    $ErrorActionPreference = $oldErrorActionPreference
    if ($probeExitCode -eq 0) {
        $selected = @{ Path = $resolved.Source; Prefix = $candidate.Prefix }
        break
    }
}

if (-not $selected) {
    [Console]::Error.WriteLine("Codex hook: kullanilabilir Python 3 bulunamadi.")
    exit 1
}

$scriptArguments = @()
if ($Format) {
    $scriptArguments = @("--bicim", $Format)
}

& $selected.Path @($selected.Prefix) $Script @scriptArguments
exit $LASTEXITCODE
