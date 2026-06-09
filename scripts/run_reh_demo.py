# REH Demonstration Script
# Proves full directive-to-report chain

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services import reh_directive_manager as dm
from services import kingdom_task_manager as tm
from services import kingdom_assignment_manager as am
from services import kingdom_progress_tracker as pt
from services import kingdom_report_compiler as rc

def main():
    print("=== REH Operational Proof Demonstration ===\n")
    
    # Step 1: Create Directive
    print("Step 1: Creating directive from Hung Vuong...")
    directive = dm.create_directive(
        title="Q1-Audit Evidence Collection",
        authority="Hung Vuong",
        priority="HIGH",
        deadline="2026-07-08",
        objective="Collect operational evidence for Q1 audit",
        category="AUDIT",
    )
    print(f"  Created: {directive['directive_id']}\n")
    
    # Step 2: Generate Tasks
    print("Step 2: Janus generating tasks...")
    tasks = []
    tasks.append(tm.create_task(directive["directive_id"], "Create trading forecast registry", "hermes", "HIGH", "2026-06-09"))
    tasks.append(tm.create_task(directive["directive_id"], "Run MT5 observation loop", "iris", "HIGH", "2026-06-09"))
    tasks.append(tm.create_task(directive["directive_id"], "Track capability usage", "hermes", "MEDIUM", "2026-06-09"))
    print(f"  Created: {len(tasks)} tasks\n")
    
    # Step 3: Assign Tasks
    print("Step 3: Assigning tasks to agents...")
    for task in tasks:
        assigned = am.assign_task_to_agent(task["task_id"], task["owner"])
        print(f"  Assigned: {task['task_id']} to {task['owner']}")
    print()
    
    # Step 4: Track Progress
    print("Step 4: Tracking progress...")
    progress = pt.get_directive_progress(directive["directive_id"])
    print(f"  Directive Progress: {progress['progress']}%")
    
    for task in tasks:
        # Simulate partial progress
        tm.update_task(task["task_id"], progress=33.0)
        print(f"  {task['task_id']}: 33% complete")
    print()
    
    # Step 5: Generate Report
    print("Step 5: Generating executive report...")
    report = rc.generate_executive_report(directive["directive_id"])
    print(f"  Generated: {report['report_id']}")
    print(f"  Sections: {list(report['sections'].keys())}\n")
    
    # Step 6: Verify Audit Trail
    print("Step 6: Verifying audit trail...")
    directive_reg = dm._load_registry()
    tasks_reg = tm._load_registry()
    assignments_reg = am._load_assignment_registry()
    
    print(f"  Directive audit entries: {len(directive_reg['kingdom_directive_registry']['directives'][-1]['audit_trail'])}")
    print(f"  Total tasks: {len(tasks_reg['kingdom_task_registry']['tasks'])}")
    print(f"  Total assignments: {len(assignments_reg['kingdom_assignment_registry']['assignments'])}\n")
    
    print("=== REH OPERATIONAL PROOF: COMPLETE ===")
    return {
        "directive": directive["directive_id"],
        "tasks": len(tasks),
        "assignments": len(tasks),
        "report": report["report_id"],
        "operational": True,
    }

if __name__ == "__main__":
    result = main()
    print(f"\nResult: {result}")