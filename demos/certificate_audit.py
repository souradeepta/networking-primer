#!/usr/bin/env python3
"""Print metadata from a public PEM certificate without exposing a key."""

from pathlib import Path
import ssl
import sys


def main() -> None:
    """Audit one certificate file using Python's standard library."""
    if len(sys.argv) != 2:
        raise SystemExit("Usage: certificate_audit.py public-certificate.pem")
    path = Path(sys.argv[1])
    if not path.is_file():
        raise SystemExit(f"Certificate file not found: {path}")
    try:
        certificate = ssl._ssl._test_decode_cert(str(path))
    except (ssl.SSLError, OSError) as error:
        raise SystemExit(f"Unable to decode a public PEM certificate: {error}") from error
    print(f"Subject: {certificate.get('subject')}")
    print(f"Issuer: {certificate.get('issuer')}")
    print(f"Not before: {certificate.get('notBefore')}")
    print(f"Not after: {certificate.get('notAfter')}")
    print(f"SubjectAltName: {certificate.get('subjectAltName', ())}")


if __name__ == "__main__":
    main()
