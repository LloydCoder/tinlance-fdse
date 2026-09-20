from uuid import UUID
from .domain import Evidence, Finding, Project, RepositoryRef, VerificationResult, VerificationStatus
from .evidence import digest
from .ports import EvidenceStore, FindingStore, ProjectStore, VerificationStore
from .policy import DenyByDefaultPolicy

class FdseService:
    def __init__(self, projects: ProjectStore, findings: FindingStore, evidence: EvidenceStore, verifications: VerificationStore, policy: DenyByDefaultPolicy | None = None):
        self.projects,self.findings,self.evidence,self.verifications = projects,findings,evidence,verifications
        self.policy = policy or DenyByDefaultPolicy()

    def create_project(self, tenant_id: UUID, name: str, repository: RepositoryRef) -> Project:
        project = Project.create(tenant_id,name,repository); self.projects.save(project); return project

    def record_evidence(self, kind: str, summary: str, payload: object, source: str) -> Evidence:
        item = Evidence.create(kind,summary,digest(payload),source); self.evidence.save(item); return item

    def record_finding(self, tenant_id: UUID, project_id: UUID, title: str, category: str, severity: str, evidence_ids: tuple[UUID,...]=()) -> Finding:
        project = self.projects.get(project_id)
        if project is None or project.tenant_id != tenant_id: raise PermissionError("project is not accessible to tenant")
        finding = Finding.create(project_id,title,category,severity,evidence_ids); self.findings.save(finding); return finding

    def verify_finding(self, tenant_id: UUID, finding_id: UUID, status: VerificationStatus, checks: tuple[str,...], evidence_ids: tuple[UUID,...]=()) -> VerificationResult:
        finding = self.findings.get(finding_id)
        if finding is None: raise LookupError("finding not found")
        project = self.projects.get(finding.project_id)
        if project is None or project.tenant_id != tenant_id: raise PermissionError("finding is not accessible to tenant")
        if status is VerificationStatus.PASSED and not self.policy.authorize(tenant_id,"verify_remediation","high"):
            raise PermissionError("verification requires external policy authorization")
        result = VerificationResult.create(finding_id,status,checks,evidence_ids); self.verifications.save(result); return result
