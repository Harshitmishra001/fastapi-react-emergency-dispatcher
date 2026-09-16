import re
with open('c:/Users/hmhar/Projects/Disaster_Coordinator/backend/agents/resource_matcher.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Update process signature
code = code.replace(
    'def process(self, needs: List[VerifiedNeed], resources: List[ResourceRecord]) -> List[Allocation]:',
    'def process(self, needs: List[VerifiedNeed], resources: List[ResourceRecord], revision_notes: str = None) -> List[Allocation]:'
)

# Update the objective weight calculation to boost if need_id is in revision_notes
old_weight_calc = """                    # Base value is urgency weight. We subtract distance to prefer closer resources.
                    # As long as distance penalty < 1000, it won't override a higher urgency category.
                    weight = urgency_w - min(dist, 999.0)
                    objective_terms.append(weight * var)"""

new_weight_calc = """                    # Base value is urgency weight. We subtract distance to prefer closer resources.
                    # As long as distance penalty < 1000, it won't override a higher urgency category.
                    weight = urgency_w - min(dist, 999.0)
                    
                    # If evaluator flagged this need for revision, massively boost it
                    if revision_notes and n.need_id in revision_notes:
                        weight += 500000.0
                        
                    objective_terms.append(weight * var)"""

code = code.replace(old_weight_calc, new_weight_calc)

with open('c:/Users/hmhar/Projects/Disaster_Coordinator/backend/agents/resource_matcher.py', 'w', encoding='utf-8') as f:
    f.write(code)
