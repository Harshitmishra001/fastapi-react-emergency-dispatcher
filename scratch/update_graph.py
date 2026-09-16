import re
with open('c:/Users/hmhar/Projects/Disaster_Coordinator/backend/graph/build_graph.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_match = """    def match_node(state: CoordinatorState):
        # Gather all needs: existing + the newly verified one
        needs = state.get("existing_needs", [])
        if state.get("verified_need"):
            needs.append(state["verified_need"])
            
        allocs = match_agent.process(needs, state.get("available_resources", []))
        return {"allocations": allocs}"""

new_match = """    def match_node(state: CoordinatorState):
        # Gather all needs: existing + the newly verified one
        needs = state.get("existing_needs", [])
        if state.get("verified_need"):
            needs.append(state["verified_need"])
            
        revision_notes = None
        evaluation = state.get("evaluation")
        if evaluation and not evaluation.passed:
            revision_notes = evaluation.revision_notes
            
        allocs = match_agent.process(needs, state.get("available_resources", []), revision_notes=revision_notes)
        return {"allocations": allocs}"""

code = code.replace(old_match, new_match)

with open('c:/Users/hmhar/Projects/Disaster_Coordinator/backend/graph/build_graph.py', 'w', encoding='utf-8') as f:
    f.write(code)
