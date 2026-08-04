#!/usr/bin/env python3
"""
Task 002 Validation Script

Validates Gate 2 design deliverables for the First Vertical Scenario.
Uses only Python standard library. Returns 0 only when all required
design artifacts pass validation.

Validation Scope:
- Required documents exist and have correct structure
- State schema is valid JSON Schema and contains only required fields
- Document cross-references are consistent
- Design constraints from Task Contract are enforced
- Gate 1 limitations are acknowledged
- PER-STEP validation: each of 6 steps has entry/exit criteria within its own text range
"""

import json
import re
import sys
from pathlib import Path


def read_file(filepath):
    """Read file content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"ERROR: Failed to read {filepath}: {e}", file=sys.stderr)
        return None


def validate_json_file(filepath):
    """Validate JSON file syntax."""
    content = read_file(filepath)
    if content is None:
        return False
    try:
        json.loads(content)
        return True
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {filepath}: {e}", file=sys.stderr)
        return False


def validate_markdown_structure(filepath, required_headers):
    """Validate markdown file has required top-level headers."""
    content = read_file(filepath)
    if content is None:
        return False

    # Extract all headers
    headers = re.findall(r'^#+ (.+)$', content, re.MULTILINE)

    missing = []
    for required in required_headers:
        if not any(required.lower() in h.lower() for h in headers):
            missing.append(required)

    if missing:
        print(f"ERROR: {filepath} missing required sections: {missing}", file=sys.stderr)
        return False

    return True


def extract_step_sections(content):
    """Extract individual step sections from scenario document."""
    # Find all step headings and their positions
    step_pattern = r'### Step (\d+): (.+?)$'
    step_matches = list(re.finditer(step_pattern, content, re.MULTILINE))

    if len(step_matches) != 6:
        return None

    steps = {}
    for i, match in enumerate(step_matches):
        step_num = int(match.group(1))
        step_title = match.group(2)
        step_start = match.start()

        # End of this step is the start of next step, or end of flow section
        if i < len(step_matches) - 1:
            step_end = step_matches[i + 1].start()
        else:
            # Find "Complete Flow Summary" section which follows Step 6
            summary_match = re.search(r'^## Complete Flow Summary', content[step_start:], re.MULTILINE)
            if summary_match:
                step_end = step_start + summary_match.start()
            else:
                step_end = len(content)

        steps[step_num] = {
            'title': step_title,
            'content': content[step_start:step_end]
        }

    return steps


def validate_step_criteria(step_num, step_data):
    """Validate that a specific step has all required sections within its text range."""
    content = step_data['content']
    title = step_data['title']

    errors = []

    # Check for Entry Criteria section
    if '**Entry Criteria**' not in content and '**Entry Criteria:**' not in content:
        errors.append(f"Step {step_num} ({title}) missing Entry Criteria section")

    # Check for Exit Criteria section
    if '**Exit Criteria**' not in content and '**Exit Criteria:**' not in content:
        errors.append(f"Step {step_num} ({title}) missing Exit Criteria section")

    # Check for Recovery Behavior section
    if '**Recovery Behavior**' not in content and '**Recovery Behavior:**' not in content:
        errors.append(f"Step {step_num} ({title}) missing Recovery Behavior section")

    # Check for Evidence Collection section
    if '**Evidence Collection**' not in content and '**Evidence Collection:**' not in content:
        errors.append(f"Step {step_num} ({title}) missing Evidence Collection section")

    # Check for Success Criterion (at least mentioned)
    if '**Success Criterion**' not in content and '**Success Criteria**' not in content:
        # This is optional per step, but at least one step should have it
        pass

    return errors


def validate_scenario_document():
    """Validate FIRST_VERTICAL_SCENARIO.md structure and content."""
    print("Validating FIRST_VERTICAL_SCENARIO.md...")

    filepath = Path(__file__).parent.parent / 'docs' / 'FIRST_VERTICAL_SCENARIO.md'

    required_sections = [
        'Scenario Identity',
        'Actor',
        'Real-Material Input',
        'Preconditions',
        'Complete Step-by-Step Flow',
        'Measurable Success Criteria',
        'Failure States',
        'Explicit Non-Goals',
        'Design Assumptions and Limitations'
    ]

    if not validate_markdown_structure(filepath, required_sections):
        return False

    content = read_file(filepath)
    if content is None:
        return False

    # Extract individual step sections
    steps = extract_step_sections(content)
    if steps is None:
        print(f"ERROR: Could not extract 6 flow steps", file=sys.stderr)
        return False

    # Validate each step independently
    all_errors = []
    for step_num in range(1, 7):
        step_errors = validate_step_criteria(step_num, steps[step_num])
        all_errors.extend(step_errors)

    if all_errors:
        for error in all_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return False

    # Check Gate 1 limitations acknowledged
    if 'Limitations Carried Forward from Gate 1' not in content:
        print("ERROR: Gate 1 limitations not acknowledged", file=sys.stderr)
        return False

    # Check source grounding constraints mentioned
    if 'src-001' not in content or 'src-002' not in content:
        print("ERROR: Source grounding constraints not referenced", file=sys.stderr)
        return False

    print("✓ FIRST_VERTICAL_SCENARIO.md validated (including per-step criteria)")
    return True


def validate_decision_tree_document():
    """Validate PEDAGOGICAL_ACTION_DECISION_TREE.md structure and content."""
    print("Validating PEDAGOGICAL_ACTION_DECISION_TREE.md...")

    filepath = Path(__file__).parent.parent / 'docs' / 'PEDAGOGICAL_ACTION_DECISION_TREE.md'

    required_sections = [
        'Purpose',
        'Decision Tree Structure',
        'Decision Rules',
        'Evidence Boundaries',
        'Limitations and Assumptions',
        'Validation Criteria'
    ]

    if not validate_markdown_structure(filepath, required_sections):
        return False

    content = read_file(filepath)
    if content is None:
        return False

    # Check six classification types defined
    classifications = [
        'terminology_gap',
        'prerequisite_deficit',
        'procedural_confusion',
        'conceptual_confusion',
        'stuck_on_specific_step',
        'lost_context'
    ]

    for classification in classifications:
        if classification not in content:
            print(f"ERROR: Classification type '{classification}' not defined", file=sys.stderr)
            return False

    # Check six action types defined
    actions = [
        'Clarify Terminology',
        'Restore Prerequisite',
        'Give Bounded Example',
        'Request Explanation',
        'Request Fresh Attempt',
        'Stop and Request More Material'
    ]

    for action in actions:
        if action not in content:
            print(f"ERROR: Action type '{action}' not defined", file=sys.stderr)
            return False

    # Check provisional status acknowledged
    if 'provisional' not in content.lower() and 'PROVISIONAL' not in content:
        print("ERROR: Provisional status not acknowledged", file=sys.stderr)
        return False

    # Check automatic detection limitation acknowledged
    if 'does NOT automatically detect' not in content and 'does not automatically detect' not in content:
        print("ERROR: Automatic detection limitation not acknowledged", file=sys.stderr)
        return False

    # Check material_scope_status handling
    if 'material_scope_status' not in content and 'outside_supplied_corpus' not in content:
        print("ERROR: Material scope status handling not documented", file=sys.stderr)
        return False

    # Check cannot_articulate handling
    if 'cannot_articulate' not in content:
        print("ERROR: Cannot-articulate case not documented", file=sys.stderr)
        return False

    print("✓ PEDAGOGICAL_ACTION_DECISION_TREE.md validated")
    return True


def validate_state_schema():
    """Validate MINIMAL_LEARNING_STATE.schema.json structure and constraints."""
    print("Validating MINIMAL_LEARNING_STATE.schema.json...")

    filepath = Path(__file__).parent.parent / 'templates' / 'MINIMAL_LEARNING_STATE.schema.json'

    if not validate_json_file(filepath):
        return False

    content = read_file(filepath)
    schema = json.loads(content)

    # Check required top-level fields
    required_fields = [
        'schema_version',
        'scenario_id',
        'session_id',
        'created_at',
        'updated_at',
        'current_position',
        'task_boundary',
        'observed_difficulty',
        'last_pedagogical_action',
        'independent_check',
        'next_action'
    ]

    schema_required = schema.get('required', [])
    missing = [f for f in required_fields if f not in schema_required]

    if missing:
        print(f"ERROR: Schema missing required fields: {missing}", file=sys.stderr)
        return False

    # Check evidence_level enum is 0, 1, 2 (not 3 or higher)
    independent_check = schema.get('properties', {}).get('independent_check', {})
    evidence_level = independent_check.get('properties', {}).get('evidence_level', {})
    evidence_enum = evidence_level.get('enum', [])

    if evidence_enum != [0, 1, 2]:
        print(f"ERROR: evidence_level enum must be [0, 1, 2], got {evidence_enum}", file=sys.stderr)
        return False

    # Check additionalProperties is false at top level
    if schema.get('additionalProperties') is not False:
        print("ERROR: Schema must set additionalProperties: false at top level", file=sys.stderr)
        return False

    # Check nested objects have additionalProperties: false
    nested_objects = ['current_position', 'task_boundary', 'observed_difficulty',
                      'last_pedagogical_action', 'independent_check', 'next_action']

    for obj_name in nested_objects:
        obj_schema = schema.get('properties', {}).get(obj_name, {})
        if obj_schema.get('type') == 'object':
            if obj_schema.get('additionalProperties') is not False:
                print(f"ERROR: Nested object '{obj_name}' must set additionalProperties: false", file=sys.stderr)
                return False

    # Check scenario_id is constrained to this scenario
    scenario_id_prop = schema.get('properties', {}).get('scenario_id', {})
    expected_scenario = 'source-grounded-learning-recovery-and-independent-completion-check'
    if scenario_id_prop.get('const') != expected_scenario:
        print(f"ERROR: scenario_id must be constrained to '{expected_scenario}'", file=sys.stderr)
        return False

    # Check source-grounded actions require citations
    last_action = schema.get('properties', {}).get('last_pedagogical_action', {})
    action_props = last_action.get('properties', {})
    action_type_prop = action_props.get('action_type', {})
    citations_prop = action_props.get('material_citations', {})

    # material_citations should exist
    if 'material_citations' not in action_props:
        print("ERROR: last_pedagogical_action missing material_citations field", file=sys.stderr)
        return False

    # STRUCTURAL CHECK: obstacle_classification enum exactly 6 + null
    observed_difficulty = schema.get('properties', {}).get('observed_difficulty', {})
    obstacle_props = observed_difficulty.get('properties', {}).get('obstacle_classification', {})
    obstacle_enum = obstacle_props.get('enum', [])
    
    expected_obstacles = [
        'terminology_gap',
        'prerequisite_deficit',
        'procedural_confusion',
        'conceptual_confusion',
        'stuck_on_specific_step',
        'lost_context',
        None
    ]
    
    if set(obstacle_enum) != set(expected_obstacles):
        print(f"ERROR: obstacle_classification enum must be exactly 6 strings + null, got {obstacle_enum}", file=sys.stderr)
        return False
    
    # Check cannot_articulate is NOT in obstacle enum
    if 'cannot_articulate' in obstacle_enum:
        print("ERROR: cannot_articulate must not be in obstacle_classification enum", file=sys.stderr)
        return False
    
    # Check obsolete outside_corpus is absent
    if 'outside_corpus' in observed_difficulty.get('properties', {}):
        print("ERROR: obsolete outside_corpus field must not exist", file=sys.stderr)
        return False
    
    # STRUCTURAL CHECK: material_scope_status exactly 3 values
    material_scope = observed_difficulty.get('properties', {}).get('material_scope_status', {})
    material_scope_enum = material_scope.get('enum', [])
    expected_scope = ['in_scope', 'missing_required_material', 'outside_supplied_corpus']
    
    if set(material_scope_enum) != set(expected_scope):
        print(f"ERROR: material_scope_status enum must be exactly {expected_scope}, got {material_scope_enum}", file=sys.stderr)
        return False
    
    # STRUCTURAL CHECK: articulation_status exactly 2 values
    articulation = observed_difficulty.get('properties', {}).get('articulation_status', {})
    articulation_enum = articulation.get('enum', [])
    expected_articulation = ['articulated', 'cannot_articulate']
    
    if set(articulation_enum) != set(expected_articulation):
        print(f"ERROR: articulation_status enum must be exactly {expected_articulation}, got {articulation_enum}", file=sys.stderr)
        return False
    
    # STRUCTURAL CHECK: All nested objects with additionalProperties: false
    def check_nested_additional_props(obj, path="root"):
        if isinstance(obj, dict):
            if obj.get('type') == 'object' and 'properties' in obj:
                if obj.get('additionalProperties') is not False:
                    print(f"ERROR: Nested object at {path} missing additionalProperties: false", file=sys.stderr)
                    return False
                for prop_name, prop_schema in obj.get('properties', {}).items():
                    if not check_nested_additional_props(prop_schema, f"{path}.{prop_name}"):
                        return False
            elif 'items' in obj:
                if not check_nested_additional_props(obj['items'], f"{path}[]"):
                    return False
        return True
    
    if not check_nested_additional_props(schema):
        return False
    
    # STRUCTURAL CHECK: Nullable enums include null
    def check_nullable_enums(obj, path="root"):
        if isinstance(obj, dict):
            if 'type' in obj and 'enum' in obj:
                types = obj['type'] if isinstance(obj['type'], list) else [obj['type']]
                if 'null' in types or ['string', 'null'] == obj['type'] or ['integer', 'null'] == obj['type']:
                    if None not in obj['enum'] and 'null' not in obj['enum']:
                        print(f"ERROR: Nullable field at {path} has enum without null: {obj['enum']}", file=sys.stderr)
                        return False
            if 'properties' in obj:
                for prop_name, prop_schema in obj['properties'].items():
                    if not check_nullable_enums(prop_schema, f"{path}.{prop_name}"):
                        return False
            if 'items' in obj:
                if not check_nullable_enums(obj['items'], f"{path}[]"):
                    return False
        return True
    
    if not check_nullable_enums(schema):
        return False
    
    # STRUCTURAL CHECK: Draft-07 citation condition exists
    if 'if' not in last_action or 'then' not in last_action:
        print("ERROR: last_pedagogical_action missing Draft-07 if/then citation constraints", file=sys.stderr)
        return False
    
    # Check five source-grounded actions require minItems >= 1
    source_grounded_actions = [
        'clarify_terminology',
        'restore_prerequisite',
        'give_bounded_example',
        'request_explanation',
        'request_fresh_attempt'
    ]
    
    if_clause = last_action.get('if', {})
    action_enum_in_if = if_clause.get('properties', {}).get('action_type', {}).get('enum', [])
    
    if set(action_enum_in_if) != set(source_grounded_actions):
        print(f"ERROR: if clause must check exactly these 5 actions: {source_grounded_actions}, got {action_enum_in_if}", file=sys.stderr)
        return False
    
    then_clause = last_action.get('then', {})
    citations_min = then_clause.get('properties', {}).get('material_citations', {}).get('minItems', 0)
    
    if citations_min < 1:
        print(f"ERROR: then clause must require minItems >= 1 for citations, got {citations_min}", file=sys.stderr)
        return False

    # Check no knowledge_graph, mastery_estimate, or similar speculative fields
    prohibited_keywords = ['knowledge_graph', 'mastery_estimate', 'skill_decomposition', 'cross_domain']
    schema_str = json.dumps(schema).lower()

    found_prohibited = [kw for kw in prohibited_keywords if kw in schema_str]
    if found_prohibited:
        print(f"ERROR: Schema contains prohibited speculative fields: {found_prohibited}", file=sys.stderr)
        return False

    print("✓ MINIMAL_LEARNING_STATE.schema.json validated")
    return True


def validate_cross_references():
    """Validate cross-references between documents are consistent."""
    print("Validating cross-document consistency...")

    scenario_file = Path(__file__).parent.parent / 'docs' / 'FIRST_VERTICAL_SCENARIO.md'
    tree_file = Path(__file__).parent.parent / 'docs' / 'PEDAGOGICAL_ACTION_DECISION_TREE.md'

    scenario_content = read_file(scenario_file)
    tree_content = read_file(tree_file)

    if scenario_content is None or tree_content is None:
        return False

    # Check scenario references decision tree
    if 'PEDAGOGICAL_ACTION_DECISION_TREE.md' not in scenario_content:
        print("ERROR: Scenario does not reference decision tree document", file=sys.stderr)
        return False

    # Check scenario references state schema
    if 'MINIMAL_LEARNING_STATE.schema.json' not in scenario_content:
        print("ERROR: Scenario does not reference state schema", file=sys.stderr)
        return False

    # Check both documents reference Gate 1 limitations
    if 'Gate 1' not in scenario_content or 'Gate 1' not in tree_content:
        print("ERROR: Documents do not reference Gate 1 limitations", file=sys.stderr)
        return False

    # Check consistent classification type count (6 types)
    scenario_classifications = len(re.findall(r'(terminology_gap|prerequisite_deficit|procedural_confusion|conceptual_confusion|stuck_on_specific_step|lost_context)', scenario_content))
    tree_classifications = len(re.findall(r'(terminology_gap|prerequisite_deficit|procedural_confusion|conceptual_confusion|stuck_on_specific_step|lost_context)', tree_content))

    # Both documents should mention these classifications multiple times
    if scenario_classifications < 6 or tree_classifications < 6:
        print(f"ERROR: Inconsistent classification references (scenario: {scenario_classifications}, tree: {tree_classifications})", file=sys.stderr)
        return False

    print("✓ Cross-document consistency validated")
    return True


def validate_design_constraints():
    """Validate Task Contract design constraints are enforced."""
    print("Validating design constraint enforcement...")

    scenario_file = Path(__file__).parent.parent / 'docs' / 'FIRST_VERTICAL_SCENARIO.md'
    scenario_content = read_file(scenario_file)

    if scenario_content is None:
        return False

    # Check prohibited activities are explicitly called out
    prohibited = [
        'frontend',
        'multi-agent',
        'automatic mastery',
        'knowledge graph',
        'review scheduler'
    ]

    non_goals_section = scenario_content[scenario_content.find('Explicit Non-Goals'):] if 'Explicit Non-Goals' in scenario_content else ""

    for prohibited_item in prohibited:
        if prohibited_item.lower() not in non_goals_section.lower():
            print(f"WARNING: Prohibited activity '{prohibited_item}' not explicitly called out in non-goals", file=sys.stderr)
            # Warning only, not failure

    # Check source grounding constraint enforced
    if 'cite uploaded material' not in scenario_content.lower() and 'source-bounded' not in scenario_content.lower():
        print("ERROR: Source grounding constraint not enforced in scenario", file=sys.stderr)
        return False

    # Check single scenario scope
    if 'multiple scenarios' in scenario_content.lower() and 'NOT' in scenario_content:
        pass  # Correctly states NOT multiple scenarios
    else:
        print("ERROR: Single scenario scope not clearly stated", file=sys.stderr)
        return False

    print("✓ Design constraints validated")
    return True


def main():
    """Run all validations."""
    print("=== Task 002 Gate 2 Design Validation ===\n")

    repo_root = Path(__file__).parent.parent

    # Check required files exist
    required_files = [
        repo_root / 'docs' / 'FIRST_VERTICAL_SCENARIO.md',
        repo_root / 'docs' / 'PEDAGOGICAL_ACTION_DECISION_TREE.md',
        repo_root / 'templates' / 'MINIMAL_LEARNING_STATE.schema.json',
    ]

    for filepath in required_files:
        if not filepath.exists():
            print(f"ERROR: Required file missing: {filepath}", file=sys.stderr)
            return 1

    # Run validation checks
    checks = [
        validate_scenario_document,
        validate_decision_tree_document,
        validate_state_schema,
        validate_cross_references,
        validate_design_constraints,
    ]

    passed = 0
    failed = 0

    for check in checks:
        try:
            if check():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"ERROR: Validation check failed with exception: {e}", file=sys.stderr)
            failed += 1

    print(f"\n=== Validation Summary ===")
    print(f"Checks passed: {passed}/{len(checks)}")
    print(f"Checks failed: {failed}/{len(checks)}")

    if failed == 0:
        print("\n✓ All Task 002 Gate 2 design validations passed")
        return 0
    else:
        print(f"\n✗ {failed} validation check(s) failed", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
