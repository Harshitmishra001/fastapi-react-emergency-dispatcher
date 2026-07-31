import asyncio
from datetime import datetime, timezone
from backend.schemas.models import RawReport
from backend.graph.build_graph import build_coordinator_graph

async def main():
    print("Building graph...")
    graph = build_coordinator_graph()
    
    report = RawReport(
        report_id="test-rpt-001",
        source_channel="sms",
        raw_text="URGENT: We have about 50 people at the community center and we are out of water and blankets. Please send help quickly!",
        submitted_at=datetime.now(timezone.utc)
    )
    
    config = {"configurable": {"thread_id": report.report_id}}
    state = {"raw_report": report}
    
    print("Starting execution...")
    try:
        # stream_mode="values" yields the full state after each node
        for event in graph.stream(state, config, stream_mode="values"):
            pass
            
        final_state = graph.get_state(config)
        
        print("\n--- EXECUTION COMPLETED ---")
        if final_state.next and "human_review" in final_state.next:
            print("Status: PAUSED for Human Review (Confidence was too low or duplicate suspected).")
        else:
            print("Status: AUTOMATICALLY PROCESSED.")
            
        print("\nExtracted Need:")
        print(final_state.values.get("extracted_need"))
        
        print("\nVerified Need:")
        print(final_state.values.get("verified_need"))
        
        print("\nAllocations:")
        print(final_state.values.get("allocations"))
        
        print("\nDispatch Plan:")
        print(final_state.values.get("plan"))
        
        print("\nEvaluation:")
        print(final_state.values.get("evaluation"))
        
    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    asyncio.run(main())
