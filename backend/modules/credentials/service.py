from typing import Dict, List
from datetime import datetime, timezone
from logging import getLogger
import uuid

from .models import DigitalBadge, CredentialVerification
from backend.modules.certificates.service import CertificateEngine
from backend.modules.certificates.enums import CertificateStatus

logger = getLogger("VerificationEngine")

class VerificationEngine:
    def __init__(self, certificate_engine: CertificateEngine):
        self.certificate_engine = certificate_engine
        self._badges: Dict[str, DigitalBadge] = {}

    def issue_badge(self, badge: DigitalBadge) -> DigitalBadge:
        self._badges[badge.id] = badge
        logger.info(f"Issued badge {badge.name} to User {badge.user_id}")
        return badge

    def verify_certificate(self, certificate_number: str) -> CredentialVerification:
        logger.info(f"Publicly verifying certificate: {certificate_number}")
        
        cert = self.certificate_engine.validate_certificate(certificate_number)
        
        if not cert:
            return CredentialVerification(
                is_valid=False,
                message="Certificate not found.",
                verification_type="CERTIFICATE",
                identifier=certificate_number,
                issued_to="UNKNOWN"
            )
            
        is_valid = cert.status == CertificateStatus.ACTIVE
        return CredentialVerification(
            is_valid=is_valid,
            message=f"Certificate is {cert.status.value}",
            verification_type="CERTIFICATE",
            identifier=cert.certificate_number,
            issued_to=cert.user_id,
            issued_at=cert.issue_date,
            expires_at=cert.expiry_date,
            status_enum=cert.status.value
        )
