import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import datetime

# Dummy data
ongoing_cases = pd.DataFrame({
    'lat': [8.5241],
    'lon': [76.9366],
    'ambulance_id': ['AMB001'],
    'destination': ['City Hospital']
})

available_ambulances = pd.DataFrame({
    'lat': [8.5275, 8.5201],
    'lon': [76.9400, 76.9333],
    'ambulance_id': ['AMB002', 'AMB003'],
    'type': ['Basic Life Support', 'Advanced Life Support']
})

call_logs = pd.DataFrame({
    'time': ["09:00 AM", "10:15 AM", "11:00 AM"],
    'caller': ["John", "Mary", "Ravi"],
    'status': ["Ongoing", "Completed", "Ongoing"]
})

case_database = pd.DataFrame({
    'Location': ['MG Road', 'Kowdiar'],
    'Nature of Injury': ['Accident', 'Heart Attack'],
    'Number of Patients': [2, 1],
    'Caller Details': ['John Doe, 9999999999', 'Mary Roy, 8888888888'],
    'Special Remarks': ['Multiple vehicles involved', 'Needs defibrillator']
})

st.set_page_config(layout="wide")
st.sidebar.title("Unified Dashboard")
option = st.sidebar.radio("Select a view:", ["Ongoing Cases", "Available Ambulances", "Call Logs and History", "Database"])

if option == "Ongoing Cases":
    st.title("Ongoing Emergency Cases")
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v11',
        initial_view_state=pdk.ViewState(
            latitude=8.5241,
            longitude=76.9366,
            zoom=13,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=ongoing_cases,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
                pickable=True
            )
        ],
        tooltip={"text": "Ambulance: {ambulance_id}\nDestination: {destination}"}
    ))

elif option == "Available Ambulances":
    st.title("Available Ambulances")
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=8.5241,
            longitude=76.9366,
            zoom=13
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=available_ambulances,
                get_position='[lon, lat]',
                get_color='[0, 150, 0, 160]',
                get_radius=150,
                pickable=True
            )
        ],
        tooltip={"text": "Ambulance: {ambulance_id}\nType: {type}"}
    ))

elif option == "Call Logs and History":
    st.title("Today's Call Logs")
    def highlight_ongoing(row):
        return ["background-color: lightgreen" if row.status == "Ongoing" else ""] * len(row)

    st.dataframe(call_logs.style.apply(highlight_ongoing, axis=1))

elif option == "Database":
    st.title("Case Database")
    st.dataframe(case_database)
