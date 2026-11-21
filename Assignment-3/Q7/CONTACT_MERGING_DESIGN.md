# ASSIGNMENT 3 - Q7: CONTACT-MERGING PROGRAM DESIGN FROM FIRST PRINCIPLES

---

## Stage 1: Interpret the Problem (2 Marks)
1. **Inputs**: Raw contact records imported from diverse devices (SIM card, Phone A, Phone B), each containing messy names, phone numbers, and optional email addresses.
2. **Output**: A unified master contact directory where each distinct human entity appears exactly once, consolidating all associated phone numbers (in E.164 canonical format) and email addresses (in lowercase), with the cleanest title/name preserved.
3. **Equivalence Rules**:
   - Two records represent the **same individual** if they share at least one identical 10-digit normalized phone number OR one identical normalized email address.
   - Names alone do not guarantee identity (e.g. two distinct individuals can both be named "Suresh Kumar"), whereas mobile numbers and email addresses are globally unique identifiers.
4. **Data Structures Selected**:
   - `dict`: Core registry mapping canonical contact identifiers to unified person profiles.
   - `set`: Collects distinct phone numbers and emails per person to automatically eliminate intra-contact duplicates.
   - `list`: Maintains input queues and deterministic output sorting.

---

## Stage 2: Algorithmic Design & Pseudocode (3 Marks)

### Normalisation Rules:
1. **Phone Normalisation**:
   - Strip all non-digit characters (spaces, hyphens, parentheses, plus signs).
   - If length $> 10$ and starts with country code `91` or trunk prefix `0`, strip down to the base 10-digit national number.
2. **Name Canonicalisation**:
   - Strip whitespace, normalize honorific abbreviations (`Dr.`, `Prof.`), convert to `title()` case.
3. **Email Normalisation**:
   - Strip whitespace and convert to `lower()`.

### Standardized Pseudocode:
```text
ALGORITHM MergeContacts(raw_contact_list)
START
    SET master_records TO empty list
    SET phone_to_person_id TO empty dictionary
    SET email_to_person_id TO empty dictionary

    FOR each raw_record IN raw_contact_list DO
        SET clean_name TO CANONICALISE_NAME(raw_record.name)
        SET clean_phones TO SET OF NORMALISED_PHONES(raw_record.phones)
        SET clean_emails TO SET OF NORMALISED_EMAILS(raw_record.emails)

        SET matched_id TO NULL

        // Check Phone Match
        FOR each p IN clean_phones DO
            IF p IN phone_to_person_id THEN
                SET matched_id TO phone_to_person_id[p]
                BREAK
            ENDIF
        ENDFOR

        // Check Email Match if not matched by phone
        IF matched_id IS NULL THEN
            FOR each e IN clean_emails DO
                IF e IN email_to_person_id THEN
                    SET matched_id TO email_to_person_id[e]
                    BREAK
                ENDIF
            ENDFOR
        ENDIF

        IF matched_id IS NOT NULL THEN
            // Merge into existing entity
            MERGE raw_record INTO master_records[matched_id]
        ELSE
            // Create new person profile
            SET new_id TO LENGTH(master_records)
            ADD new profile TO master_records
            SET matched_id TO new_id
        ENDIF

        // Update secondary indices
        FOR each p IN clean_phones DO
            SET phone_to_person_id[p] TO matched_id
        ENDFOR
        FOR each e IN clean_emails DO
            SET email_to_person_id[e] TO matched_id
        ENDFOR
    ENDFOR

    RETURN master_records
END
```

---

## Stage 3 & 4: Implementation, Measurement & Defense
See `contact_merging.py` for execution across duplicate records, missing fields, hand-trace validation, and $O(n)$ hash mapping vs $O(n^2)$ pairwise comparison benchmarks.
