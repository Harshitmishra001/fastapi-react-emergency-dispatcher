import math
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from backend.schemas.models import VerifiedNeed, ResourceRecord, Allocation, UrgencyLevel
from backend.config.model_router import get_llm

def haversine_distance(coord1, coord2):
    if not coord1 or not coord2:
        return 9999.0 # Unknown distance, penalize
        
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371.0 # Earth radius in km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class ResourceMatcher:
    def __init__(self):
        self.llm = get_llm("local", temperature=0.1)
        
        self.tiebreak_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an emergency coordination tie-breaker.
You are given two locations that are equidistant and have the same priority.
Choose the one that sounds more accessible or safer based on the name.
Respond with EXACTLY the need_id of the preferred location. No other text."""),
            ("user", "Location A (need_id: {id_a}): {loc_a}\nLocation B (need_id: {id_b}): {loc_b}")
        ])

    def _urgency_weight(self, urgency: UrgencyLevel) -> int:
        weights = {
            UrgencyLevel.CRITICAL: 4,
            UrgencyLevel.HIGH: 3,
            UrgencyLevel.MODERATE: 2,
            UrgencyLevel.LOW: 1
        }
        return weights.get(urgency, 1)

    def process(self, needs: List[VerifiedNeed], resources: List[ResourceRecord]) -> List[Allocation]:
        # For Phase 2, we implement the Greedy Fallback method.
        # ILP optimization will be swapped in later if needed.
        
        allocations = []
        
        # Sort needs by urgency descending
        sorted_needs = sorted(needs, key=lambda n: self._urgency_weight(n.urgency), reverse=True)
        
        # Keep track of available quantities
        available_resources = {r.resource_id: r for r in resources if r.status == "available" and r.quantity_available > 0}
        
        for need in sorted_needs:
            needed_qty = need.quantity_estimate
            if needed_qty <= 0:
                continue
                
            # Filter resources by type
            matching_resources = [r for r in available_resources.values() if r.resource_type == need.need_type]
            
            # Sort resources by distance
            matching_resources.sort(key=lambda r: haversine_distance(need.coordinates, r.location))
            
            # Allocate greedily
            for res in matching_resources:
                if needed_qty <= 0:
                    break
                    
                if res.quantity_available <= 0:
                    continue
                    
                # Note: Tie-breaker LLM call could be inserted here if distances are exactly equal.
                # To keep the greedy solver fast, we rely on the stable sort for now unless explicitly requested.
                
                allocated_qty = min(needed_qty, res.quantity_available)
                dist = haversine_distance(need.coordinates, res.location)
                
                allocations.append(Allocation(
                    need_id=need.need_id,
                    resource_id=res.resource_id,
                    quantity_allocated=allocated_qty,
                    distance_km=round(dist, 2),
                    allocation_method="greedy_fallback"
                ))
                
                res.quantity_available -= allocated_qty
                needed_qty -= allocated_qty
                
        return allocations
