# Privacy Audit: Global Network Artifact Scan (`agent_15`)

## Scope
- Repository-wide scan from: `/Users/cesar514/Documents/agent_programming/cosimi-idai-test`
- Objective: identify internal URLs, localhost/private IPs, internal hostnames, and accidental service endpoints.

## Method
Regex-based searches were run across tracked text files for:
- Local/internal hosts: `localhost`, `127.0.0.1`, `0.0.0.0`, `host.docker.internal`
- Private IPv4 ranges: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`
- Internal DNS patterns: `.internal`, `.local`, `.corp`, `.intra`, `.private`, Kubernetes `.svc(.cluster.local)`
- Service URI schemes: `redis://`, `postgres://`, `mongodb://`, `amqp://`, `kafka://`, `grpc://`, `ws://`, `wss://`, `ftp://`, `sftp://`
- Plain HTTP endpoint literals (`http://`) for potential insecure service usage.

## Findings

### 1) No internal/private network endpoints found (High confidence)
No matches were found for:
- localhost/loopback bindings
- RFC1918 private IP literals
- internal/private DNS suffixes
- Kubernetes service hostnames
- non-HTTP service connection URIs

Assessment:
- No accidental leak of internal service topology was identified in this scan.

### 2) Low: plaintext external API endpoint in skill script
A hardcoded external API endpoint uses HTTP (not HTTPS):
- `skills/literature-review/scripts/fetch_arxiv.py:16`
  - `ARXIV_API = "http://export.arxiv.org/api/query"`

Risk:
- Traffic to this endpoint may be vulnerable to interception/tampering on untrusted networks.
- This is not an internal endpoint leak, but it is a network hygiene issue.

Recommendation:
1. Verify whether HTTPS is supported by this endpoint.
2. If supported, migrate to HTTPS and keep strict URL validation.

## Contextual Notes
- The repository contains many public internet URLs in docs, lockfiles, and citation artifacts; these are expected and are not internal endpoint disclosures.
- XML namespace URIs (for example `http://schemas.openxmlformats.org/...`) were observed and treated as standards metadata, not service endpoints.

## Conclusion
- Internal/private endpoint exposure: **none detected**.
- Actionable network endpoint issue: **1 low-severity plaintext external API URL**.
