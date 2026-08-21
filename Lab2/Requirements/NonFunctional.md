# Non-Functional Requirements

## Performance and capacity

| ID | Requirement and verification | Responsible role |
| --- | --- | --- |
| NFR-PER-01 | The 95th percentile for validating an application, calculating a quote and returning the preliminary decision shall be ≤ 3 seconds with 200 concurrent users and 20 submissions per second. | Platform administrator |
| NFR-PER-02 | The 95th percentile for opening an application or operations worklist shall be ≤ 2 seconds with 100,000 active applications in the test dataset. | Platform administrator |
| NFR-CAP-01 | The pilot shall support 5,000 registered companies, 500 internal users and 100,000 applications while meeting `NFR-PER-01/02`. | Platform administrator |

## Availability and recovery

| ID | Requirement and verification | Responsible role |
| --- | --- | --- |
| NFR-AVL-01 | Monthly availability shall be ≥ 99.5% for application intake, formal review and status consultation, excluding announced maintenance. | Platform administrator |
| NFR-REC-01 | After a simulated total service outage, the pilot shall restore service in ≤ 30 minutes with no more than 5 minutes of confirmed transactional data loss. The test shall run quarterly. | Platform administrator |

## Security and privacy

| ID | Requirement and verification | Responsible role |
| --- | --- | --- |
| NFR-SEC-01 | Applicant, financial and decision data shall be encrypted in transit and at rest. All unauthorized attempts in the role-and-case test matrix shall be denied and audited. | Platform administrator |
| NFR-SEC-02 | Internal users shall use multi-factor authentication; sessions shall expire after 15 minutes of inactivity. | Platform administrator |
| NFR-SEC-03 | Before a real negative-record or private credit-bureau query, the platform shall verify an authorized purpose, provider credentials and the applicable applicant notice/legal-basis reference. Attempts without them shall be denied and audited. | Data-protection owner |
| NFR-PRV-01 | The platform shall collect only fields identified in the approved data inventory and shall apply a documented retention period to application evidence. A quarterly review shall report fields without purpose or retention rule. | Data-protection owner |

## Reliability and auditability

| ID | Requirement and verification | Responsible role |
| --- | --- | --- |
| NFR-REL-01 | Submission and quote acceptance operations shall be idempotent. Repeating the same request 20 times with one idempotency key shall create one application or one transition. | Platform administrator |
| NFR-REL-02 | A negative-record or bureau timeout, malformed response or unavailable provider shall never be converted into an adverse credit result. The case shall enter a technical-review state with the failed source and correlation ID. | Platform administrator |
| NFR-AUD-01 | Audit records shall be append-only for application users and shall be retained with synchronized timestamps. A tampering test shall prove that ordinary roles cannot update or delete them. | Platform administrator |

## Usability and compatibility

| ID | Requirement and verification | Responsible role |
| --- | --- | --- |
| NFR-USA-01 | At least 90% of representative SME users shall complete the valid initial request in ≤ 5 minutes without assistance after a ≤ 5-minute introduction. | Product owner |
| NFR-USA-02 | At least 90% of test users shall correctly identify that the quote is preliminary, the financed amount and the next step. | Product owner |
| NFR-COM-01 | Applicant flows shall support current desktop and mobile layouts from 360 px width without hiding mandatory information or actions. | Product owner |

## Observability

| ID | Requirement and verification | Responsible role |
| --- | --- | --- |
| NFR-OBS-01 | The operational dashboard shall report each minute request rate, decision latency, error rate and counts by application status; every API error shall include a correlation ID. | Platform administrator |
| NFR-OBS-02 | Each external-risk query shall record provider, start/end time, outcome (`CLEAR`, `FOUND`, `SUCCESS`, `TIMEOUT` or `ERROR`), correlation ID and whether the short-circuit prevented later queries, without placing full sensitive reports in application logs. | Platform administrator |

## POC boundary

`NFR-SEC-03`, `NFR-REL-02` and `NFR-OBS-02` specify safeguards for a future authorized integration. The current POC uses deterministic local adapters, contains no real external credit data and proves only the successful call order and negative-record short-circuit.
