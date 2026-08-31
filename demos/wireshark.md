# Wireshark and tshark workflow

Packet captures are powerful evidence and a data-handling risk. Capture only a
local lab interface or an explicitly approved production slice, set a short
duration, protect the file, and redact before sharing. Do not capture private
keys, bearer tokens, cookies, or unrelated users.

## Local Docker lab

1. Start the Compose server/client lab in [docker](docker/README.md).
2. Identify the bridge with `docker network ls` and `docker network inspect`.
3. Capture only the lab interface and port for a short window:

```bash
tshark -i <approved-lab-interface> -f 'tcp port 8080' -a duration:10 -w /tmp/networking-primer.pcapng
```

4. Open the file in Wireshark and inspect the TCP SYN/SYN-ACK/ACK, HTTP
   request/response, and retransmissions. Use display filters such as
   `tcp.port == 8080` and `http`.
5. Remove the capture using the approved temporary-file cleanup process after
   extracting only the evidence needed for the exercise.

The packet view proves what was observed on that interface; it does not prove
that a packet was never dropped elsewhere. Correlate with endpoint, proxy, and
application logs.
