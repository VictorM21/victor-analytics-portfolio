param(
    [ValidateSet('up', 'down', 'build', 'logs')]
    [string]$Command = 'up'
)

switch ($Command) {
    'up' {
        docker compose up -d
        Write-Host "API running at http://localhost:8000"
    }
    'down' {
        docker compose down
    }
    'build' {
        docker compose build --no-cache
    }
    'logs' {
        docker compose logs -f
    }
}