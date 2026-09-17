import re

with open('c:/Users/hmhar/Projects/Disaster_Coordinator/backend/graph/build_graph.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Add import
if 'from backend.utils.logger import get_audit_logger' not in code:
    code = code.replace(
        'from backend.agents.evaluator_agent import EvaluatorAgent',
        'from backend.agents.evaluator_agent import EvaluatorAgent\nfrom backend.utils.logger import get_audit_logger'
    )

# Add logger setup inside build_coordinator_graph
if 'audit_logger = get_audit_logger()' not in code:
    code = code.replace(
        '    eval_agent = EvaluatorAgent()',
        '    eval_agent = EvaluatorAgent()\n    audit_logger = get_audit_logger()'
    )

# Instrument ingest_node
old_ingest = """    def ingest_node(state: CoordinatorState):
        extracted = ingest_agent.process(state["raw_report"])
        return {"extracted_need": extracted}"""
new_ingest = """    def ingest_node(state: CoordinatorState):
        extracted = ingest_agent.process(state["raw_report"])
        audit_logger.info("Ingestion complete", extra={"action": "ingest", "report_id": state["raw_report"].report_id})
        return {"extracted_need": extracted}"""
code = code.replace(old_ingest, new_ingest)

# Instrument verify_node
old_verify = """    def verify_node(state: CoordinatorState):
        verified = verify_agent.process(state["extracted_need"], state.get("existing_needs", []))
        return {
            "verified_need": verified,
            "requires_human_review": verified.requires_human_review
        }"""
new_verify = """    def verify_node(state: CoordinatorState):
        verified = verify_agent.process(state["extracted_need"], state.get("existing_needs", []))
        audit_logger.info("Verification complete", extra={"action": "verify", "need_id": verified.need_id})
        return {
            "verified_need": verified,
            "requires_human_review": verified.requires_human_review
        }"""
code = code.replace(old_verify, new_verify)

# Instrument match_node
old_match = """    def match_node(state: CoordinatorState):
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
        audit_logger.info("Matching complete", extra={"action": "match", "allocations_count": len(allocs)})
        return {"allocations": allocs}"""
code = code.replace(old_match, new_match)

# Instrument eval_node
old_eval = """    def eval_node(state: CoordinatorState):
        needs = state.get("existing_needs", [])
        if state.get("verified_need"):
            needs.append(state["verified_need"])
            
        result = eval_agent.process(state["plan"], needs)
        new_rev_count = state.get("revision_count", 0) + 1
        return {
            "evaluation": result,
            "revision_count": new_rev_count
        }"""
new_eval = """    def eval_node(state: CoordinatorState):
        needs = state.get("existing_needs", [])
        if state.get("verified_need"):
            needs.append(state["verified_need"])
            
        result = eval_agent.process(state["plan"], needs)
        new_rev_count = state.get("revision_count", 0) + 1
        audit_logger.info("Evaluation complete", extra={"action": "evaluate", "passed": result.passed, "fairness": result.fairness_score})
        return {
            "evaluation": result,
            "revision_count": new_rev_count
        }"""
code = code.replace(old_eval, new_eval)

with open('c:/Users/hmhar/Projects/Disaster_Coordinator/backend/graph/build_graph.py', 'w', encoding='utf-8') as f:
    f.write(code)
