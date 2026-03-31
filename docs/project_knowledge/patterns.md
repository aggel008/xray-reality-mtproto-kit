# Patterns

## IP-First Bring-Up

Bring up the replacement server by IP first.

Why:

- fewer moving parts
- faster validation
- no early DNS dependency
- easier staged migration

Only add domain-dependent features after the basic paths work.

## Parallel Migration

Do not shut down the old server before the new one is proven.

Recommended order:

1. create new server
2. test new server
3. issue new client links
4. migrate users gradually
5. shut down the old server later

## Separate Per-User Profiles

Separate profiles are useful when the operator wants:

- selective revocation
- per-user handoff
- clearer auditing

If that is not needed, a shared profile can still work for a very small setup.

## Publish Only Sanitized Artifacts

Never commit:

- real UUIDs
- live panel passwords
- live MTProto secrets
- certs
- private keys

Use placeholders and templates in public repos.
