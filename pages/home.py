import streamlit as st
import datetime
import matplotlib.pyplot as plt

def home_page():
    st.markdown("""
    <div class="title-container">
        <h1>🌤️ Welcome back, Daniella!</h1>
        <div class="title-sub">Plan your day with calm focus — we've got the details covered.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### Quick glance at your week")
    col1, col2, col3 = st.columns(3)

    with col1:
        total_income = sum(i["amount"] for i in st.session_state.budget_store.get("incomes", []))
        total_expenses = sum(e["amount"] for e in st.session_state.budget_store.get("expenses", []))
        st.metric("💸 Balance", f"₦{total_income - total_expenses:,.2f}")

    with col2:
        due_assignments = [a for a in st.session_state.assignments if a.get("status") != "Done"]
        st.metric("📚 Assignments Pending", str(len(due_assignments)))

    with col3:
        upcoming = [e for e in st.session_state.all_events if datetime.date.fromisoformat(e["date"]) >= datetime.date.today()]
        st.metric("🎉 Upcoming Events", str(len(upcoming)))

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("✨ Daniella’s Picks")
    picks = [e for e in st.session_state.all_events if e.get("user_pick")]
    if not picks:
        st.info("You don't have any picks yet — go to Activities to spotlight your faves!")
    else:
        for e in picks[:4]:
            days_left = (datetime.date.fromisoformat(e["date"]) - datetime.date.today()).days
            st.markdown(f"""
                <div class="card">
                    <h4>{e['title']} <span style='color:gold'>★</span></h4>
                    <p><b>Date:</b> {e['date']} | <b>Time:</b> {e['time']}<br>
                    <b>Type:</b> {e['type']} | <b>Location:</b> {e['location']}<br>
                    <small>⏳ {days_left} day(s) to go</small></p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📊 Quick Budget Snapshot")
    if st.session_state.budget_store.get("expenses"):
        labels = [e["expense"] for e in st.session_state.budget_store["expenses"]]
        sizes = [e["amount"] for e in st.session_state.budget_store["expenses"]]
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.info("Add expenses in Budget Tracker to see a visual snapshot here.")
