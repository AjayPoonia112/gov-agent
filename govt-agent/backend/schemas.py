from pydantic import BaseModel
from typing import Optional, List

class UserProfile(BaseModel):
    age: Optional[int] = None
    annual_income: Optional[int] = None
    occupation: Optional[str] = None          # farmer / student / worker / unemployed / self-employed
    land_owned: Optional[bool] = None
    land_size_acres: Optional[float] = None
    disability: Optional[bool] = None
    caste_category: Optional[str] = None      # SC/ST/OBC/GEN
    has_bank_account: Optional[bool] = None
    has_aadhaar: Optional[bool] = None
    has_pan: Optional[bool] = None
    has_ration_card: Optional[bool] = None
    ration_card_type: Optional[str] = None    # BPL/PHH/APL etc.
    gender: Optional[str] = None              # male/female/other
    state: Optional[str] = None               # e.g., WB
    district: Optional[str] = None
    student_marks_pct: Optional[float] = None
    student_course: Optional[str] = None

class EligibilityResult(BaseModel):
    scheme_id: str
    scheme_name: str
    benefits: Optional[str] = None
    documents_required: List[str] = []
    application_steps: List[str] = []
    official_url: Optional[str] = None
    score: int
    reasons: List[str] = []

class EligibilityResponse(BaseModel):
    eligible_schemes: List[EligibilityResult]

class WhatsAppInbound(BaseModel):
    From: Optional[str] = None
    Body: Optional[str] = None