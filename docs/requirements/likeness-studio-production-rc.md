# EchoMedia Likeness Studio - Production RC Requirements

Status: Production Release Candidate requirements
Target repo: EchoMedia-ContentEngine
Initial likeness projects: Shannon, Vanessa
Operating mode: consent-first, provenance-preserving, human-reviewed authorized likeness generation

> Terminology note: externally and in code, use **authorized likeness**, **synthetic likeness**, **reference-guided generation**, and **digital likeness project**. Avoid framing the product as a deceptive clone/deepfake system. The system must not bypass model/provider safety systems. False-positive mitigation must rely on consent metadata, prompt normalization, provenance, and human review.

---

## 1. Release Candidate Goal

Build a production-ready likeness project manager for EchoMedia that can organize reference images and generated images for Shannon, Vanessa, and future authorized likeness projects.

The RC must provide:

- Project folder creation per person or likeness project.
- Consent-gated reference image intake.
- Reference approval workflow.
- Prompt templates and generation profiles.
- API abstraction for image generation providers.
- Safe handling of provider false positives.
- Human review before approval or publishing.
- Audit logs and provenance records.
- Production deployment readiness.

---

## 2. Non-Negotiable Safety and Legal Requirements

### 2.1 Consent Gate

Generation is blocked unless a valid consent record exists and is marked approved.

Each likeness project must include:

```json
{
  "subject_name": "Vanessa",
  "project_slug": "Vanessa",
  "consent_status": "approved",
  "consent_type": "written",
  "allowed_use": ["private", "social_media", "marketing", "training_reference"],
  "restricted_use": [
    "deceptive_impersonation",
    "political_endorsement_without_approval",
    "medical_claims",
    "financial_claims",
    "legal_claims",
    "explicit_sexual_content",
    "minor_sensitive_content",
    "third_party_likeness_without_consent"
  ],
  "date_signed": "YYYY-MM-DD",
  "expires_on": null,
  "signed_by": "Subject Name",
  "verified_by": "Shannon Bray",
  "source_document_path": "consent/signed-consent.pdf",
  "revoked_at": null
}
```

Acceptance criteria:

- Missing consent blocks project generation.
- Expired consent blocks project generation.
- Revoked consent blocks project generation.
- Intended use outside allowed_use blocks generation.
- Restricted use blocks generation.
- Every blocked generation creates a moderation/audit event.

### 2.2 No Deceptive Impersonation

The system must not generate content that implies a subject said, did, attended, endorsed, or experienced something unless the use case is explicitly approved.

Public-facing outputs must support disclosure metadata:

```text
AI-generated authorized likeness image.
Synthetic image based on authorized references.
AI-assisted promotional image.
```

### 2.3 No Safety-System Bypass

The product may mitigate false-positive provider errors, but must not bypass provider policies.

Allowed:

- Add consent metadata to provider request.
- Clarify synthetic/authorized use.
- Normalize risky or ambiguous wording.
- Reduce deceptive realism language.
- Switch to safer stylized/editorial variants.
- Stop and require human review.

Disallowed:

- Hiding identity context to avoid moderation.
- Retrying prohibited content with evasive wording.
- Routing blocked content to weaker providers solely to bypass safety systems.
- Removing provenance or disclosure markers.
- Creating deceptive political, legal, financial, medical, or sexual content.

---

## 3. Required Repository Structure

Create or support this structure:

```text
echomedia-content-engine/
├── docs/
│   └── requirements/
│       └── likeness-studio-production-rc.md
├── config/
│   ├── providers.json
│   ├── safety-rules.json
│   ├── project-types.json
│   └── storage.json
├── projects/
│   ├── _template/
│   │   ├── consent/
│   │   ├── references/approved/
│   │   ├── references/pending/
│   │   ├── references/rejected/
│   │   ├── prompts/
│   │   ├── outputs/draft/
│   │   ├── outputs/approved/
│   │   ├── outputs/rejected/
│   │   ├── outputs/published/
│   │   ├── metadata/
│   │   └── models/
│   │       ├── embeddings/
│   │       ├── lora/
│   │       └── checkpoints/
│   ├── Shannon/
│   └── Vanessa/
├── src/
│   ├── api/
│   ├── auth/
│   ├── consent/
│   ├── generation/
│   ├── moderation/
│   ├── provenance/
│   ├── review/
│   ├── storage/
│   └── workers/
├── tools/
│   ├── create-project.ps1
│   ├── import-references.ps1
│   ├── audit-project.ps1
│   └── export-approved.ps1
└── tests/
    ├── consent/
    ├── generation/
    ├── moderation/
    ├── storage/
    └── review/
```

PowerShell scripts must target PowerShell 7+ only.

---

## 4. Initial Project Folders

The RC must create these initial projects:

```text
projects/Shannon/
projects/Vanessa/
```

Each must include:

```text
consent/
references/approved/
references/pending/
references/rejected/
prompts/
outputs/draft/
outputs/approved/
outputs/rejected/
outputs/published/
metadata/
models/embeddings/
models/lora/
models/checkpoints/
```

Each folder should include a `.gitkeep` unless another file exists.

---

## 5. Project Creation Requirements

### 5.1 CLI

Add:

```powershell
pwsh ./tools/create-project.ps1 -ProjectName "Vanessa"
```

Optional parameters:

```powershell
-DisplayName
-SubjectName
-ProjectType authorized_likeness
-InitializeConsentTemplate
-Force
```

### 5.2 API

```http
POST /api/likeness/projects
```

Request:

```json
{
  "project_name": "Vanessa",
  "display_name": "Vanessa",
  "subject_name": "Vanessa",
  "project_type": "authorized_likeness"
}
```

Acceptance criteria:

- Project names are sanitized.
- Duplicate project names are rejected unless force mode is explicit.
- Project starts with consent_status = missing.
- Generation is disabled until consent approval.

---

## 6. Reference Image Intake Requirements

### 6.1 Upload / Import

All incoming references first land in:

```text
projects/{ProjectName}/references/pending/
```

Metadata must be written to:

```text
projects/{ProjectName}/metadata/image-index.json
```

Reference metadata schema:

```json
{
  "image_id": "uuid",
  "project": "Vanessa",
  "original_filename": "IMG_1234.jpeg",
  "storage_path": "projects/Vanessa/references/pending/IMG_1234.jpeg",
  "sha256": "hash",
  "uploaded_at": "timestamp",
  "source": "user_upload",
  "rights_status": "pending_review",
  "face_detected": true,
  "third_party_faces_detected": false,
  "quality_score": 0.91,
  "approved_for_training": false,
  "approved_for_generation_reference": false,
  "review_state": "pending",
  "notes": ""
}
```

### 6.2 Approval States

Supported states:

```text
pending
approved
rejected
archived
```

Approval requires:

- Consent exists.
- Subject identity confirmed.
- Quality is acceptable.
- No unauthorized third-party faces.
- No minor-sensitive content.
- No conflicting rights issue.

---

## 7. Prompt and Profile Requirements

Each project must support reusable prompt assets:

```text
prompts/base-style.md
prompts/wardrobe.md
prompts/poses.md
prompts/negative-prompts.md
prompts/disclosure.md
prompts/provider-notes.md
```

Prompt profiles should include:

```json
{
  "profile_id": "coastal-editorial",
  "display_name": "Coastal Editorial",
  "allowed_projects": ["Vanessa"],
  "intended_use": ["private", "social_media"],
  "default_aspect_ratio": "4:5",
  "public_disclosure_required": true,
  "negative_prompt": "deformed hands, distorted face, extra limbs, third-party faces, text artifacts"
}
```

---

## 8. Generation Pipeline Requirements

### 8.1 Generation Request

```json
{
  "project": "Vanessa",
  "prompt": "Create a relaxed coastal editorial portrait using authorized references.",
  "style_profile": "coastal-editorial",
  "reference_image_ids": ["uuid1", "uuid2"],
  "output_count": 4,
  "aspect_ratio": "4:5",
  "safety_mode": "standard",
  "public_disclosure_required": true,
  "intended_use": "social_media",
  "requested_by": "ShannonBrayNC"
}
```

### 8.2 Preflight Validator

Before generation, the validator must check:

- Project exists.
- Consent is approved.
- Intended use is allowed.
- References are approved.
- Prompt does not request deceptive impersonation.
- Prompt does not request restricted content.
- Prompt does not include unauthorized third parties.
- Output count and aspect ratio are valid.
- Provider supports requested capabilities.

Failed preflight blocks provider calls.

### 8.3 Output Location

All generated images must land in:

```text
projects/{ProjectName}/outputs/draft/
```

No automatic move to approved or published.

---

## 9. Provider API Abstraction Requirements

Implement a provider interface.

TypeScript example:

```ts
export interface ImageGenerationProvider {
  name: string;
  generate(request: GenerationRequest): Promise<GenerationResult>;
  supportsReferenceImages(): boolean;
  supportsMultipleReferences(): boolean;
  supportsSafetyMetadata(): boolean;
}
```

Python example:

```python
class ImageGenerationProvider(Protocol):
    name: str

    def generate(self, request: GenerationRequest) -> GenerationResult:
        ...

    def supports_reference_images(self) -> bool:
        ...

    def supports_multiple_references(self) -> bool:
        ...

    def supports_safety_metadata(self) -> bool:
        ...
```

Provider config:

```json
{
  "defaultProvider": "openai",
  "providers": {
    "openai": {
      "enabled": true,
      "supportsReferences": true,
      "supportsSafetyMetadata": true,
      "requiresDisclosure": true
    },
    "local-comfyui": {
      "enabled": false,
      "supportsReferences": true,
      "supportsSafetyMetadata": false,
      "requiresDisclosure": true
    }
  }
}
```

---

## 10. False-Positive Moderation Handling

### 10.1 Moderation Event Schema

```json
{
  "event_id": "uuid",
  "project": "Vanessa",
  "provider": "openai",
  "request_id": "provider_request_id",
  "prompt_original": "Make a perfect clone of Vanessa by the pool",
  "prompt_normalized": "Create an authorized synthetic likeness image of Vanessa using approved references...",
  "blocked": true,
  "error_type": "provider_policy_block",
  "suspected_false_positive": true,
  "retry_level": 1,
  "review_required": true,
  "timestamp": "timestamp"
}
```

### 10.2 Retry Levels

```text
0: normalized prompt
1: add consent and synthetic-disclosure language
2: remove ambiguous/deceptive realism language
3: convert to editorial/stylized output
4: stop and require human review
```

The system must never continue retrying after Level 4.

---

## 11. Review Workflow Requirements

Generated outputs have states:

```text
draft
approved
rejected
published
archived
```

Output metadata:

```json
{
  "output_id": "uuid",
  "project": "Vanessa",
  "provider": "openai",
  "source_request_id": "uuid",
  "storage_path": "outputs/draft/image.png",
  "state": "draft",
  "likeness_score": null,
  "artifact_score": null,
  "reviewed_by": null,
  "reviewed_at": null,
  "public_disclosure_required": true,
  "provenance_required": true
}
```

Approval criteria:

- Subject consistency acceptable.
- No unauthorized third-party likeness.
- No distorted hands/face/body severe enough to harm brand quality.
- Intended use matches consent.
- Disclosure requirement recorded.
- Human reviewer approves.

---

## 12. Quality Scoring Requirements

The RC should support manual scoring now and automated scoring later.

Score categories:

- Face similarity.
- Body consistency.
- Hair consistency.
- Eye consistency.
- Age consistency.
- Skin tone consistency.
- Pose realism.
- Hand accuracy.
- Wardrobe accuracy.
- Background quality.
- Artifact severity.

Schema:

```json
{
  "output_id": "uuid",
  "likeness_score": 0.88,
  "artifact_score": 0.12,
  "pose_score": 0.91,
  "approved": false,
  "review_notes": "Good likeness; hand needs regeneration."
}
```

---

## 13. API Endpoint Requirements

Required endpoints:

```http
POST   /api/likeness/projects
GET    /api/likeness/projects
GET    /api/likeness/projects/{projectName}
POST   /api/likeness/projects/{projectName}/consent
GET    /api/likeness/projects/{projectName}/consent
POST   /api/likeness/projects/{projectName}/references
GET    /api/likeness/projects/{projectName}/references
POST   /api/likeness/projects/{projectName}/references/{imageId}/approve
POST   /api/likeness/projects/{projectName}/references/{imageId}/reject
POST   /api/likeness/projects/{projectName}/generate
GET    /api/likeness/projects/{projectName}/outputs
POST   /api/likeness/projects/{projectName}/outputs/{outputId}/approve
POST   /api/likeness/projects/{projectName}/outputs/{outputId}/reject
POST   /api/likeness/projects/{projectName}/outputs/{outputId}/publish
GET    /api/likeness/projects/{projectName}/moderation-events
GET    /api/likeness/projects/{projectName}/audit
```

---

## 14. Security Requirements

Roles:

```text
admin
creator
reviewer
viewer
subject
```

Permissions:

```text
admin: full access
creator: create generation requests and draft outputs
reviewer: approve/reject references and outputs
viewer: view approved/published outputs only
subject: view own project, approve public use, revoke consent
```

Security controls:

- Auth required for all endpoints.
- Signed URLs for private assets.
- Hash all files.
- Never overwrite originals.
- Encrypt storage at rest.
- Audit all mutations.
- Support consent revocation.
- Block generation after revocation.

---

## 15. Audit and Provenance Requirements

Every meaningful action must create an audit log entry.

```json
{
  "event_id": "uuid",
  "actor": "ShannonBrayNC",
  "action": "approve_reference",
  "project": "Vanessa",
  "target_id": "image_uuid",
  "timestamp": "timestamp",
  "result": "success"
}
```

Required audited actions:

- Project creation.
- Consent creation/update/revocation.
- Reference import.
- Reference approval/rejection.
- Generation request.
- Provider block/error.
- Output approval/rejection/publication.
- Export.
- Deletion/archive.

---

## 16. UI Requirements

Minimum RC dashboard:

- Project cards.
- Consent status.
- Reference counts.
- Draft/approved/published output counts.
- Moderation event count.
- Last generation timestamp.

Project detail tabs:

```text
Overview
Consent
References
Prompt Library
Generate
Drafts
Approved
Published
Moderation Events
Audit Log
```

Generation UI must show preflight warnings before provider calls.

Example warnings:

```text
Generation blocked: consent record missing.
Generation blocked: selected image contains an unapproved third-party face.
Generation warning: public-use disclosure required.
```

---

## 17. Required PowerShell 7+ Tools

### create-project.ps1

Creates project structure from `_template`.

### import-references.ps1

Imports images into pending references and writes metadata.

### audit-project.ps1

Checks consent, folder integrity, metadata integrity, and orphaned outputs.

### export-approved.ps1

Exports only approved or published images with metadata and disclosure notes.

---

## 18. Testing Requirements

Minimum tests:

- Project creation creates all required folders.
- Missing consent blocks generation.
- Approved consent allows generation preflight.
- Expired consent blocks generation.
- Revoked consent blocks generation.
- Pending reference cannot be used for generation.
- Approved reference can be used.
- Rejected reference cannot be used.
- Provider policy block creates moderation event.
- Retry logic stops at Level 4.
- Output starts in draft state.
- Only reviewer/admin can approve outputs.
- Published output requires disclosure metadata.
- Project audit detects missing folders and missing consent.

---

## 19. Production RC Definition of Done

The RC is complete when:

- Shannon and Vanessa folders exist.
- `_template` exists.
- Consent schemas exist.
- API stubs/routes exist.
- Provider interface exists.
- Preflight validator blocks unsafe or unauthorized generation.
- Reference import/approval workflow exists.
- Draft/approved/rejected/published output workflow exists.
- Moderation event logging exists.
- False-positive retry handling exists without bypass behavior.
- Audit logging exists.
- PowerShell 7+ tools exist.
- Tests pass locally and in CI.
- README documents the consent-first workflow.
- The system can add future likeness projects without code changes.

---

## 20. Suggested Implementation Order

### Sprint 1 - Structure and Consent Gate

- Add folders.
- Add schemas.
- Add create-project.ps1.
- Add consent preflight.
- Add initial tests.

### Sprint 2 - Reference Management

- Add import workflow.
- Add metadata hashing.
- Add approval/rejection flow.
- Add audit logs.

### Sprint 3 - Generation API Layer

- Add provider interface.
- Add OpenAI provider stub.
- Add prompt normalization.
- Add moderation event capture.
- Store generated outputs as drafts.

### Sprint 4 - Review, Publish, and Export

- Add review workflow.
- Add quality scoring.
- Add export-approved.ps1.
- Add dashboard tabs.
- Finalize tests and README.

---

## 21. Codex Build Instruction

Use this issue as the source of truth. Implement incrementally with tests. Do not build bypasses for AI/provider safety systems. Build robust consent, provenance, prompt normalization, moderation logging, and human-review workflows so authorized likeness generation is reliable, auditable, and production-safe.
