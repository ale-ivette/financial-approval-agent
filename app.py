import streamlit as st
from agent import build_agent
from data import SAMPLE_INVOICES, DEPARTMENT_BUDGETS

st.set_page_config(
    page_title="Financial Approval Agent",
    page_icon="📋",
    layout="wide"
)

st.title("Financial Approval Agent")
st.caption("Powered by LangGraph · Dynamics 365 Finance")

if "agent" not in st.session_state:
    st.session_state.agent = build_agent()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Submit Invoice for Review")
    
    invoice_id = st.text_input("Invoice ID", "INV-2025-004")
    vendor = st.text_input("Vendor", "Microsoft")
    department = st.selectbox("Department", list(DEPARTMENT_BUDGETS.keys()))
    amount = st.number_input("Amount (USD)", min_value=0, value=5000, step=500)
    description = st.text_area("Description", "Software licenses Q1 2025")
    submitted_by = st.text_input("Submitted by", "Ale Cabrales")
    
    if st.button("Process Invoice"):
        invoice = {
            "id": invoice_id,
            "vendor": vendor,
            "department": department,
            "amount": amount,
            "description": description,
            "submitted_by": submitted_by
        }
        
        with st.spinner("Agent analyzing invoice..."):
            result = st.session_state.agent.invoke({"invoice": invoice})
        
        st.session_state.last_result = result

with col2:
    st.subheader("Agent Decision")
    
    if "last_result" in st.session_state:
        result = st.session_state.last_result
        
        decision = result["final_decision"]
        if decision == "APPROVED":
            st.success(f"Decision: {decision}")
        elif decision == "REJECTED":
            st.error(f"Decision: {decision}")
        else:
            st.warning(f"Decision: {decision}")
        
        with st.expander("Budget Analysis", expanded=True):
            st.write(result["budget_check"])
        
        with st.expander("Approval Level Required", expanded=True):
            st.write(result["approval_level"])
        
        with st.expander("Risk Analysis", expanded=True):
            st.write(result["risk_analysis"])
        
        with st.expander("Full Recommendation", expanded=True):
            st.write(result["recommendation"])
    else:
        st.info("Submit an invoice to see the agent's analysis.")

st.divider()
st.subheader("Department Budget Status")

cols = st.columns(len(DEPARTMENT_BUDGETS))
for col, (dept, budget) in zip(cols, DEPARTMENT_BUDGETS.items()):
    with col:
        pct = (budget["spent"] / budget["total"]) * 100
        if pct > 100:
            st.error(f"**{dept}**\n\nSpent: ${budget['spent']:,}\nBudget: ${budget['total']:,}\n\nOVER BUDGET")
        elif pct > 85:
            st.warning(f"**{dept}**\n\nSpent: ${budget['spent']:,}\nAvailable: ${budget['available']:,}\n\n{pct:.0f}% used")
        else:
            st.success(f"**{dept}**\n\nSpent: ${budget['spent']:,}\nAvailable: ${budget['available']:,}\n\n{pct:.0f}% used")