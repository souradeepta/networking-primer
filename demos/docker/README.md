# Reproducible local Docker lab

This optional lab starts a tiny HTTP server and client on an isolated Compose
network. It demonstrates service naming, TCP connection setup, HTTP evidence,
and a packet-capture point without contacting external services.

Prerequisite: Docker Engine and Compose. From this directory:

```bash
docker compose up --build --abort-on-container-exit
docker compose down
```

Expected client output includes `http://server:8080/health` and `status=200`.
For an owned local capture, start `tshark` on the Docker bridge before `up`; do
not capture shared or production interfaces.
