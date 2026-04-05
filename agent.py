from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import TypedDict, Optional
from data import APPROVAL_RULES, DEPARTMENT_BUDGETS

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

class InvoiceState(TypedDict):
    invoice: dict
    budget_check: Optional[str]
    approval_level: Optional[str]
    risk_analysis: Optional[str]
    final_decision: Optional[str]
    recommendation: Optional[str]

def check_budget(state: InvoiceState) -> InvoiceState:
    invoice = state["invoice"]
    dept = invoice["department"]
    amount = invoice["amount"]
    
    budget = DEPARTMENT_BUDGETS.get(dept, {})
    available = budget.get("available", 0)
    
    if available <= 0:
        result = f"BUDGET EXCEEDED: {dept} has no available budget. Spent ${budget.get('spent',0):,} of ${budget.get('total',0):,} total."
    elif amount > available:
        result = f"INSUFFICIENT BUDGET: {dept} needs ${amount:,} but only ${available:,} available."
    else:
        result = f"BUDGET OK: {dept} has ${available:,} available. Invoice for ${amount:,} fits within budget."
    
    return {**state, "budget_check": result}

def determine_approval_level(state: InvoiceState) -> InvoiceState:
    amount = state["invoice"]["amount"]
    
    for level, limit in APPROVAL_RULES.items():
        if amount <= limit:
            result = f"Requires {level.upper()} approval (limit: ${limit:,})"
            break
    
    return {**state, "approval_level": result}

def analyze_risk(state: InvoiceState) -> InvoiceState:
    invoice = state["invoice"]
    budget_check = state["budget_check"]
    
    prompt = f"""Analyze this invoice for risk and compliance in a D365 Finance context:
    
Invoice: {invoice['id']}
Vendor: {invoice['vendor']}
Department: {invoice['department']}
Amount: ${invoice['amount']:,}
Description: {invoice['description']}
Budget status: {budget_check}

Provide a brief risk assessment in 2-3 sentences. Flag any concerns."""

    response = llm.invoke([HumanMessage(content=prompt)])
    return {**state, "risk_analysis": response.content}

def make_decision(state: InvoiceState) -> InvoiceState:
    invoice = state["invoice"]
    
    prompt = f"""Based on this analysis, make a final approval recommendation:

Invoice: {invoice['id']} - {invoice['vendor']} - ${invoice['amount']:,}
Department: {invoice['department']}
Budget check: {state['budget_check']}
Approval level needed: {state['approval_level']}
Risk analysis: {state['risk_analysis']}

Respond with:
DECISION: [APPROVED / REJECTED / PENDING CFO REVIEW]
REASON: [One clear sentence]
ACTION: [Next step required]"""

    response = llm.invoke([HumanMessage(content=prompt)])
    
    decision_text = response.content
    if "APPROVED" in decision_text:
        decision = "APPROVED"
    elif "REJECTED" in decision_text:
        decision = "REJECTED"
    else:
        decision = "PENDING REVIEW"
    
    return {**state, "final_decision": decision, "recommendation": decision_text}

def build_agent():
    workflow = StateGraph(InvoiceState)
    
    workflow.add_node("check_budget", check_budget)
    workflow.add_node("determine_approval_level", determine_approval_level)
    workflow.add_node("analyze_risk", analyze_risk)
    workflow.add_node("make_decision", make_decision)
    
    workflow.set_entry_point("check_budget")
    workflow.add_edge("check_budget", "determine_approval_level")
    workflow.add_edge("determine_approval_level", "analyze_risk")
    workflow.add_edge("analyze_risk", "make_decision")
    workflow.add_edge("make_decision", END)
    
    return workflow.compile()

if __name__ == "__main__":
    from data import SAMPLE_INVOICES
    
    agent = build_agent()
    
    print("Testing Financial Approval Agent\n" + "="*40)
    
    for invoice in SAMPLE_INVOICES:
        print(f"\nProcessing: {invoice['id']} - {invoice['vendor']}")
        result = agent.invoke({"invoice": invoice})
        print(f"Budget: {result['budget_check']}")
        print(f"Approval needed: {result['approval_level']}")
        print(f"Decision: {result['final_decision']}")
        print("-"*40)