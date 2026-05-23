# Content Engine API

## Purpose

Expose EchoMedia Content Engine workflows through an API that can be used by UI clients and Christina.

## Primary Consumers

- Web UI
- Christina employee assistant
- automation agents
- future creator dashboards

## Initial API Capabilities

- create project intake
- validate canon
- audit continuity
- build chapter packet
- assemble screenplay
- build export package
- create release manifest
- query project status

## Planned Routes

```text
GET  /health
POST /projects/intake
POST /projects/{project}/validate-canon
POST /projects/{project}/audit-continuity
POST /projects/{project}/build-chapter-packet
POST /projects/{project}/assemble-screenplay
POST /projects/{project}/build-export-package
POST /projects/{project}/create-release
GET  /projects/{project}/status
```

## Christina Integration

Christina should call this API directly using role-scoped service credentials.

Christina should be able to:

- create story projects
- request canon validation
- run continuity audits
- build chapter packets
- generate screenplay exports
- package releases
- summarize current project status

## Future Expansion

- authentication and RBAC
- audit logs
- job queue
- async task status
- file upload support
- integration with EchoMedia dashboard
