from typing import Dict, Optional, List
from datetime import datetime, timezone, timedelta
from logging import getLogger
import uuid

from .models import CertificateTemplate, Certificate
from .enums import CertificateStatus

logger = getLogger("CertificateEngine")

class CertificateEngine:
    def __init__(self):
        self._templates: Dict[str, CertificateTemplate] = {}
        self._certificates: Dict[str, Certificate] = {}

    def get_template(self, template_id: str) -> Optional[CertificateTemplate]:
        return self._templates.get(template_id)

    def register_template(self, template: CertificateTemplate):
        self._templates[template.id] = template
        logger.info(f"Registered Certificate Template: {template.name}")

    def evaluate_eligibility(self, user_id: str, template_id: str) -> bool:
        """Mock method to evaluate if a user meets the eligibility rules for a template."""
        # In a real system, this would query ProgressEngine, AssessmentEngine, and CompetencyEngine
        logger.debug(f"Evaluating eligibility for User {user_id} on Template {template_id}")
        return True # Mocked as eligible

    def request_certificate(self, user_id: str, template_id: str) -> Certificate:
        template = self.get_template(template_id)
        if not template:
            raise ValueError("Template not found")

        if not self.evaluate_eligibility(user_id, template_id):
            raise ValueError("User is not eligible for this certificate")

        cert = Certificate(
            id=str(uuid.uuid4()),
            certificate_number=f"CERT-{uuid.uuid4().hex[:8].upper()}",
            template_id=template_id,
            user_id=user_id,
            status=CertificateStatus.PENDING_APPROVAL if (template.eligibility.requires_manager_approval or template.eligibility.requires_hr_approval or template.eligibility.requires_department_approval) else CertificateStatus.ACTIVE
        )

        if cert.status == CertificateStatus.ACTIVE:
            cert.issue_date = datetime.now(timezone.utc)
            if template.validity_period_days:
                cert.expiry_date = cert.issue_date + timedelta(days=template.validity_period_days)
        
        self._certificates[cert.id] = cert
        logger.info(f"Certificate {cert.certificate_number} requested for User {user_id}. Status: {cert.status.value}")
        return cert

    def validate_certificate(self, certificate_number: str) -> Optional[Certificate]:
        for cert in self._certificates.values():
            if cert.certificate_number == certificate_number:
                if cert.expiry_date and cert.expiry_date < datetime.now(timezone.utc) and cert.status == CertificateStatus.ACTIVE:
                    cert.status = CertificateStatus.EXPIRED
                    logger.info(f"Certificate {certificate_number} automatically expired.")
                return cert
        return None

    def revoke_certificate(self, certificate_id: str) -> Optional[Certificate]:
        cert = self._certificates.get(certificate_id)
        if cert:
            cert.status = CertificateStatus.REVOKED
            logger.warning(f"Certificate {cert.certificate_number} has been REVOKED.")
        return cert
