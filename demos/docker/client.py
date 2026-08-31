"""Local-only HTTP client for the Compose networking lab."""

from urllib.request import urlopen


with urlopen("http://server:8080/health", timeout=3) as response:
    print(f"url=http://server:8080/health status={response.status} body={response.read().decode().strip()}")
