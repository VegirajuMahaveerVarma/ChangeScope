# Security Policy

## Scope

ChangeScope is experimental and currently analyzes repository source statically. It is not a sandbox and should not be treated as a security scanner.

## Reporting a vulnerability

Please report suspected vulnerabilities privately to the repository maintainer through GitHub's security reporting feature if it is enabled. If private reporting is unavailable, open an issue with minimal non-sensitive details and ask for a private contact method. Do not publish credentials, private source code, or exploit details in a public issue.

## Current safety boundaries

- ChangeScope does not intentionally execute analyzed project code.
- Git commands are invoked as argument arrays rather than through a shell.
- Analysis is read-only with respect to the analyzed repository.
- Repository files are untrusted input; extremely large files are skipped.
- Static analysis can be incomplete and should not be relied on as the only review or test mechanism.
