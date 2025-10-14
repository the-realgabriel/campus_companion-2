# campus_companion.py
import streamlit as st
import matplotlib.pyplot as plt
import datetime
import uuid
import json
import os

# ----------------------------
# 🌈 CONFIG
# ----------------------------
st.set_page_config(page_title="Campus Companion", page_icon="🎓", layout="wide")

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

FILES = {
    "events": os.path.join(DATA_DIR, "events.json"),
    "timetable": os.path.join(DATA_DIR, "timetable.json"),
    "assignments": os.path.join(DATA_DIR, "assignments.json"),
    "streaks": os.path.join(DATA_DIR, "streaks.json"),
    "budget": os.path.join(DATA_DIR, "budget.json"),  # will store incomes, budgets, expenses
}

# ----------------------------
# 💾 Persistence Utilities
# ----------------------------
def save_data(path, data):
    with open(path, "w") as f:
        json.dump(data, f, default=str)

def load_data(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return default
    return default

# ----------------------------
# 🎨 THEME & GLOBAL FONT (APPLIES TO WHOLE APP)
# ----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&family=Playfair+Display:wght@500&display=swap');

    /* Force app-wide font and base color */
    * {
        font-family: 'Poppins', sans-serif !important;
        color: #16314a !important;
    }

    /* App background */
    .stApp {
        background: linear-gradient(180deg, #f7fbff 0%, #ffffff 100%);
    }

    /* Header / Title styles (use Playfair for headings for visual luxury) */
    .title-container h1 {
        font-family: 'Playfair Display', serif !important;
        color: #10293f !important;
        font-size: 2.2rem;
        margin: 0;
    }
    .title-sub {
        color: #3b556e !important;
        margin-top: 6px;
        margin-bottom: 18px;
    }

    /* Sidebar: darker, high-contrast but still elegant */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f3a6b 0%, #153056 100%) !important;
        color: #ffffff !important;
        border-right: 1px solid rgba(255,255,255,0.06);
        padding-top: 18px;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        font-weight: 500;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stButton>button {
        background: rgba(255,255,255,0.06) !important;
        color: #ffffff !important;
    }

    /* Card styling used across body content */
    .card {
        background: #ffffff;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 8px 24px rgba(17,36,59,0.06);
        border: 1px solid #eef4fb;
    }

    /* Buttons (primary) */
    .stButton>button {
        background: linear-gradient(90deg, #5c84d6, #89aef5) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 8px 14px !important;
        font-weight: 600 !important;
        box-shadow: 0 6px 16px rgba(92,132,214,0.18) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
    }

    /* Inputs */
    input, textarea, select {
        border-radius: 8px !important;
        border: 1px solid #dbeefc !important;
        background-color: #fbfeff !important;
        color: #16314a !important;
    }

    /* Metric labels & values */
    [data-testid="stMetricValue"] {
        color: #0b2a49 !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #16314a !important;
        font-weight: 600 !important;
    }

    /* Tab styling */
    div[data-baseweb="tab-list"] {
        background: #f2f8ff !important;
        border-radius: 10px !important;
        padding: 6px !important;
    }
    button[data-baseweb="tab"] {
        color: #0b2a49 !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(90deg,#5c84d6,#89aef5) !important;
        color: #fff !important;
        box-shadow: 0 6px 14px rgba(92,132,214,0.14) !important;
    }

    /* Small responsive tweaks */
    @media (max-width: 800px) {
        .title-container h1 { font-size: 1.6rem !important; }
        .card { padding: 12px !important; }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# 🔁 Initialize / Load Data into session_state
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# load stores
if "all_events" not in st.session_state:
    st.session_state.all_events = load_data(FILES["events"], [])

if "timetable_entries" not in st.session_state:
    st.session_state.timetable_entries = load_data(FILES["timetable"], [])

if "assignments" not in st.session_state:
    st.session_state.assignments = load_data(FILES["assignments"], [])

if "streak_dates" not in st.session_state:
    st.session_state.streak_dates = load_data(FILES["streaks"], [])

if "budget_store" not in st.session_state:
    st.session_state.budget_store = load_data(FILES["budget"], {"incomes": [], "budgets": [], "expenses": []})

# ----------------------------
# 🧭 Sidebar Navigation (high contrast & clear)
# ----------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3022/3022067.png", width=72)
    st.markdown("<h2 style='color:white; margin:6px 0 0 0;'>Campus Companion</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#dbeaff; margin-bottom:8px;'>Your  luxury planner</div>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)

    page_choice = st.radio("Navigate", ["🏠 Home", "💰 Budget Tracker", "📅 Timetable", "🎉 Activities", "🤖 StudyBot"])
    mapping = {
        "🏠 Home": "home",
        "💰 Budget Tracker": "budget",
        "📅 Timetable": "timetable",
        "🎉 Activities": "activities",
        "🤖 StudyBot": "chatbot",
    }
    st.session_state.page = mapping.get(page_choice, "home")

    st.markdown("---", unsafe_allow_html=True)
    if st.button("Save All Now"):
        save_data(FILES["events"], st.session_state.all_events)
        save_data(FILES["timetable"], st.session_state.timetable_entries)
        save_data(FILES["assignments"], st.session_state.assignments)
        save_data(FILES["streaks"], st.session_state.streak_dates)
        save_data(FILES["budget"], st.session_state.budget_store)
        st.success("All data saved ✅")

# ----------------------------
# 🏠 Home Page Function
# ----------------------------
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
                <div class="card" style="margin-bottom:12px;">
                <h4 style="margin:0">{e['title']} <span style='color:gold'>★</span></h4>
                <p style="margin:6px 0 0 0;"><b>Date:</b> {e['date']} | <b>Time:</b> {e['time']}<br>
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

# ----------------------------
# 💰 Budget Page Function
# ----------------------------
def budget_page():
    st.title("💰 Budget Tracker")
    tabs = st.tabs(["💵 Log Income", "📊 Budget Categories", "📉 Log Expenses", "📋 Summary Sheet"])

    # --- income
    with tabs[0]:
        st.subheader("💵 Add Income")
        with st.form("income_form"):
            source = st.text_input("Source name")
            amount = st.number_input("Amount", min_value=0.0, format="%f")
            submit = st.form_submit_button("➕ Add Income")
            if submit and source and amount:
                st.session_state.budget_store.setdefault("incomes", []).append({"id": str(uuid.uuid4()), "source": source, "amount": float(amount)})
                save_data(FILES["budget"], st.session_state.budget_store)
                st.success(f"Added income: {source} — ₦{amount:,.2f}")

        if st.session_state.budget_store.get("incomes"):
            st.markdown("**Your incomes**")
            for inc in st.session_state.budget_store["incomes"]:
                st.write(f"• {inc['source']} — ₦{inc['amount']:,.2f}")

    # --- budgets (planned)
    with tabs[1]:
        st.subheader("📊 Budget Categories (Planned Allocations)")
        with st.form("budget_cat_form"):
            cat = st.text_input("Category name")
            amt = st.number_input("Amount", min_value=0.0, format="%f")
            color = st.color_picker("Color tag", value="#b3e5fc")
            add = st.form_submit_button("➕ Add Category")
            if add and cat and amt:
                st.session_state.budget_store.setdefault("budgets", []).append({"id": str(uuid.uuid4()), "category": cat, "amount": float(amt), "color": color})
                save_data(FILES["budget"], st.session_state.budget_store)
                st.success(f"Added category: {cat} — ₦{amt:,.2f}")

        if st.session_state.budget_store.get("budgets"):
            for b in st.session_state.budget_store["budgets"]:
                st.markdown(f"- {b['category']} — ₦{b['amount']:,.2f}")

    # --- expenses (actual)
    with tabs[2]:
        st.subheader("📉 Log Expense")
        with st.form("expense_form"):
            name = st.text_input("Expense name")
            amt = st.number_input("Amount", min_value=0.0, format="%f")
            color = st.color_picker("Color tag", value="#ffccbc")
            submit = st.form_submit_button("➕ Add Expense")
            if submit and name and amt:
                st.session_state.budget_store.setdefault("expenses", []).append({"id": str(uuid.uuid4()), "expense": name, "amount": float(amt), "color": color, "date": datetime.date.today().isoformat()})
                save_data(FILES["budget"], st.session_state.budget_store)
                st.success(f"Logged expense: {name} — ₦{amt:,.2f}")

        # streak tracker
        st.markdown("---")
        st.subheader("🔥 Expense Logging Streak")
        today = datetime.date.today().isoformat()
        if st.button("✅ I logged expenses today"):
            if today not in st.session_state.streak_dates:
                st.session_state.streak_dates.append(today)
                save_data(FILES["streaks"], st.session_state.streak_dates)
                st.success("Nice! Today added to your streak 🔥")
            else:
                st.info("You already logged today 👏")
        # compute streak
        streak_list = sorted([datetime.date.fromisoformat(d) for d in st.session_state.streak_dates]) if st.session_state.streak_dates else []
        streak_count = 0
        if streak_list:
            # start from the end and count consecutive days backward
            streak_count = 1
            for i in range(len(streak_list)-1, 0, -1):
                if (streak_list[i] - streak_list[i-1]).days == 1:
                    streak_count += 1
                else:
                    break
        st.metric("🔥 Current Streak", f"{streak_count} day(s)")

    # --- summary
    with tabs[3]:
        st.subheader("📋 Financial Summary")
        incomes = st.session_state.budget_store.get("incomes", [])
        expenses = st.session_state.budget_store.get("expenses", [])
        budgets = st.session_state.budget_store.get("budgets", [])
        total_income = sum(i["amount"] for i in incomes)
        total_exp = sum(e["amount"] for e in expenses)
        total_budgeted = sum(b["amount"] for b in budgets)
        net = total_income - total_exp

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("💰 Total Income", f"₦{total_income:,.2f}")
        c2.metric("📉 Total Expenses", f"₦{total_exp:,.2f}")
        c3.metric("📊 Budgeted", f"₦{total_budgeted:,.2f}")
        c4.metric("💼 Net Balance", f"₦{net:,.2f}")

        if expenses:
            st.markdown("### 🥧 Expense Breakdown")
            labels = [e["expense"] for e in expenses]
            sizes = [e["amount"] for e in expenses]
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
            ax.axis("equal")
            st.pyplot(fig)
        else:
            st.info("No expenses yet — add some to see a breakdown.")

# ----------------------------
# 📅 Timetable Page
# ----------------------------
def timetable_page():
    st.title("📅 Timetable & Assignments")
    st.markdown("Add classes, color-code them, and track assignments.")

    # add class form
    with st.form("add_class_form"):
        col1, col2 = st.columns(2)
        with col1:
            day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
            time = st.time_input("Class Time")
            color = st.color_picker("Class Color", value="#b3e5fc")
        with col2:
            course = st.text_input("Course Name")
            lecturer = st.text_input("Lecturer")
            notes = st.text_area("Notes / Location")
        reminder = st.checkbox("Set Reminder (simulated)")
        submit = st.form_submit_button("➕ Add Class")
        if submit and course:
            st.session_state.timetable_entries.append({
                "id": str(uuid.uuid4()),
                "day": day,
                "time": time.strftime("%I:%M %p"),
                "course": course,
                "lecturer": lecturer,
                "notes": notes,
                "color": color,
                "reminder": reminder
            })
            save_data(FILES["timetable"], st.session_state.timetable_entries)
            st.success(f"{course} added!")

    # display timetable grouped by day
    st.subheader("Weekly Timetable")
    if st.session_state.timetable_entries:
        by_day = {}
        for t in st.session_state.timetable_entries:
            by_day.setdefault(t["day"], []).append(t)
        for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
            entries = by_day.get(d, [])
            if entries:
                st.markdown(f"#### {d}")
                for e in sorted(entries, key=lambda x: x["time"]):
                    st.markdown(f"""
                        <div class="card" style="margin-bottom:8px; background:{e['color']}">
                        <strong>{e['time']} - {e['course']}</strong><br>
                        👩‍🏫 {e['lecturer']}<br>
                        🗒️ {e['notes']}<br>
                        {'🔔 Reminder set' if e['reminder'] else ''}
                        </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("No classes yet — add one above!")

    # assignments
    st.markdown("---")
    st.subheader("📚 Class Assignments")
    class_choices = [e["course"] for e in st.session_state.timetable_entries] or ["General"]
    with st.form("assignment_form"):
        selected_course = st.selectbox("Select Course", class_choices)
        title = st.text_input("Assignment Title")
        status = st.selectbox("Status", ["Not Started", "In Progress", "Done"])
        due_date = st.date_input("Due Date", value=datetime.date.today())
        notes = st.text_area("Notes")
        add = st.form_submit_button("➕ Log Assignment")
        if add and title:
            st.session_state.assignments.append({
                "id": str(uuid.uuid4()),
                "course": selected_course,
                "title": title,
                "status": status,
                "due_date": due_date.isoformat(),
                "notes": notes
            })
            save_data(FILES["assignments"], st.session_state.assignments)
            st.success(f"Assignment '{title}' added for {selected_course}!")

    # assignment filters
    st.subheader("Your Assignments")
    status_filter = st.selectbox("Filter by Status", ["All", "Not Started", "In Progress", "Done"])
    upcoming_only = st.checkbox("Show only due in next 7 days")
    today = datetime.date.today()
    filtered = []
    for a in st.session_state.assignments:
        d = datetime.date.fromisoformat(a["due_date"])
        status_ok = (status_filter == "All") or (a["status"] == status_filter)
        date_ok = (not upcoming_only) or (0 <= (d - today).days <= 7)
        if status_ok and date_ok:
            filtered.append((a, d))
    if filtered:
        for a, due in filtered:
            overdue = (due < today and a["status"] != "Done")
            bg = "#ffdddd" if overdue else "#ffffff"
            st.markdown(f"""
                <div class="card" style="margin-bottom:8px; background:{bg}">
                <strong>📝 {a['title']}</strong> — {a['course']}<br>
                📅 Due: {a['due_date']} — <em>{a['status']}</em><br>
                📌 {a['notes']}<br>
                {'<span style="color:red">🚨 Overdue!</span>' if overdue else ''}
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No assignments match the filters.")

# ----------------------------
# 🎉 Activities Page
# ----------------------------
def activities_page():
    st.title("🎉 Campus Activities")
    st.write("Create public events and personal schedule items.")

    st.subheader("Create an Event for Everyone")
    with st.form("public_event_form"):
        ev_title = st.text_input("Event Title")
        ev_date = st.date_input("Event Date", value=datetime.date.today())
        ev_time = st.time_input("Event Time")
        ev_loc = st.text_input("Location")
        ev_type = st.selectbox("Event Type", ["Social", "Academic", "Club", "Other"])
        ev_color = st.color_picker("Event Color", value="#cfe9ff")
        ev_pick = st.checkbox("Mark as User's Pick (spotlight)")
        ev_desc = st.text_area("Description")
        add_ev = st.form_submit_button("✅ Add Event")
        if add_ev and ev_title:
            event = {
                "id": str(uuid.uuid4()),
                "title": ev_title,
                "date": ev_date.isoformat(),
                "time": ev_time.strftime("%I:%M %p"),
                "location": ev_loc,
                "type": ev_type,
                "color": ev_color,
                "user_pick": ev_pick,
                "description": ev_desc or "No description"
            }
            st.session_state.all_events.append(event)
            save_data(FILES["events"], st.session_state.all_events)
            st.success("🎉 Event added!")

    st.markdown("---")
    st.subheader("Upcoming Campus Events")
    today = datetime.date.today()
    if st.session_state.all_events:
        for e in sorted(st.session_state.all_events, key=lambda x: x["date"]):
            days_left = (datetime.date.fromisoformat(e["date"]) - today).days
            st.markdown(f"""
                <div class="card" style="margin-bottom:10px; background:{e['color']}">
                <strong>🎫 {e['title']}</strong> — {e['type']}<br>
                📍 {e['location']} | 🕒 {e['time']} | 📅 {e['date']}<br>
                📝 {e['description']}<br>
                {'⏳ Starts in ' + str(days_left) + ' day(s)' if days_left >= 0 else '🚨 Happened already'}
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No campus events yet — add one above!")

    st.markdown("---")
    st.subheader("Your Personal Schedule")
    username = st.text_input("Your name (for personal schedule)", value="Daniella")
    if "personal_schedules" not in st.session_state:
        st.session_state.personal_schedules = {}

    if username and username not in st.session_state.personal_schedules:
        st.session_state.personal_schedules[username] = []

    with st.form("personal_event_form"):
        ptitle = st.text_input("Task Title")
        pdate = st.date_input("Task Date", value=today)
        ptime = st.time_input("Task Time")
        pdesc = st.text_area("Notes")
        pcolor = st.color_picker("Color tag", value="#e3f2fd")
        psave = st.form_submit_button("➕ Add Personal Task")
        if psave and ptitle:
            st.session_state.personal_schedules.setdefault(username, []).append({
                "id": str(uuid.uuid4()),
                "title": ptitle,
                "date": pdate.isoformat(),
                "time": ptime.strftime("%I:%M %p"),
                "description": pdesc,
                "color": pcolor
            })
            st.success(f"Added personal task '{ptitle}'")

    st.markdown(f"#### Tasks for {username} (today)")
    tasks = st.session_state.personal_schedules.get(username, [])
    for t in tasks:
        if datetime.date.fromisoformat(t["date"]) == today:
            st.markdown(f"""
                <div class="card" style="margin-bottom:8px; background:{t['color']}">
                📌 <strong>{t['title']}</strong><br>
                🕒 {t['time']}<br>
                📝 {t['description']}
                </div>
            """, unsafe_allow_html=True)

# ----------------------------
# 🤖 Chatbot Page (Simple)
# ----------------------------
def chatbot_page():
    st.title("🤖 StudyBot")
    st.info("Ask StudyBot a study question — currently a simple helper (no AI integration).")
    q = st.text_input("Ask StudyBot:")
    if q:
        st.markdown("**StudyBot says:**")
        if "assignment" in q.lower() or "due" in q.lower():
            st.write("Make a checklist, break the task into 25-minute pomodoro sessions, and set small milestones.")
        elif "budget" in q.lower() or "money" in q.lower():
            st.write("Track all incomes and expenses for 2 weeks to find savings opportunities. Use categories.")
        else:
            st.write("Good question! Try splitting it into smaller parts — what specifically would you like help with?")

# ----------------------------
# 🧭 Page Router
# ----------------------------
page = st.session_state.page
if page == "home":
    home_page()
elif page == "budget":
    budget_page()
elif page == "timetable":
    timetable_page()
elif page == "activities":
    activities_page()
elif page == "chatbot":
    chatbot_page()

# ----------------------------
# 🔁 Auto-save on every rerun (lightweight)
# ----------------------------
save_data(FILES["events"], st.session_state.all_events)
save_data(FILES["timetable"], st.session_state.timetable_entries)
save_data(FILES["assignments"], st.session_state.assignments)
save_data(FILES["streaks"], st.session_state.streak_dates)
save_data(FILES["budget"], st.session_state.budget_store)
