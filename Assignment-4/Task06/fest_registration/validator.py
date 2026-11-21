"""
Module validator.py: Handles string validation without regular expressions.
"""

def validate_email_string(email_str):
    """
    Validates an email address using string operations only:
    - Must not have spaces
    - Exactly one '@' character
    - User and domain parts must be non-empty
    - Domain part must contain at least one '.' with valid suffix
    """
    if not email_str or not isinstance(email_str, str):
        return False, "Empty or non-string email"
    
    clean = email_str.strip()
    if " " in clean:
        return False, "Email contains whitespace"
    
    if clean.count("@") != 1:
        return False, "Email must contain exactly one '@'"
    
    user, domain = clean.split("@")
    if not user:
        return False, "Missing username part before '@'"
    if not domain:
        return False, "Missing domain part after '@'"
    
    if "." not in domain:
        return False, "Domain part must contain at least one '.'"
    
    domain_parts = domain.split(".")
    if any(not part for part in domain_parts):
        return False, "Domain contains consecutive or trailing dots"
    
    # Suffix check (e.g. .edu, .com, .in)
    if len(domain_parts[-1]) < 2:
        return False, "Domain suffix too short"
    
    return True, clean.lower()

def validate_registration_line(line_text):
    """
    Validates a raw CSV line from department registration files:
    Format: register_no,name,department,email,events (semicolon separated)
    """
    line = line_text.strip()
    if not line:
        return False, None, "Empty line"
    
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 5:
        return False, None, f"Expected 5 comma-separated fields, found {len(parts)}"
    
    reg_no, name, dept, email_raw, events_raw = parts
    
    if not reg_no or not reg_no.isalnum():
        return False, None, f"Invalid register number: '{reg_no}'"
    if not name:
        return False, None, "Name cannot be empty"
    if not dept:
        return False, None, "Department cannot be empty"
    
    is_valid_email, email_res = validate_email_string(email_raw)
    if not is_valid_email:
        return False, None, f"Invalid email '{email_raw}': {email_res}"
    
    # Split events by semicolon
    events = [e.strip() for e in events_raw.split(";") if e.strip()]
    if not events:
        return False, None, "No events selected"
    
    record = {
        "reg_no": reg_no.upper(),
        "name": name.title(),
        "department": dept.upper(),
        "email": email_res,
        "events": events
    }
    return True, record, "Valid"
