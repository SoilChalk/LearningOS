#!/usr/bin/env python3
"""
Validate source ledger and individual source records against JSON schemas.
Returns 0 on success, nonzero on validation failure.
"""

import json
import sys
from pathlib import Path

def validate_source_ledger():
    """Validate source ledger structure and individual source records."""
    repo_root = Path(__file__).parent.parent
    ledger_path = repo_root / "sources" / "source-ledger.json"
    
    errors = []
    
    # Load ledger
    try:
        with open(ledger_path) as f:
            ledger = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to load source ledger: {e}", file=sys.stderr)
        return 1
    
    # Basic ledger structure validation
    required_ledger_fields = [
        "schema_version", "generated_at", "task_id", "status",
        "stage", "source_count", "target_minimum", "target_maximum", "sources"
    ]
    
    for field in required_ledger_fields:
        if field not in ledger:
            errors.append(f"Ledger missing required field: {field}")
    
    # Validate source count matches array length
    if "sources" in ledger and "source_count" in ledger:
        actual_count = len(ledger["sources"])
        declared_count = ledger["source_count"]
        if actual_count != declared_count:
            errors.append(
                f"Source count mismatch: declared {declared_count}, "
                f"but found {actual_count} sources"
            )
    
    # Validate each source record
    required_record_fields = [
        "id", "title", "organization_or_authors", "publication_date",
        "source_type", "url", "accessed_at", "research_question_ids",
        "directly_supported_observations", "design_implications",
        "limitations_and_non_inferences", "decision_affected",
        "verification_status"
    ]
    
    valid_source_types = [
        "product_documentation", "research_paper_survey",
        "research_paper_experiment", "research_paper_simulation",
        "research_paper_field_evaluation", "technical_report",
        "project_repository", "official_blog_post"
    ]
    
    valid_decisions = [
        "source_grounding_strategy", "course_boundary_enforcement",
        "pedagogical_action_selection", "evidence_collection",
        "learner_model_applicability", "first_scenario_scope",
        "state_schema_design", "anti_pattern_avoidance"
    ]
    
    for i, source in enumerate(ledger.get("sources", [])):
        source_id = source.get("id", f"source_{i}")
        
        # Check required fields
        for field in required_record_fields:
            if field not in source:
                errors.append(f"{source_id}: missing required field '{field}'")
        
        # Validate source_type
        if "source_type" in source:
            if source["source_type"] not in valid_source_types:
                errors.append(
                    f"{source_id}: invalid source_type '{source['source_type']}'"
                )
        
        # Validate decision_affected
        if "decision_affected" in source:
            for decision in source["decision_affected"]:
                if decision not in valid_decisions:
                    errors.append(
                        f"{source_id}: invalid decision '{decision}'"
                    )
        
        # Validate arrays are not empty
        array_fields = [
            "research_question_ids", "directly_supported_observations",
            "design_implications", "limitations_and_non_inferences",
            "decision_affected"
        ]
        for field in array_fields:
            if field in source:
                if not isinstance(source[field], list) or len(source[field]) == 0:
                    errors.append(f"{source_id}: '{field}' must be non-empty array")
        
        # Validate ID format
        if "id" in source:
            if not source["id"].startswith("src-"):
                errors.append(f"{source_id}: ID must start with 'src-'")
    
    # Report results
    if errors:
        print("VALIDATION FAILED:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    else:
        print("✓ Source ledger validation passed")
        print(f"✓ Ledger structure valid")
        print(f"✓ {len(ledger.get('sources', []))} source records validated")
        return 0

if __name__ == "__main__":
    sys.exit(validate_source_ledger())
