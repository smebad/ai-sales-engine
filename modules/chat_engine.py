# QUESTION FLOW

QUESTIONS = [
    {
        "key": "timeline",
        "text": (
            "Hello! I'm AI Sales Assistant. 👋\n\n"
            "I'd like to ask you a few quick questions to make sure "
            "we can find the right solution for your team.\n\n"
            "**First: What is your expected timeline for implementing "
            "a CRM or HRM solution?**\n"
            "_(e.g. Within 1 month / 1–3 months / 3–6 months / Just exploring)_"
        )
    },
    {
        "key": "pain_point",
        "text": (
            "Got it, thank you!\n\n"
            "**What is the biggest challenge your team is facing right now "
            "that a CRM or HRM system would help solve?**\n"
            "_(e.g. losing track of leads, slow hiring process, manual reporting, etc.)_"
        )
    },
    {
        "key": "decision_maker",
        "text": (
            "That's a common challenge and exactly what I'm built to solve.\n\n"
            "**Are you the main decision maker for this purchase, or are "
            "others involved in the approval?**\n"
            "_(e.g. Yes, I decide / Need manager approval / Board decision)_"
        )
    },
    {
        "key": "current_tool",
        "text": (
            "Understood.\n\n"
            "**What tools or systems are you currently using to manage "
            "your sales pipeline or HR processes?**\n"
            "_(e.g. Excel, another CRM, nothing yet, in-house system)_"
        )
    },
    {
        "key": "top_priority",
        "text": (
            "Very helpful to know, thank you for sharing that.\n\n"
            "**Last question: What matters most to you when choosing a platform?**\n"
            "_(e.g. Price, ease of use, Arabic language support, integrations, "
            "local UAE support, scalability)_"
        )
    }
]

# RESPONSE ANALYSIS HELPERS
# Function to convert a free-text timeline answer into a standard category
def analyze_timeline(answer: str) -> str:

    answer = answer.lower()
    if any(w in answer for w in ["1 month", "30 day", "asap", "urgent", "immediately", "now"]):
        return "Within 1 month"
    elif any(w in answer for w in ["1-3", "1 to 3", "quarter", "q1", "q2", "q3", "q4", "few months"]):
        return "1–3 months"
    elif any(w in answer for w in ["3-6", "3 to 6", "6 month", "half year"]):
        return "3–6 months"
    else:
        return "Exploring / Not decided"

# Function to classify the user's role in the purchase decision
def analyze_decision_maker(answer: str) -> str:

    answer = answer.lower()
    if any(w in answer for w in ["yes", "i decide", "my decision", "i am", "sole", "only me"]):
        return "Decision maker"
    elif any(w in answer for w in ["manager", "boss", "director", "approval", "my team"]):
        return "Needs approval"
    elif any(w in answer for w in ["board", "committee", "ceo", "cto", "cfo", "executive"]):
        return "Executive approval required"
    else:
        return "Unclear"

# Function to classify what tool they currently use.
def analyze_current_tool(answer: str) -> str:

    answer = answer.lower()
    if any(w in answer for w in ["excel", "spreadsheet", "sheet", "google sheet"]):
        return "Excel/Spreadsheets"
    elif any(w in answer for w in ["nothing", "none", "no system", "manual", "no tool"]):
        return "No system"
    elif any(w in answer for w in ["salesforce", "hubspot", "zoho", "pipedrive", "odoo"]):
        return "Competitor CRM"
    elif any(w in answer for w in ["in-house", "custom", "internal", "built"]):
        return "In-house system"
    else:
        return "Other / unclear"

# FOLLOW-UP RESPONSES

# Function to return a short acknowledgment
def get_acknowledgment(question_key: str, answer: str) -> str:
    
    if question_key == "timeline":
        tl = analyze_timeline(answer)
        if tl == "Within 1 month":
            return "⚡ Great — that's a fast timeline. We have teams ready to onboard quickly."
        elif tl == "1–3 months":
            return "📅 Perfect — that gives us enough time to do a proper implementation."
        else:
            return "No rush at all — we can work at whatever pace suits your team."
    
    elif question_key == "pain_point":
        return "💡 That's one of the top issues our clients come to us with. Good context."
    
    elif question_key == "decision_maker":
        dm = analyze_decision_maker(answer)
        if dm == "Decision maker":
            return "👍 Excellent — having the decision maker involved always speeds things up."
        else:
            return "Understood — we can prepare a proposal package that's easy to share upward."
    
    elif question_key == "current_tool":
        tool = analyze_current_tool(answer)
        if tool == "No system":
            return "📋 Starting fresh is actually easier — no messy migration needed."
        elif tool == "Competitor CRM":
            return "🔄 We have migration support and can import your existing data."
        else:
            return "Good to know — we'll factor that into the implementation plan."
    
    elif question_key == "top_priority":
        return "✅ Noted — that helps us tailor the right package for you."
    
    return ""

# SUMMARY GENERATOR

# Function to generate a structured lead summary after all questions are answered
def generate_summary(lead: dict, answers: dict) -> dict:
    
    timeline    = analyze_timeline(answers.get("timeline", ""))
    dm_status   = analyze_decision_maker(answers.get("decision_maker", ""))
    current_tool= analyze_current_tool(answers.get("current_tool", ""))
    pain_point  = answers.get("pain_point", "Not provided")
    priority    = answers.get("top_priority", "Not provided")
    
    # Determine conversation based qualification score adjustment
    boost = 0
    flags = []
    
    if timeline == "Within 1 month":
        boost += 15
        flags.append("🔥 Urgent timeline")
    elif timeline == "1–3 months":
        boost += 8
        flags.append("📅 Near-term timeline")
    
    if dm_status == "Decision maker":
        boost += 10
        flags.append("✅ Decision maker confirmed")
    elif dm_status == "Needs approval":
        boost += 3
        flags.append("⚠️ Needs internal approval")
    
    if current_tool == "No system":
        boost += 5
        flags.append("📋 No existing system — easy win")
    elif current_tool == "Competitor CRM":
        boost += 3
        flags.append("🔄 Currently on competitor tool")
    
    # Build the summary text
    summary_lines = [
        f"**Lead:** {lead.get('name')} @ {lead.get('company')}",
        f"**Product Interest:** {lead.get('product_interest', 'N/A')}",
        f"**Budget:** ${float(lead.get('budget_usd', 0)):,.0f}",
        "",
        "**Qualification Answers:**",
        f"- Timeline: {timeline}",
        f"- Main pain point: {pain_point}",
        f"- Decision authority: {dm_status}",
        f"- Current tool: {current_tool}",
        f"- Top priority: {priority}",
        "",
        "**Signals Detected:**",
    ] + [f"  {flag}" for flag in flags]
    
    if not flags:
        summary_lines.append("No strong urgency signals detected — nurture track recommended")
    
    return {
        "summary_text": "\n".join(summary_lines),
        "score_boost": boost,
        "timeline": timeline,
        "dm_status": dm_status,
        "current_tool": current_tool,
        "pain_point": pain_point,
        "priority": priority,
        "flags": flags
    }

# CHAT STATE MANAGER

# Function to return the very first message the bot sends.
def get_initial_state():

    return {
        "messages":       [],   # List of {"role": "assistant"/"user", "content": "..."}
        "question_index": 0,    # Which question we're currently on (0–4)
        "answers":        {},   # Collected answers keyed by question key
        "completed":      False # Whether all 5 questions are done
    }

# Function to give the bot current chat state and a new user message.
def process_user_message(state: dict, user_input: str, lead: dict) -> dict:
    
    # Record the user's message
    state["messages"].append({"role": "user", "content": user_input})
    
    q_index = state["question_index"]
    
    # If we've already finished all questions, do nothing
    if state["completed"]:
        return state
    
    # Store the answer for the current question
    current_question_key = QUESTIONS[q_index]["key"]
    state["answers"][current_question_key] = user_input
    
    # Generate acknowledgment for this answer
    ack = get_acknowledgment(current_question_key, user_input)
    
    # Move to the next question
    next_index = q_index + 1
    state["question_index"] = next_index
    
    if next_index < len(QUESTIONS):
        # There are more questions — send acknowledgment + next question
        next_q = QUESTIONS[next_index]["text"]
        bot_reply = f"{ack}\n\n{next_q}" if ack else next_q
        state["messages"].append({"role": "assistant", "content": bot_reply})
    else:
        # All questions answered — generate summary
        state["completed"] = True
        summary = generate_summary(lead, state["answers"])
        state["summary"] = summary
        
        closing = (
            f"{ack}\n\n"
            "---\n"
            "✅ **Thank you — I have everything I need!**\n\n"
            "Here's a summary of your qualification:\n\n"
            f"{summary['summary_text']}\n\n"
            "A Digiit sales specialist will be in touch shortly. "
            "We look forward to showing you what we can do! 🚀"
        )
        state["messages"].append({"role": "assistant", "content": closing})
    
    return state

# Function to return the very first message the bot sends
def get_opening_message():

    return QUESTIONS[0]["text"]