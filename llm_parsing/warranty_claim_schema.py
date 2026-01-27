from pydantic import BaseModel
from typing import List, Optional


class FaultCode(BaseModel):
    code: Optional[str]
    description: Optional[str]
    system: Optional[str]
    status: Optional[str]


class PartItem(BaseModel):
    part_number: Optional[str]
    description: Optional[str]
    quantity: Optional[int]
    unit_price: Optional[float]
    total: Optional[float]


class LaborInfo(BaseModel):
    hours: Optional[float]
    rate: Optional[float]
    total: Optional[float]


class Totals(BaseModel):
    parts_subtotal: Optional[float]
    labor_subtotal: Optional[float]
    claimed_amount: Optional[float]
    approved_amount: Optional[float]


class AIReview(BaseModel):
    fraud_score: Optional[int]
    recommendation: Optional[str]


class WarrantyClaimSchema(BaseModel):
    claim_id: Optional[str]
    claim_date: Optional[str]

    vehicle_vin: Optional[str]
    vehicle_model: Optional[str]
    vehicle_mileage: Optional[int]

    dealer_code: Optional[str]
    dealer_name: Optional[str]
    dealer_address: Optional[str]

    fault_codes: List[FaultCode] = []
    parts: List[PartItem] = []
    labor: Optional[LaborInfo]

    totals: Optional[Totals]
    ai_review: Optional[AIReview]
