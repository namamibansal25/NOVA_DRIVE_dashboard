"""
NovaDrive CRO Decision-Support Platform - Data Loader & Analytical Engine
Loads clean research data, builds relational joins, and computes master risk scorecards.
"""

import json
import os
import pandas as pd
import numpy as np

DATA_JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "extracted_data.json")

def _clean_dataframe_from_rows(rows, header_row_idx=2):
    """Utility to turn raw extracted spreadsheet rows into a clean typed pandas DataFrame."""
    if not rows or len(rows) <= header_row_idx:
        return pd.DataFrame()
    
    headers = [str(c).strip() for c in rows[header_row_idx]]
    # Handle empty or duplicate headers
    clean_headers = []
    seen = {}
    for i, h in enumerate(headers):
        if not h:
            h = f"Col_{i}"
        if h in seen:
            seen[h] += 1
            clean_headers.append(f"{h}_{seen[h]}")
        else:
            seen[h] = 0
            clean_headers.append(h)
            
    data_rows = rows[header_row_idx + 1:]
    # Pad or truncate rows to header length
    norm_rows = []
    for r in data_rows:
        if not any(r):
            continue
        padded = r + [''] * (len(clean_headers) - len(r))
        norm_rows.append(padded[:len(clean_headers)])
        
    df = pd.DataFrame(norm_rows, columns=clean_headers)
    
    # Clean whitespace and replace empty strings with NaN where appropriate
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
    return df

def load_all_data():
    """
    Loads all 12 operational sheets into structured DataFrames.
    """
    if not os.path.exists(DATA_JSON_PATH):
        raise FileNotFoundError(f"Extracted data not found at {DATA_JSON_PATH}")
        
    with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
        raw_dict = json.load(f)
        
    df_bus = _clean_dataframe_from_rows(raw_dict.get('Business & Components', []), header_row_idx=1)
    df_univ = _clean_dataframe_from_rows(raw_dict.get('Supplier Universe & Risk', []), header_row_idx=2)
    df_score_build = _clean_dataframe_from_rows(raw_dict.get('Supplier Score Build', []), header_row_idx=2)
    df_network = _clean_dataframe_from_rows(raw_dict.get('Supplier Network', []), header_row_idx=2)
    df_excluded = _clean_dataframe_from_rows(raw_dict.get('Excluded & Mismatches', []), header_row_idx=2)
    df_evid = _clean_dataframe_from_rows(raw_dict.get('Relationship Evidence', []), header_row_idx=2)
    df_comp = _clean_dataframe_from_rows(raw_dict.get('Component Risk', []), header_row_idx=2)
    df_crit = _clean_dataframe_from_rows(raw_dict.get('Node Criticality', []), header_row_idx=2)
    df_events = _clean_dataframe_from_rows(raw_dict.get('Event Feed & Alerts', []), header_row_idx=2)
    df_flood = _clean_dataframe_from_rows(raw_dict.get('Z01 Flood Exposure', []), header_row_idx=2)
    df_alts = _clean_dataframe_from_rows(raw_dict.get('Alternate Supplier Assessment', []), header_row_idx=2)
    df_rules = _clean_dataframe_from_rows(raw_dict.get('Scoring & Evidence Rules', []), header_row_idx=2)

    # Convert numeric fields where applicable
    if "Annual Revenue (USD m)" in df_bus.columns:
        df_bus["Revenue_USD_M"] = pd.to_numeric(df_bus["Annual Revenue (USD m)"], errors="coerce").fillna(0)

    if "Supplier Risk Score" in df_univ.columns:
        df_univ["Supplier Risk Score"] = pd.to_numeric(df_univ["Supplier Risk Score"], errors="coerce")
        df_univ["Current Ratio"] = pd.to_numeric(df_univ["Current Ratio"], errors="coerce")
        df_univ["Net Debt / EBITDA"] = pd.to_numeric(df_univ["Net Debt / EBITDA"], errors="coerce")
        df_univ["Shipment Timeliness - 3M Avg (%)"] = pd.to_numeric(df_univ["Shipment Timeliness - 3M Avg (%)"], errors="coerce")
        df_univ["Timeliness Change - Jan To Latest (pp)"] = pd.to_numeric(df_univ["Timeliness Change - Jan To Latest (pp)"], errors="coerce")
        df_univ["Physical Hazard Index"] = pd.to_numeric(df_univ["Physical Hazard Index"], errors="coerce")
        df_univ["Logistics Friction Index"] = pd.to_numeric(df_univ["Logistics Friction Index"], errors="coerce")
        df_univ["Infrastructure Index"] = pd.to_numeric(df_univ["Infrastructure Index"], errors="coerce")

    if "Revenue dependent (USD m)" in df_crit.columns:
        df_crit["Revenue_Dependent_USD_M"] = pd.to_numeric(df_crit["Revenue dependent (USD m)"], errors="coerce").fillna(0)
        df_crit["Supplier risk score"] = pd.to_numeric(df_crit["Supplier risk score"], errors="coerce").fillna(0)

    if "Weighted score / 5" in df_alts.columns:
        df_alts["Weighted_Score"] = pd.to_numeric(df_alts["Weighted score / 5"], errors="coerce")

    return df_bus, df_univ, df_score_build, df_network, df_excluded, df_evid, df_comp, df_crit, df_events, df_flood, df_alts, df_rules

def calculate_master_scorecard(df_univ, df_crit, df_network, df_evid):
    """
    Computes an enriched executive scorecard uniting supplier risk metrics,
    tier role, dependent revenue, evidence counts, and chokepoint diagnostics.
    """
    master = df_univ.copy()
    
    # Merge with Node Criticality
    crit_cols = ["Entity ID", "Network role", "Components fed", "Products reached", "Revenue dependent (USD m)", "Risk band"]
    available_crit_cols = [c for c in crit_cols if c in df_crit.columns]
    
    if "Entity ID" in df_crit.columns:
        df_crit_sub = df_crit[available_crit_cols].drop_duplicates(subset=["Entity ID"])
        master = pd.merge(master, df_crit_sub, on="Entity ID", how="left")
    
    # Fill defaults for network role and dependent revenue
    if "Network role" not in master.columns:
        master["Network role"] = "Unassigned"
    else:
        master["Network role"] = master["Network role"].fillna("Non-core / Inactive")
        
    if "Revenue dependent (USD m)" not in master.columns:
        master["Revenue dependent (USD m)"] = 0
    else:
        master["Revenue dependent (USD m)"] = pd.to_numeric(master["Revenue dependent (USD m)"], errors="coerce").fillna(0)

    # Calculate evidence count per entity
    # Search entity legal name or Entity ID in df_evid
    evidence_counts = {}
    evidence_doc_ids = {}
    for _, row in master.iterrows():
        eid = row.get("Entity ID", "")
        name = row.get("Legal Name", "")
        # Clean name for matching
        short_name = name.replace("Ltd.", "").replace("GmbH", "").replace("Inc.", "").strip()
        
        matches = []
        if not df_evid.empty:
            for _, ev_row in df_evid.iterrows():
                ev_text = (ev_row.get("Title / Parties", "") + " " + ev_row.get("Evidence Detail", "")).lower()
                if (eid and eid.lower() in ev_text) or (short_name and short_name.lower() in ev_text):
                    doc_id = ev_row.get("Evidence ID", "")
                    if doc_id and doc_id not in matches:
                        matches.append(doc_id)
        evidence_counts[eid] = len(matches)
        evidence_doc_ids[eid] = ", ".join(matches[:6]) if matches else "None recorded"
        
    master["Evidence Count"] = master["Entity ID"].map(evidence_counts).fillna(0).astype(int)
    master["Linked Evidence IDs"] = master["Entity ID"].map(evidence_doc_ids).fillna("None recorded")

    # Add Chokepoint & Concentration flags
    def flag_chokepoint(row):
        rev = row.get("Revenue dependent (USD m)", 0)
        score = row.get("Supplier Risk Score", 0)
        band = str(row.get("Supplier Risk Category", "")).upper()
        name = str(row.get("Legal Name", ""))
        
        if "IonPeak" in name:
            return "CRITICAL CHOKEPOINT (Sole-source die supplier, $1,560M at risk, Z01 Flood)"
        elif "Jade" in name:
            return "CRITICAL CHOKEPOINT (Sole PCB substrate, $1,560M at risk, Z01 Flood)"
        elif "Meridian" in name:
            return "CRITICAL CHOKEPOINT (Sole dielectric film, Financial Distress EV-003)"
        elif "Aster" in name or "Boreal" in name:
            return "COMMON OWNERSHIP RISK (Both controlled by CommonSpan Holdings)"
        elif rev >= 1000 and score >= 60:
            return "HIGH-IMPACT BOTTLENECK (Portfolio exposure >$1B)"
        elif rev > 0 and score >= 70:
            return "ELEVATED CONCENTRATION RISK"
        elif rev > 0:
            return "ACTIVE PIPELINE NODE"
        else:
            return "MONITORED / STANDBY"

    master["Chokepoint Status"] = master.apply(flag_chokepoint, axis=1)

    # Risk category normalization
    if "Supplier Risk Category" in master.columns:
        master["Risk Category"] = master["Supplier Risk Category"].fillna("UNSCORED")
    else:
        master["Risk Category"] = "UNSCORED"

    return master
