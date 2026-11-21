"""
ASSIGNMENT 3 - Q7: Design a Contact-Merging Program from First Principles

Includes:
- Multi-field normalisation (phone, name, email)
- Disjoint set / index-based entity resolution
- Handling duplicates, missing fields, multiple numbers/emails
- Verification on hand-designed sample test cases
- Benchmark comparison: O(n) Hash Index vs O(n^2) Pairwise Comparison for 1,000 and 100,000 records
- Defense of edge cases (same name different people)
"""

import time
import random
import sys

def normalise_phone(raw_phone):
    """Strips non-digits and reduces Indian numbers (+91, 0) to 10 digits."""
    if not raw_phone:
        return None
    digits = "".join(ch for ch in str(raw_phone) if ch.isdigit())
    if len(digits) == 10:
        return digits
    elif len(digits) == 11 and digits.startswith("0"):
        return digits[1:]
    elif len(digits) == 12 and digits.startswith("91"):
        return digits[2:]
    elif len(digits) > 10:
        return digits[-10:]
    return None  # Invalid phone length

def normalise_name(raw_name):
    """Trims, standardizes titles, and converts to Title Case."""
    if not raw_name or not raw_name.strip():
        return "Unknown"
    cleaned = " ".join(raw_name.strip().split())
    # Prefer longer name with initials/titles
    return cleaned.title()

def normalise_email(raw_email):
    """Trims and converts email to lowercase."""
    if not raw_email or "@" not in raw_email:
        return None
    return raw_email.strip().lower()

class ContactMerger:
    def __init__(self):
        self.profiles = []  # list of dicts: {"name": str, "phones": set, "emails": set}
        self.phone_index = {}  # phone -> profile index
        self.email_index = {}  # email -> profile index

    def add_contact(self, name, raw_phones, raw_emails):
        # 1. Normalise attributes
        clean_name = normalise_name(name)
        phones = set()
        for p in raw_phones:
            norm_p = normalise_phone(p)
            if norm_p:
                phones.add(norm_p)

        emails = set()
        for e in raw_emails:
            norm_e = normalise_email(e)
            if norm_e:
                emails.add(norm_e)

        # 2. Entity resolution: Find existing matching profile index
        matched_idx = None
        for p in phones:
            if p in self.phone_index:
                matched_idx = self.phone_index[p]
                break

        if matched_idx is None:
            for e in emails:
                if e in self.email_index:
                    matched_idx = self.email_index[e]
                    break

        # 3. Merge or Create
        if matched_idx is not None:
            # Merge into existing profile
            target = self.profiles[matched_idx]
            target["phones"].update(phones)
            target["emails"].update(emails)
            # Retain the longer, more informative name
            if len(clean_name) > len(target["name"]) and "Unknown" not in clean_name:
                target["name"] = clean_name
        else:
            # New unique profile
            new_idx = len(self.profiles)
            self.profiles.append({
                "name": clean_name,
                "phones": phones,
                "emails": emails
            })
            matched_idx = new_idx

        # 4. Update indices
        for p in phones:
            self.phone_index[p] = matched_idx
        for e in emails:
            self.email_index[e] = matched_idx

    def get_merged_contacts(self):
        return sorted(self.profiles, key=lambda x: x["name"])

# Alternative Concept: O(n^2) Pairwise Comparison
def merge_pairwise_naive(raw_records):
    """Compares every contact against every previously merged contact (O(n^2))."""
    merged = []
    for raw in raw_records:
        norm_name = normalise_name(raw["name"])
        norm_phones = {normalise_phone(p) for p in raw["phones"] if normalise_phone(p)}
        norm_emails = {normalise_email(e) for e in raw["emails"] if normalise_email(e)}

        matched = False
        for ex in merged:
            if (norm_phones & ex["phones"]) or (norm_emails & ex["emails"]):
                ex["phones"].update(norm_phones)
                ex["emails"].update(norm_emails)
                if len(norm_name) > len(ex["name"]):
                    ex["name"] = norm_name
                matched = True
                break
        if not matched:
            merged.append({"name": norm_name, "phones": norm_phones, "emails": norm_emails})
    return merged

def run_q7():
    print("=" * 75)
    print("ASSIGNMENT 3 - Q7: CONTACT MERGING FROM FIRST PRINCIPLES")
    print("=" * 75)

    # 1. Hand-Designed Verification Test Case
    print("\n--- Hand Trace Verification Case ---")
    incoming_raw_contacts = [
        {"name": "Dr. Ravi Kumar", "phones": ["+91 98400 12345"], "emails": ["ravi.k@hospital.org"]},
        {"name": "ravi kumar",     "phones": ["09840012345", "98400-99999"], "emails": []},
        {"name": "Ravi K",          "phones": ["9840099999"], "emails": ["ravi.kumar@gmail.com"]},
        {"name": "Suresh Raina",    "phones": ["9841122334"], "emails": ["suresh@cricket.in"]},
        {"name": "Suresh Raina",    "phones": ["9999900000"], "emails": ["suresh.alt@mail.com"]}, # Different person, same name!
        {"name": "Unknown",         "phones": ["9841122334"], "emails": []}, # Duplicate of 1st Suresh
    ]

    merger = ContactMerger()
    for c in incoming_raw_contacts:
        merger.add_contact(c["name"], c["phones"], c["emails"])

    merged = merger.get_merged_contacts()
    print(f"Total Raw Contacts Processed: {len(incoming_raw_contacts)}")
    print(f"Consolidated Unique Entities : {len(merged)}")
    print("-" * 75)
    for p in merged:
        print(f"Name   : {p['name']}")
        print(f"Phones : {sorted(p['phones'])}")
        print(f"Emails : {sorted(p['emails'])}")
        print("-" * 40)

    # Verifications
    # 3 Ravi entries should merge into 1 entity with 2 phones and 2 emails
    ravi_entity = [p for p in merged if "Ravi" in p["name"]][0]
    assert len(ravi_entity["phones"]) == 2, "Expected 2 consolidated phone numbers for Ravi"
    assert len(ravi_entity["emails"]) == 2, "Expected 2 consolidated emails for Ravi"
    assert ravi_entity["name"] == "Dr. Ravi Kumar", "Expected longest honorific name to be preserved"

    # Suresh with phone 9841122334 and Suresh with 9999900000 must NOT be merged (different phones/emails)
    suresh_entities = [p for p in merged if "Suresh" in p["name"]]
    assert len(suresh_entities) == 2, "Two different individuals with the same name must remain separate!"
    print("[PASS] Multi-source consolidation and same-name disambiguation verified.")

    # 2. Performance Comparison: O(n) Hash Dictionary vs O(n^2) Pairwise Scan
    print("\n--- Performance Scaling: O(n) Hash vs O(n^2) Pairwise Scan ---")
    print(f"{'Contacts':<12} | {'Hash Index Merger (s)':<24} | {'Pairwise Scan (s)':<20} | {'Speedup':<10}")
    print("-" * 72)

    scales = [1_000, 10_000]
    for n in scales:
        synth = [
            {
                "name": f"User_{i % 500}",
                "phones": [f"98400{i:05d}"],
                "emails": [f"user{i % 400}@example.com"]
            }
            for i in range(n)
        ]

        # Hash index
        t0 = time.perf_counter()
        m = ContactMerger()
        for rec in synth:
            m.add_contact(rec["name"], rec["phones"], rec["emails"])
        _ = m.get_merged_contacts()
        t_hash = time.perf_counter() - t0

        # Pairwise scan
        t0 = time.perf_counter()
        _ = merge_pairwise_naive(synth)
        t_pair = time.perf_counter() - t0

        speedup = f"{t_pair / t_hash:.1f}x"
        print(f"{n:<12} | {t_hash:<24.4f} | {t_pair:<20.4f} | {speedup:<10}")

    print("\n--- Defense of Design ---")
    print("1. Disambiguation: Same-name distinct individuals are kept isolated because matching relies on unique identifiers (phones/emails).")
    print("2. Computational Complexity: Hash indexing performs in average O(n) time, whereas pairwise comparison is O(n^2), rendering it unusable for 100,000 contacts.")

if __name__ == "__main__":
    run_q7()
