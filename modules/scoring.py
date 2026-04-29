# Function to score a lead based on multiple factors
def score_lead(lead: dict) -> dict:
    """
    Score a lead based on 5 factors:
      1. Budget       (0–30 points)
      2. Lead Source  (0–25 points)
      3. Company Size (0–20 points)
      4. Industry Fit (0–15 points)
      5. Notes Signal (0–10 points)

    """

    score = 0
    reasons = []
    breakdown = {}

    # 1. BUDGET (max 30 points) 
    budget = float(lead.get("budget_usd") or 0)
    
    if budget >= 20000:
        pts = 30
        reasons.append(f"High budget (${budget:,.0f}) — strong buying signal")
    elif budget >= 10000:
        pts = 22
        reasons.append(f"Mid-range budget (${budget:,.0f}) — viable deal")
    elif budget >= 5000:
        pts = 14
        reasons.append(f"Lower budget (${budget:,.0f}) — possible if scope fits")
    else:
        pts = 5
        reasons.append(f"Low budget (${budget:,.0f}) — may not fit Digiit pricing")
    
    score += pts
    breakdown["Budget"] = pts

    # 2. LEAD SOURCE (max 25 points)
    source = str(lead.get("source") or "").strip()
    source_scores = {
        "Referral":   25,
        "LinkedIn":   20,
        "Website":    15,
        "Cold Call":   8,
    }
    pts = source_scores.get(source, 5)
    score += pts
    breakdown["Lead Source"] = pts
    
    if pts >= 20:
        reasons.append(f"High-quality source ({source}) — warm intent")
    elif pts >= 15:
        reasons.append(f"Inbound source ({source}) — showed genuine interest")
    else:
        reasons.append(f"Lower-quality source ({source}) — needs more nurturing")

    # 3. COMPANY SIZE (max 20 points)
    size = str(lead.get("company_size") or "").strip()
    size_scores = {
        "1001+":   20,
        "501-1000": 17,
        "201-500":  14,
        "51-200":   10,
        "1-50":      5,
    }
    pts = size_scores.get(size, 5)
    score += pts
    breakdown["Company Size"] = pts
    
    if pts >= 17:
        reasons.append(f"Large enterprise ({size} employees) — high deal value potential")
    elif pts >= 14:
        reasons.append(f"Mid-size company ({size} employees) — good CRM/HRM fit")
    else:
        reasons.append(f"Small company ({size} employees) — lower contract value expected")

    # 4. INDUSTRY FIT (max 15 points)
    industry = str(lead.get("industry") or "").strip()
    # Industries known to be strong buyers of CRM/HRM in the UAE
    high_fit = ["Finance", "Real Estate", "Retail", "Healthcare", "Manufacturing"]
    mid_fit  = ["Technology", "Logistics", "Trading", "Hospitality", "Pharma",
                "Education", "Diversified", "Conglomerate"]
    
    if industry in high_fit:
        pts = 15
        reasons.append(f"{industry} is a top-fit industry for Digiit products")
    elif industry in mid_fit:
        pts = 10
        reasons.append(f"{industry} has moderate fit for CRM/HRM solutions")
    else:
        pts = 5
        reasons.append(f"{industry} — fit with Digiit products is unclear")
    
    score += pts
    breakdown["Industry Fit"] = pts

    # 5. NOTES SIGNAL (max 10 points)
    notes = str(lead.get("notes") or "").lower()
    
    # Look for strong buying-intent keywords
    hot_keywords   = ["urgent", "ready to sign", "decision maker", "30 days",
                      "immediate", "asap", "confirmed"]
    warm_keywords  = ["evaluating", "comparing", "demo", "interested", "automate",
                      "needs", "wants", "implementation"]
    
    if any(word in notes for word in hot_keywords):
        pts = 10
        reasons.append("Notes show strong buying urgency or decision-maker access")
    elif any(word in notes for word in warm_keywords):
        pts = 6
        reasons.append("Notes show active evaluation or product interest")
    else:
        pts = 2
        reasons.append("Notes show limited buying signal")
    
    score += pts
    breakdown["Notes Signal"] = pts

    # FINAL STATUS
    if score >= 65:
        status = "🔥 Hot"
    elif score >= 40:
        status = "🌡️ Warm"
    else:
        status = "❄️ Cold"

    return {
        "score": score,
        "status": status,
        "reasons": reasons,           # List of plain English explanations
        "breakdown": breakdown,       # Dict of category points for chart
        "summary": f"Score: {score}/100 — {status}"
    }

# Function to score every lead in a DataFrame and add the results as new columns
def score_all_leads(leads_df):

    results = leads_df.apply(lambda row: score_lead(row.to_dict()), axis=1)
    
    leads_df = leads_df.copy()
    leads_df["score"]        = results.apply(lambda r: r["score"])
    leads_df["status"]       = results.apply(lambda r: r["status"])
    leads_df["score_reason"] = results.apply(lambda r: " | ".join(r["reasons"]))
    
    return leads_df