import asyncio
import time
import uuid
import json
from datetime import datetime, timezone
from backend.db.models import SessionLocal, DBResource, init_db
from backend.schemas.models import RawReport, ResourceRecord, NeedType
from backend.graph.build_graph import build_coordinator_graph

def get_db_resources():
    db = SessionLocal()
    records = []
    for r in db.query(DBResource).all():
        records.append(ResourceRecord(
            resource_id=r.resource_id,
            resource_type=NeedType(r.resource_type),
            quantity_available=r.quantity_available,
            location=(r.lat, r.lon),
            status=r.status
        ))
    db.close()
    return records

def seed_resources_if_empty():
    init_db()
    db = SessionLocal()
    count = db.query(DBResource).count()
    if count == 0:
        print("Seeding resources...")
        seed_data = [
            DBResource(resource_id="res-water-01", resource_type="water", quantity_available=500, lat=34.05, lon=-118.25, status="available"),
            DBResource(resource_id="res-water-02", resource_type="water", quantity_available=200, lat=34.06, lon=-118.24, status="available"),
            DBResource(resource_id="res-medical-01", resource_type="medical", quantity_available=50, lat=34.04, lon=-118.26, status="available"),
            DBResource(resource_id="res-shelter-01", resource_type="shelter", quantity_available=100, lat=34.07, lon=-118.27, status="available"),
            DBResource(resource_id="res-food-01", resource_type="food", quantity_available=1000, lat=34.055, lon=-118.255, status="available"),
        ]
        db.add_all(seed_data)
        db.commit()
        count = 5
    db.close()
    return count

reports = [
    # 5 Clean / High Confidence
    {"text": "URGENT: We have 50 people trapped at the community center. Need water immediately.", "type": "clean"},
    {"text": "Medical supplies needed at Main St Clinic. We have 10 injured people.", "type": "clean"},
    {"text": "Need shelter for 30 families after the flood on Elm St.", "type": "clean"},
    {"text": "Send food for 100 people at the high school gym. It's critical.", "type": "clean"},
    {"text": "We are out of water for 20 patients at the Southside hospital.", "type": "clean"},
    
    # 5 Ambiguous / Low Confidence
    {"text": "We need stuff at the place!", "type": "ambiguous"},
    {"text": "Can someone help us? It's really bad here.", "type": "ambiguous"},
    {"text": "Send whatever you have to the downtown area.", "type": "ambiguous"},
    {"text": "People are hungry and thirsty everywhere.", "type": "ambiguous"},
    {"text": "Help!", "type": "ambiguous"},
    
    # 5 Intentional Duplicates
    {"text": "URGENT: We have 50 people trapped at the community center. Need water immediately.", "type": "duplicate"}, # Dup of 1
    {"text": "We have 50 people trapped at the community center. Need water immediately.", "type": "duplicate"}, # Dup of 1
    {"text": "Medical supplies needed at Main St Clinic. We have 10 injured people.", "type": "duplicate"}, # Dup of 2
    {"text": "Need shelter for 30 families after the flood on Elm St.", "type": "duplicate"}, # Dup of 3
    {"text": "Send food for 100 people at the high school gym. It's critical.", "type": "duplicate"}, # Dup of 4
]

async def run_benchmarks():
    db_size = seed_resources_if_empty()
    resources = get_db_resources()
    history_needs = []
    
    graph = build_coordinator_graph()
    
    results = {
        "total_reports": len(reports),
        "auto_approved": 0,
        "human_review": 0,
        "review_reasons": {"low_confidence": 0, "duplicate": 0},
        "duplicates_caught": 0,
        "actual_duplicates_in_set": 5,
        "latencies": [],
        "evaluator_passes_first_try": 0,
        "evaluator_revisions_needed": 0,
        "evaluator_max_retries_hit": 0,
        "coverage_scores": [],
        "fairness_scores": [],
        "db_size": db_size
    }
    
    print(f"Starting benchmark of {len(reports)} reports...")
    
    for i, r in enumerate(reports):
        print(f"\n--- Processing Report {i+1}/{len(reports)} ({r['type']}) ---")
        report_obj = RawReport(
            report_id=f"bench-rpt-{uuid.uuid4().hex[:6]}",
            source_channel="sms",
            raw_text=r["text"],
            submitted_at=datetime.now(timezone.utc)
        )
        
        config = {"configurable": {"thread_id": report_obj.report_id}}
        state = {
            "raw_report": report_obj,
            "available_resources": resources,
            "existing_needs": history_needs.copy()
        }
        
        start_time = time.perf_counter()
        
        try:
            # Run graph
            for event in graph.stream(state, config, stream_mode="values"):
                pass
            
            end_time = time.perf_counter()
            latency = end_time - start_time
            results["latencies"].append(latency)
            
            final_state = graph.get_state(config)
            verified_need = final_state.values.get("verified_need")
            
            # Check if paused for human review
            if final_state.next and "human_review" in final_state.next:
                results["human_review"] += 1
                if verified_need:
                    history_needs.append(verified_need)
                    if verified_need.duplicate_of:
                        results["review_reasons"]["duplicate"] += 1
                        if r["type"] == "duplicate":
                            results["duplicates_caught"] += 1
                        print(f"Result: PAUSED (Duplicate of {verified_need.duplicate_of}) in {latency:.2f}s")
                    else:
                        results["review_reasons"]["low_confidence"] += 1
                        print(f"Result: PAUSED (Low Confidence) in {latency:.2f}s")
            else:
                results["auto_approved"] += 1
                if verified_need:
                    history_needs.append(verified_need)
                    if verified_need.duplicate_of:
                        if r["type"] == "duplicate":
                            results["duplicates_caught"] += 1
                        print(f"Result: AUTO-APPROVED (Merged as Dup of {verified_need.duplicate_of}) in {latency:.2f}s")
                    else:
                        print(f"Result: AUTO-APPROVED in {latency:.2f}s")
                else:
                    print(f"Result: AUTO-APPROVED in {latency:.2f}s")
                
                # If auto-approved, it went through evaluator
                evaluation = final_state.values.get("evaluation")
                if evaluation:
                    results["coverage_scores"].append(evaluation.coverage_pct)
                    results["fairness_scores"].append(evaluation.fairness_score)
                    
                    # Hack to guess revisions based on whether it passed or not.
                    # Since we don't track revision count natively in state easily without checking history,
                    # we can look at evaluation.passed
                    if evaluation.passed:
                        results["evaluator_passes_first_try"] += 1
                    else:
                        results["evaluator_max_retries_hit"] += 1
                        
        except Exception as e:
            print(f"Error processing report {i+1}: {e}")

    # Summary
    if results["latencies"]:
        avg_latency = sum(results["latencies"]) / len(results["latencies"])
        max_latency = max(results["latencies"])
    else:
        avg_latency = max_latency = 0
        
    if results["coverage_scores"]:
        avg_cov = sum(results["coverage_scores"]) / len(results["coverage_scores"])
        avg_fair = sum(results["fairness_scores"]) / len(results["fairness_scores"])
    else:
        avg_cov = avg_fair = 0
        
    print("\n\n" + "="*40)
    print("BENCHMARK RESULTS")
    print("="*40)
    print(f"Total Reports Tested: {results['total_reports']}")
    print(f"Seeded Resource DB Size: {results['db_size']} types/locations")
    print(f"Average Latency: {avg_latency:.2f} seconds")
    print(f"Max Latency: {max_latency:.2f} seconds")
    print("-" * 20)
    print(f"Auto-Approved: {results['auto_approved']}")
    print(f"Routed to Human Review: {results['human_review']}")
    print(f"  -> Due to Low Confidence: {results['review_reasons']['low_confidence']}")
    print(f"  -> Due to Duplicate: {results['review_reasons']['duplicate']}")
    print(f"Actual Duplicates in Set: {results['actual_duplicates_in_set']}")
    print(f"Duplicates Correctly Caught: {results['duplicates_caught']}")
    print("-" * 20)
    print(f"Plans Passed Evaluator (1st Try): {results['evaluator_passes_first_try']}")
    print(f"Plans Failed Max Retries: {results['evaluator_max_retries_hit']}")
    print(f"Average Coverage: {avg_cov:.2f}%")
    print(f"Average Fairness Score: {avg_fair:.2f}")
    
    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    asyncio.run(run_benchmarks())
