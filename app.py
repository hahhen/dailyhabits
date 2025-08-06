import streamlit as st
from google.cloud import firestore
import pandas as pd
import altair as alt

page_bg_img = '''
    <style>
        .st-key-waterContainer{
            position: relative;
        }

        .st-key-waterContainer::before {
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

with st.container(border=True, key="waterContainer"):
    data = {
        'Date': pd.to_datetime(
            ['2025-07-30', '2025-07-31', '2025-08-01', '2025-08-02', '2025-08-03', '2025-08-04', '2025-08-05',
             '2025-08-06']),
        'Amount': [2000, 3000, 1500, 2000, 2100, 2500, 2200, 2800]
    }
    dataframe = pd.DataFrame(data)

    st.subheader("Water")
    st.caption("Goal: 2000 mL", )

    chart = make_line_chart(dataframe)

    chart_col, _ = st.columns([5, 2])

    with chart_col:
        # Now, display the chart and tell it to fill the column it's in.
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
    # -------------------------------------------------------------

    col1, col2 = st.columns(2, vertical_alignment="bottom")
    with col1:
        title = st.number_input("Amount", value=2000, step=100)
    with col2:
        st.button("Set as done", icon=":material/check:")
    st.write("The current movie title is", title)
