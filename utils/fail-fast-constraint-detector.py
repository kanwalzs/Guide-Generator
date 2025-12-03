#!/usr/bin/env python
"""
Fail-Fast Template Constraint Detector
Analyzes feature requirements and fails immediately if constraints are violated
"""

import re
import sys

class TemplateConstraintError(Exception):
    """Exception raised when template constraints are violated"""
    pass

def analyze_feature_requirements(feature_description):
    """Analyze feature description for constraint violations"""
    
    # Features that cannot work in learning environment
    forbidden_features = [
        (r'database.*replication', 'Database Replication', 'requires account-level privileges and multiple accounts'),
        (r'account.*replication', 'Account Replication', 'requires account-level privileges and multiple accounts'),
        (r'data.*shar(e|ing)', 'Data Sharing', 'requires account-level privileges and external accounts'),
        (r'external.*stage', 'External Stages', 'requires storage integrations not available in learning environment'),
        (r'storage.*integration', 'Storage Integration', 'requires external cloud storage setup'),
        (r'notification.*integration', 'Notification Integration', 'requires external service integrations'),
        (r'warehouse.*management', 'Warehouse Management', 'requires account-level warehouse privileges'),
        (r'role.*management', 'Role Management', 'requires account-level security privileges'),
        (r'user.*management', 'User Management', 'requires account-level user administration'),
        (r'account.*parameter', 'Account Parameters', 'requires account-level configuration privileges'),
        (r'cross.*account', 'Cross-Account Operations', 'requires multiple Snowflake accounts'),
        (r'multi.*account', 'Multi-Account Setup', 'requires multiple Snowflake accounts'),
        (r'failover', 'Failover/Disaster Recovery', 'typically requires cross-account or cross-region setup'),
        (r'disaster.*recovery', 'Disaster Recovery', 'typically requires cross-account or cross-region setup'),
    ]
    
    violations = []
    
    for pattern, feature_name, reason in forbidden_features:
        if re.search(pattern, feature_description, re.IGNORECASE):
            violations.append({
                'feature': feature_name,
                'reason': reason,
                'pattern': pattern
            })
    
    return violations

def generate_failure_report(violations, feature_description):
    """Generate detailed failure report with alternatives"""
    
    report = []
    report.append("=" * 70)
    report.append("TEMPLATE GENERATION FAILED: Learning Environment Constraints")
    report.append("=" * 70)
    report.append("")
    report.append("REQUESTED FEATURE: " + feature_description)
    report.append("")
    
    report.append("DETECTED CONSTRAINT VIOLATIONS:")
    for violation in violations:
        report.append("- " + violation['feature'] + ": " + violation['reason'])
    report.append("")
    
    report.append("WHY THIS FAILS:")
    report.append("The Snowflake Learning Environment has restricted privileges that only")
    report.append("allow schema-level operations within a single account. Features requiring")
    report.append("account-level privileges, external integrations, or multiple accounts")
    report.append("cannot be demonstrated meaningfully.")
    report.append("")
    
    # Suggest alternatives based on violation types
    alternatives = get_alternative_suggestions(violations)
    if alternatives:
        report.append("SUGGESTED ALTERNATIVE FEATURES:")
        for alt in alternatives:
            report.append("- " + alt)
        report.append("")
    
    report.append("LEARNING RESOURCES:")
    report.append("For production setup of this feature, refer to:")
    report.append("- Snowflake Documentation: https://docs.snowflake.com/")
    report.append("- Snowflake University: https://university.snowflake.com/")
    report.append("- Community Forums: https://community.snowflake.com/")
    report.append("")
    
    report.append("TEMPLATE DEVELOPMENT GUIDANCE:")
    report.append("Consider creating templates for features that:")
    report.append("- Work within schema-level constraints")
    report.append("- Use only learning environment privileges")
    report.append("- Require no external dependencies")
    report.append("- Can be completed in under 5 minutes")
    report.append("=" * 70)
    
    return "\n".join(report)

def get_alternative_suggestions(violations):
    """Suggest alternative features based on violation types"""
    
    alternatives = []
    
    # Map violation types to alternatives
    violation_features = [v['feature'] for v in violations]
    
    if any('Replication' in f or 'Disaster' in f or 'Failover' in f for f in violation_features):
        alternatives.extend([
            "Table cloning for data backup and recovery",
            "Time travel for historical data access",
            "Zero-copy cloning for data protection",
            "Incremental data loading patterns"
        ])
    
    if any('Sharing' in f for f in violation_features):
        alternatives.extend([
            "Secure views for data access control",
            "Row-level security within schemas", 
            "Dynamic data masking techniques",
            "Role-based access patterns"
        ])
    
    if any('Integration' in f or 'External' in f for f in violation_features):
        alternatives.extend([
            "Internal data transformation pipelines",
            "Semi-structured data processing (JSON/XML)",
            "File format handling and parsing",
            "Data quality validation techniques"
        ])
    
    if any('Management' in f or 'Account' in f for f in violation_features):
        alternatives.extend([
            "Query optimization and performance tuning",
            "Advanced SQL techniques and patterns",
            "Data modeling best practices",
            "Monitoring and observability within schemas"
        ])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_alternatives = []
    for alt in alternatives:
        if alt not in seen:
            seen.add(alt)
            unique_alternatives.append(alt)
    
    return unique_alternatives

def check_feature_compatibility(feature_description):
    """Main function to check if a feature can be templated"""
    
    violations = analyze_feature_requirements(feature_description)
    
    if violations:
        failure_report = generate_failure_report(violations, feature_description)
        raise TemplateConstraintError(failure_report)
    
    return True

def analyze_sql_code(sql_content):
    """Analyze SQL code for constraint violations (fallback check)"""
    
    error_patterns = [
        (r'CREATE\s+DATABASE\s+\w+', 'CREATE DATABASE operations not allowed'),
        (r'DROP\s+DATABASE\s+\w+', 'DROP DATABASE operations not allowed'),
        (r'ALTER\s+DATABASE\s+.*ENABLE\s+REPLICATION', 'Database replication requires account privileges'),
        (r'AS\s+REPLICA\s+OF\s+\w+\.\w+\.\w+', 'Cross-account replica creation not allowed'),
        (r'CREATE\s+WAREHOUSE\s+\w+', 'Warehouse creation not allowed'),
        (r'CREATE\s+ROLE\s+\w+', 'Role creation not allowed'),
        (r'CREATE\s+USER\s+\w+', 'User creation not allowed'),
        (r'CREATE\s+STORAGE\s+INTEGRATION', 'Storage integrations not allowed'),
        (r'ALTER\s+ACCOUNT\s+SET', 'Account parameter changes not allowed'),
    ]
    
    violations = []
    lines = sql_content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        line_content = line.strip()
        
        # Skip comments and empty lines
        if not line_content or line_content.startswith('--'):
            continue
            
        # Check for violations
        for pattern, message in error_patterns:
            if re.search(pattern, line_content, re.IGNORECASE):
                violations.append({
                    'line': line_num,
                    'content': line_content,
                    'message': message
                })
    
    return violations

def main():
    """Main function for command-line usage"""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python fail-fast-constraint-detector.py <feature_description>")
        print("  python fail-fast-constraint-detector.py --check-sql <sql_file>")
        sys.exit(1)
    
    if sys.argv[1] == "--check-sql" and len(sys.argv) == 3:
        # Check existing SQL file for violations
        try:
            with open(sys.argv[2], 'r') as f:
                sql_content = f.read()
            
            violations = analyze_sql_code(sql_content)
            
            if violations:
                print("SQL CONSTRAINT VIOLATIONS DETECTED:")
                print("=" * 50)
                for violation in violations:
                    print("Line " + str(violation['line']) + ": " + violation['message'])
                    print("  Code: " + violation['content'])
                    print("")
                sys.exit(1)
            else:
                print("No SQL constraint violations detected")
                
        except IOError:
            print("Error: Could not read file " + sys.argv[2])
            sys.exit(1)
    else:
        # Check feature description for compatibility
        feature_description = " ".join(sys.argv[1:])
        
        try:
            check_feature_compatibility(feature_description)
            print("FEATURE COMPATIBLE: Can proceed with template generation")
            print("Feature: " + feature_description)
        except TemplateConstraintError as e:
            print(str(e))
            sys.exit(1)

if __name__ == "__main__":
    main()
