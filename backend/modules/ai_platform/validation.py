"""
Response Validation Engine (EP-08).
Validates AI responses for missing citations, empty context, and hallucination indicators.
"""
import logging
from typing import List
from .models import LLMResponse, ValidationResult

logger = logging.getLogger("AIPlatform.Validation")


class ResponseValidationEngine:
    """
    Validates every AI response before returning it to the user.
    On failure, a safe fallback message is returned instead.
    """

    SAFE_FALLBACK = (
        "I was unable to find sufficient enterprise-verified information to answer "
        "this question confidently. Please consult your Knowledge Manager or review "
        "the relevant documentation directly."
    )

    def validate(
        self,
        response: LLMResponse,
        context_had_passages: bool,
        min_length: int = 20
    ) -> ValidationResult:
        issues: List[str] = []

        # 1. Empty response check
        if not response.raw_text or not response.raw_text.strip():
            issues.append("AI returned an empty response.")

        # 2. Provider-level failure (empty text + zero tokens)
        if not response.raw_text and response.total_tokens == 0:
            issues.append("Provider returned zero tokens — possible connectivity issue.")

        # 3. Context vacuum check
        if not context_had_passages:
            issues.append("Response generated with no enterprise context (low confidence).")

        # 4. Suspiciously short answer
        if response.raw_text and len(response.raw_text.strip()) < min_length:
            issues.append(f"Response is unusually short ({len(response.raw_text)} chars).")

        # 5. Hallucination heuristics (simple pattern checks — not ML-based)
        hallucination_flags = [
            "as of my knowledge cutoff",
            "I don't have access to",
            "based on general knowledge",
            "i cannot be certain",
        ]
        text_lower = response.raw_text.lower()
        for flag in hallucination_flags:
            if flag in text_lower:
                issues.append(f"Possible hallucination indicator detected: '{flag}'")

        passed = len(issues) == 0
        confidence = "HIGH" if passed else ("MEDIUM" if len(issues) <= 1 else "LOW")

        return ValidationResult(passed=passed, issues=issues, confidence_level=confidence)

    def safe_response(self, validation: ValidationResult) -> str:
        """Returns the safe fallback with validation notes appended."""
        notes = "; ".join(validation.issues)
        return f"{self.SAFE_FALLBACK}\n\n[Validation Notes: {notes}]"
