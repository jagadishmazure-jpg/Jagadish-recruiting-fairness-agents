# Guardrails and security controls

| Control | Where | Test that proves it |
|---|---|---|
| Redact before any processing | `pii.redact`, `pipeline.run` | `test_all_synthetic_resumes_clean_after_redaction`, `test_no_leaks` |
| Extractor refuses unredacted text | `extract.extract` | `test_extract_refuses_unredacted_and_error_is_clean` |
| Errors never carry PII | `pii.SafeError` | `test_safe_error_redacts_message` |
| Logs never carry PII | `pii.RedactingFilter` | `test_logger_redacts` |
| Audit log refuses PII payloads | `audit.AuditLog.append` | `test_pii_payload_rejected` |
| Outputs on disk carry no PII | `cli.demo` | `test_outputs_have_no_pii` |
| Keyed pseudonyms, rotatable key | `pii.pseudonym` | `test_pseudonym_env_key` |
| Scorer cannot see the group | module boundary | `test_score_ignores_name`, name swap = 0 flips |
| Every score explained | `scorer.explained` | `test_all_matches_explained`, `test_unexplained_match_blocks_approval` |
| Fairness audit before approval | `signoff.Shortlist` | `test_cannot_approve_before_audit` |
| Human approval, agents refused | `signoff.approve` | `test_agent_cannot_approve` |
| Written override on failed audit | `signoff.approve` | `test_failed_audit_needs_reason`, `test_override_logged` |
| No release without approval | `signoff.release` | `test_release_without_approval_blocked` |
| Tamper-evident records | `audit.verify` | `test_edit_detected`, `test_delete_detected`, `test_reorder_detected` |
| Supply chain | CI | pinned actions, gitleaks, CodeQL, Dependabot, hashed brand check |

Key rotation: set a new `RECFAIR_HMAC_KEY`, re-pseudonymise open records, and keep the old key sealed only as long as retention rules require. Old pseudonyms do not link to new ones by design.
