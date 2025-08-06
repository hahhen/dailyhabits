import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import pandas as pd
import altair as alt
import json
from datetime import date, datetime

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

page_bg_img = '''
    <style>
        [class*="st-key-waterContainer"]{
            position: relative;
        }

        [class*="st-key-waterContainer"]::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDIxLjVDOS43ODMzMyAyMS41IDcuODk1ODMgMjAuNzMzMyA2LjMzNzUgMTkuMkM0Ljc3OTE3IDE3LjY2NjcgNCAxNS44IDQgMTMuNkM0IDEyLjU1IDQuMjA0MTcgMTEuNTQ1OCA0LjYxMjUgMTAuNTg3NUM1LjAyMDgzIDkuNjI5MTcgNS42IDguNzgzMzMgNi4zNSA4LjA1TDEyIDIuNUwxNy42NSA4LjA1QzE4LjQgOC43ODMzMyAxOC45NzkyIDkuNjI5MTcgMTkuMzg3NSAxMC41ODc1QzE5Ljc5NTggMTEuNTQ1OCAyMCAxMi41NSAyMCAxMy42QzIwIDE1LjggMTkuMjIwOCAxNy42NjY3IDE3LjY2MjUgMTkuMkMxNi4xMDQyIDIwLjczMzMgMTQuMjE2NyAyMS41IDEyIDIxLjVaIiBmaWxsPSIjOTZCRkU2Ii8+Cjwvc3ZnPgo=');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: right center;
            pointer-events: none;
            opacity: 0.3; /* Adjust transparency for the background image */
            z-index: 0; /* Place it behind the content */
        }
        
        [class*="st-key-exerciseContainer"]{
            position: relative;
        }

        [class*="st-key-exerciseContainer"]::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgZmlsbD0ibm9uZSI+CiAgPHBhdGggZmlsbD0iI0ZGQURBRCIgZD0ibTE1LjMyNSAyLjU2My0uNzUuNzc1LS43NS0uNzVhMS45MiAxLjkyIDAgMCAwLTEuNDEyLS41NzVBMS45MiAxLjkyIDAgMCAwIDExIDIuNTg4TDkuNTc1IDQuMDEzQzkuMTkyIDQuMzk2IDkgNC44NyA5IDUuNDM4YzAgLjU2Ni4xOTIgMS4wNDEuNTc1IDEuNDI1bDEuNTc1IDEuNTUtMi43NSAyLjc1LTEuNTc1LTEuNTc1YTEuOTIgMS45MiAwIDAgMC0xLjQxMy0uNTc1QTEuOTIgMS45MiAwIDAgMCA0IDkuNTg4bC0xLjQyNSAxLjQyNWMtLjM4My4zODMtLjU3NS44NTgtLjU3NSAxLjQyNSAwIC41NjYuMTkyIDEuMDQxLjU3NSAxLjQyNWwuNzUuNzUtLjc1Ljc1QTEuOTIgMS45MiAwIDAgMCAyIDE2Ljc3NWMwIC41NTkuMTkyIDEuMDMuNTc1IDEuNDEzTDUuOCAyMS40MTNhMS45MiAxLjkyIDAgMCAwIDEuNDEzLjU3NSAxLjkyIDEuOTIgMCAwIDAgMS40MTItLjU3NWwuNzUtLjc1Ljc1Ljc1Yy4zODMuMzgzLjg1OC41NzUgMS40MjUuNTc1LjU2NyAwIDEuMDQyLS4xOTIgMS40MjUtLjU3NWwxLjQyNS0xLjQyNWExLjkyIDEuOTIgMCAwIDAgLjU3NS0xLjQxMyAxLjkyIDEuOTIgMCAwIDAtLjU3NS0xLjQxMmwtMS41NzUtMS41NzUgMi43NS0yLjc1IDEuNTUgMS41NzVjLjM4My4zODMuODU4LjU3NSAxLjQyNS41NzUuNTY3IDAgMS4wNDItLjE5MiAxLjQyNS0uNTc1bDEuNDI1LTEuNDI1YTEuOTIgMS45MiAwIDAgMCAuNTc1LTEuNDEzIDEuOTIgMS45MiAwIDAgMC0uNTc1LTEuNDEybC0uNzc1LS43NzUuNzc1LS43NWExLjkyIDEuOTIgMCAwIDAgLjU3NS0xLjQxMyAxLjkyIDEuOTIgMCAwIDAtLjU3NS0xLjQxMmwtMy4yMjUtMy4yMjVjLS4zODMtLjM4NC0uODU4LS41OC0xLjQyNS0uNTg4LS41NjctLjAwOC0xLjA0Mi4xOC0xLjQyNS41NjNaIi8+Cjwvc3ZnPgo=');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: right center;
            pointer-events: none;
            opacity: 0.3; /* Adjust transparency for the background image */
            z-index: 0; /* Place it behind the content */
        }
        
        [class*="st-key-customContainer"]{
            position: relative;
        }

        [class*="st-key-customContainer"]::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTkuMyAyMkw4LjkgMTguOEM4LjY4MzMzIDE4LjcxNjcgOC40NzkxNyAxOC42MTY3IDguMjg3NSAxOC41QzguMDk1ODMgMTguMzgzMyA3LjkwODMzIDE4LjI1ODMgNy43MjUgMTguMTI1TDQuNzUgMTkuMzc1TDIgMTQuNjI1TDQuNTc1IDEyLjY3NUM0LjU1ODMzIDEyLjU1ODMgNC41NSAxMi40NDU4IDQuNTUgMTIuMzM3NVYxMS42NjI1QzQuNTUgMTEuNTU0MiA0LjU1ODMzIDExLjQ0MTcgNC41NzUgMTEuMzI1TDIgOS4zNzVMNC43NSA0LjYyNUw3LjcyNSA1Ljg3NUM3LjkwODMzIDUuNzQxNjcgOC4xIDUuNjE2NjcgOC4zIDUuNUM4LjUgNS4zODMzMyA4LjcgNS4yODMzMyA4LjkgNS4yTDkuMyAySDE0LjhMMTUuMiA1LjJDMTUuNDE2NyA1LjI4MzMzIDE1LjYyMDggNS4zODMzMyAxNS44MTI1IDUuNUMxNi4wMDQyIDUuNjE2NjcgMTYuMTkxNyA1Ljc0MTY3IDE2LjM3NSA1Ljg3NUwxOS4zNSA0LjYyNUwyMi4xIDkuMzc1TDE5LjUyNSAxMS4zMjVDMTkuNTQxNyAxMS40NDE3IDE5LjU1IDExLjU1NDIgMTkuNTUgMTEuNjYyNVYxMi4zMzc1QzE5LjU1IDEyLjQ0NTggMTkuNTMzMyAxMi41NTgzIDE5LjUgMTIuNjc1TDIyLjA3NSAxNC42MjVMMTkuMzI1IDE5LjM3NUwxNi4zNzUgMTguMTI1QzE2LjE5MTcgMTguMjU4MyAxNiAxOC4zODMzIDE1LjggMTguNUMxNS42IDE4LjYxNjcgMTUuNCAxOC43MTY3IDE1LjIgMTguOEwxNC44IDIySDkuM1pNMTIuMSAxNS41QzEzLjA2NjcgMTUuNSAxMy44OTE3IDE1LjE1ODMgMTQuNTc1IDE0LjQ3NUMxNS4yNTgzIDEzLjc5MTcgMTUuNiAxMi45NjY3IDE1LjYgMTJDMTUuNiAxMS4wMzMzIDE1LjI1ODMgMTAuMjA4MyAxNC41NzUgOS41MjVDMTMuODkxNyA4Ljg0MTY3IDEzLjA2NjcgOC41IDEyLjEgOC41QzExLjExNjcgOC41IDEwLjI4NzUgOC44NDE2NyA5LjYxMjUgOS41MjVDOC45Mzc1IDEwLjIwODMgOC42IDExLjAzMzMgOC42IDEyQzguNiAxMi45NjY3IDguOTM3NSAxMy43OTE3IDkuNjEyNSAxNC40NzVDMTAuMjg3NSAxNS4xNTgzIDExLjExNjcgMTUuNSAxMi4xIDE1LjVaIiBmaWxsPSIjRTNFM0UzIi8+Cjwvc3ZnPgo=');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: right center;
            pointer-events: none;
            opacity: 0.3; /* Adjust transparency for the background image */
            z-index: 0; /* Place it behind the content */
        }

    </style>
    '''
st.html(page_bg_img)


def make_line_chart(df):
    base = alt.Chart(df).properties(
        height=100,
    )

    # Create the blue line chart
    line = base.mark_line().encode(
        x=alt.X('Date:T', axis=alt.Axis(format='%b %d', grid=False, title=None, labelAngle=0)),
        y=alt.Y('Amount:Q', axis=alt.Axis(grid=True, title=None))
    )

    nearest_selector = alt.selection_point(
        nearest=True, on='mouseover', fields=['Date']
    )

    # Create the points that will be shown on hover
    # We use alt.condition to change the opacity based on the selector
    points = line.mark_point(filled=True).encode(
        opacity=alt.condition(nearest_selector, alt.value(1), alt.value(0))
    )

    # Create an invisible rule that will be used for the tooltip and to activate the selector
    hover_rule = base.mark_rule(color='transparent').encode(
        x='Date:T',
        tooltip=[alt.Tooltip('Date:T', format='%A, %B %d'), 'Amount:Q']
    ).add_params(
        nearest_selector
    )

    # Layer the line, the points, and the hover rule.
    chart = alt.layer(
        line, points, hover_rule
    ).configure(
        background='transparent'
    ).configure_view(
        strokeWidth=0
    )

    return chart


def login_screen():
    st.subheader("Sign In.")
    st.caption("To access the app, sign in with your Google account.")
    st.button("Log in with Google", on_click=st.login, type="primary", icon=":material/login:")


def habit_container(habit):
    with st.container(border=True, key=f"{habit['type']}Container-{habit['created_at']}"):
        data = {
            'Date': pd.to_datetime(
                ['2025-07-30', '2025-07-31', '2025-08-01', '2025-08-02', '2025-08-03', '2025-08-04', '2025-08-05',
                 '2025-08-06']),
            'Amount': [2000, 3000, 1500, 2000, 2100, 2500, 2200, 2800]
        }
        dataframe = pd.DataFrame(data)

        label = habit['type'].capitalize() if habit['type'] != 'custom' else habit['label']

        st.subheader(label)

        if habit['type'] == 'water' or habit['usesAmount']:
            unit = "mL" if habit['type'] == 'water' else "minutes" if habit['type'] != 'custom' else habit[
                'measureUnit']
            st.caption(f"Goal: 2000 mL", )

        chart = make_line_chart(dataframe)

        chart_col, _ = st.columns([5, 2])

        with chart_col:
            # Now, display the chart and tell it to fill the column it's in.
            st.altair_chart(chart, theme="streamlit", use_container_width=True)
        # -------------------------------------------------------------

        if habit['type'] == 'water' or habit['usesAmount']:
            col1, col2 = st.columns(2, vertical_alignment="bottom")
            with col1:
                title = st.number_input("Amount", value=2000, step=100, key=f"amountInput-{habit['created_at']}")
            with col2:
                st.button("Set as done", icon=":material/check:", key=f"finishButton-{habit['created_at']}")
        else:
            st.button("Set as done", icon=":material/check:", key=f"finishButton-{habit['created_at']}")

@st.dialog("Add habit")
def addHabitDialog():
    amount = 0
    measure_unit = ""
    time_toggle = False
    habit_label = ""
    measure_amount = 0
    measure_toggle = False

    type = st.selectbox("Habit type", ["Water", "Exercise", "Study", "Meditation", "Custom"])
    if type == "Water":
        col1, col2 = st.columns([3, 1])
        with col1:
            amount = st.number_input("Amount", value=2000, step=100)
        with col2:
            st.write("##")
            st.write("mL")

    elif type == "Exercise":
        time_toggle = st.toggle("Set amount of time?")

        if time_toggle:
            col1, col2 = st.columns([3, 1])
            with col1:
                amount = st.number_input("Time", value=60, step=10)
            with col2:
                st.write("##")
                st.write("minutes")

    elif type == "Study":
        time_toggle = st.toggle("Set amount of time?")

        if time_toggle:
            col1, col2 = st.columns([3, 1])
            with col1:
                amount = st.number_input("Time", value=60, step=10)
            with col2:
                st.write("##")
                st.write("minutes")

    elif type == "Meditation":
        time_toggle = st.toggle("Set amount of time?")

        if time_toggle:
            col1, col2 = st.columns([3, 1])
            with col1:
                amount = st.number_input("Time", value=60, step=10)
            with col2:
                st.write("##")
                st.write("minutes")

    elif type == "Custom":
        habit_label = st.text_input("Habit")
        measure_toggle = st.toggle("Set measuring unit?")
        if measure_toggle:
            col1, col2 = st.columns([3, 1])
            with col1:
                measure_amount = st.number_input("Amount", value=0)
            with col2:
                measure_unit = st.text_input("Unit")

    habitSubmit = st.button("Submit")
    if habitSubmit:
        newHabit = db.collection("habit").document()
        if type == "Water":
            newHabit.set({
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "water",
                "amount": amount,
                "user_id": st.user.sub,
                "completion": [{
                    "date": date.today().strftime("%Y-%m-%d"),
                    "amount": 0,
                    "finished": False
                }]
            })
        elif type == "Exercise":
            newHabit.set({
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "exercise",
                "usesAmount": time_toggle,
                "amount": amount,
                "user_id": st.user.sub,
                "completion": [{
                    "date": date.today().strftime("%Y-%m-%d"),
                    "amount": 0,
                    "finished": False
                }]
            })
        elif type == "Study":
            newHabit.set({
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "study",
                "usesAmount": time_toggle,
                "amount": amount,
                "user_id": st.user.sub,
                "completion": [{
                    "date": date.today().strftime("%Y-%m-%d"),
                    "amount": 0,
                    "finished": False
                }]
            })
        elif type == "Meditation":
            newHabit.set({
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "meditation",
                "usesAmount": time_toggle,
                "amount": amount,
                "user_id": st.user.sub,
                "completion": [{
                    "date": date.today().strftime("%Y-%m-%d"),
                    "amount": 0,
                    "finished": False
                }]
            })
        elif type == "Custom":
            newHabit.set({
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "custom",
                "label": habit_label,
                "usesAmount": measure_toggle,
                "measureUnit": measure_unit,
                "amount": measure_amount,
                "user_id": st.user.sub,
                "completion": [{
                    "date": date.today().strftime("%Y-%m-%d"),
                    "amount": 0,
                    "finished": False
                }]
            })
        st.rerun()


if not st.user.is_logged_in:
    login_screen()
else:
    usercol1, usercol2 = st.columns(2)
    with usercol1:
        st.title(f"Welcome, {st.user.given_name}!", anchor=False)
        st.button("Sign out", type="tertiary", on_click=st.logout)
    with usercol2:
        st.image(st.user.picture)

    habitsFromUser = db.collection("habit").where(field_path="user_id", op_string="==", value=st.user.sub)

    if st.button("Add habit", icon=":material/add:", type="primary"):
        addHabitDialog()
    if habitsFromUser.count().get()[0][0].value > 0:
        habits = habitsFromUser.order_by("created_at").stream()
        for habitRef in habits:
            habit = habitRef.to_dict()
            habit_container(habit)
    else:
        st.header("You have no habits yet.")
