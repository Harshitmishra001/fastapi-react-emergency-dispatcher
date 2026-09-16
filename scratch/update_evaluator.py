import re
with open('c:/Users/hmhar/Projects/Disaster_Coordinator/backend/agents/evaluator_agent.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Update the LLMEvaluation model description for revision_notes
code = code.replace(
    'revision_notes: Optional[str] = Field(description="If passed is False, specific instructions to the Resource Matcher on how to fix the plan.")',
    'revision_notes: Optional[str] = Field(description="If passed is False, specific instructions to the Resource Matcher on how to fix the plan. You MUST use the exact need_id for any needs you mention.")'
)

with open('c:/Users/hmhar/Projects/Disaster_Coordinator/backend/agents/evaluator_agent.py', 'w', encoding='utf-8') as f:
    f.write(code)
