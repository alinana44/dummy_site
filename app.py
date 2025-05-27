import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import datetime
import json

# Dummy data for ongoing cases (accident sites)
ongoing_cases = pd.DataFrame({
    'lat': [8.5241, 8.5180],
    'lon': [76.9366, 76.9290],
    'case_id': ['CASE001', 'CASE002'],
    'location': ['MG Road Junction', 'Kowdiar Palace'],
    'severity': ['High', 'Medium']
})

# Ambulances en route to cases
ambulances_enroute = pd.DataFrame({
    'lat': [8.5275, 8.5201],
    'lon': [76.9400, 76.9333],
    'ambulance_id': ['AMB001', 'AMB002'],
    'type': ['Advanced Life Support', 'Basic Life Support'],
    'destination_lat': [8.5241, 8.5180],
    'destination_lon': [76.9366, 76.9290],
    'case_id': ['CASE001', 'CASE002'],
    'eta': ['5 min', '8 min']
})

# Available ambulances (not assigned)
available_ambulances = pd.DataFrame({
    'lat': [8.5301, 8.5150, 8.5320],
    'lon': [76.9450, 76.9280, 76.9380],
    'ambulance_id': ['AMB003', 'AMB004', 'AMB005'],
    'type': ['Advanced Life Support', 'Basic Life Support', 'Cardiac Care Unit']
})

# Create route data (simple straight lines for demo)
def create_route_data():
    routes = []
    for _, ambulance in ambulances_enroute.iterrows():
        route = {
            'path': [
                [ambulance['lon'], ambulance['lat']],
                [ambulance['destination_lon'], ambulance['destination_lat']]
            ],
            'ambulance_id': ambulance['ambulance_id'],
            'case_id': ambulance['case_id']
        }
        routes.append(route)
    return pd.DataFrame(routes)

route_data = create_route_data()

call_logs = pd.DataFrame({
    'time': ["09:00 AM", "10:15 AM", "11:00 AM", "12:30 PM", "01:45 PM"],
    'caller': ["John Doe", "Mary Roy", "Ravi Kumar", "Sarah Joseph", "Alex Thomas"],
    'location': ["MG Road", "Kowdiar", "Pattom", "Statue", "Kesavadasapuram"],
    'status': ["En Route", "Completed", "En Route", "Completed", "Dispatched"]
})

case_database = pd.DataFrame({
    'Case ID': ['CASE001', 'CASE002', 'CASE003', 'CASE004'],
    'Location': ['MG Road Junction', 'Kowdiar Palace', 'Pattom Signal', 'Statue Junction'],
    'Nature of Injury': ['Vehicle Accident', 'Heart Attack', 'Slip and Fall', 'Breathing Difficulty'],
    'Number of Patients': [2, 1, 1, 1],
    'Caller Details': ['John Doe, 9999999999', 'Mary Roy, 8888888888', 'Ravi K, 7777777777', 'Sarah J, 6666666666'],
    'Special Remarks': ['Multiple vehicles involved', 'Needs defibrillator', 'Elderly patient', 'Asthma patient'],
    'Status': ['Active', 'Active', 'Completed', 'Completed'],
    'Time Called': ['09:00 AM', '10:15 AM', '08:30 AM', '07:45 AM']
})

st.set_page_config(layout="wide", page_title="Emergency Services Dashboard")

# Sidebar
st.sidebar.title("🚨 Emergency Services Dashboard")
st.sidebar.markdown("---")
option = st.sidebar.radio(
    "Select a view:", 
    ["🚑 Ongoing Cases", "🏥 Available Ambulances", "📞 Call Logs and History", "📊 Database"]
)

if option == "🚑 Ongoing Cases":
    st.title("🚑 Ongoing Emergency Cases & En Route Ambulances")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Cases", len(ongoing_cases))
    with col2:
        st.metric("Ambulances En Route", len(ambulances_enroute))
    with col3:
        st.metric("Average ETA", "6.5 min")
    
    # Create the map
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v11',
        initial_view_state=pdk.ViewState(
            latitude=8.5241,
            longitude=76.9366,
            zoom=12,
            pitch=45,
        ),
        layers=[
            # Routes layer (lines from ambulance to destination)
            pdk.Layer(
                'PathLayer',
                data=route_data,
                get_path='path',
                get_color='[255, 165, 0, 200]',
                get_width=5,
                width_scale=1,
                pickable=True
            ),
            # Accident sites layer
            pdk.Layer(
                'ScatterplotLayer',
                data=ongoing_cases,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 200]',
                get_radius=150,
                pickable=True
            ),
            # Ambulances en route layer
            pdk.Layer(
                'IconLayer',
                data=ambulances_enroute,
                get_icon='ambulance',
                get_position='[lon, lat]',
                get_size=4,
                size_scale=15,
                pickable=True,
                icon_atlas='https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.png',
                icon_mapping={
                    'ambulance': {'x': 0, 'y': 0, 'width': 128, 'height': 128, 'mask': True}
                }
            )
        ],
        tooltip={
            "html": "<b>Case:</b> {case_id}<br/><b>Location:</b> {location}<br/><b>Ambulance:</b> {ambulance_id}<br/><b>Type:</b> {type}<br/><b>ETA:</b> {eta}",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }
    ))
    
    # Display current assignments
    st.subheader("Current Assignments")
    assignment_display = ambulances_enroute.merge(
        ongoing_cases, 
        left_on='case_id', 
        right_on='case_id', 
        suffixes=('_ambulance', '_case')
    )[['ambulance_id', 'type', 'case_id', 'location', 'severity', 'eta']]
    
    st.dataframe(assignment_display, use_container_width=True)

elif option == "🏥 Available Ambulances":
    st.title("🏥 Available Ambulances")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Available", len(available_ambulances))
    with col2:
        st.metric("Advanced Life Support", len(available_ambulances[available_ambulances['type'] == 'Advanced Life Support']))
    with col3:
        st.metric("Basic Life Support", len(available_ambulances[available_ambulances['type'] == 'Basic Life Support']))
    
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=8.5241,
            longitude=76.9366,
            zoom=12
        ),
        layers=[
            # Available ambulances layer
            pdk.Layer(
                'IconLayer',
                data=available_ambulances,
                get_icon='ambulance',
                get_position='[lon, lat]',
                get_size=4,
                size_scale=15,
                get_color='[0, 150, 0, 200]',
                pickable=True,
                icon_atlas='https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.png',
                icon_mapping={
                    'ambulance': {'x': 0, 'y': 0, 'width': 128, 'height': 128, 'mask': True}
                }
            )
        ],
        tooltip={
            "html": "<b>Ambulance:</b> {ambulance_id}<br/><b>Type:</b> {type}<br/><b>Status:</b> Available",
            "style": {"backgroundColor": "green", "color": "white"}
        }
    ))
    
    # Display available ambulances table
    st.subheader("Available Fleet Details")
    st.dataframe(available_ambulances, use_container_width=True)

elif option == "📞 Call Logs and History":
    st.title("📞 Today's Call Logs")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Calls", len(call_logs))
    with col2:
        st.metric("En Route", len(call_logs[call_logs['status'] == 'En Route']))
    with col3:
        st.metric("Completed", len(call_logs[call_logs['status'] == 'Completed']))
    with col4:
        st.metric("Dispatched", len(call_logs[call_logs['status'] == 'Dispatched']))
    
    # Style the dataframe based on status
    def highlight_status(row):
        if row.status == "En Route":
            return ["background-color: lightgreen"] * len(row)
        elif row.status == "Dispatched":
            return ["background-color: lightyellow"] * len(row)
        elif row.status == "Completed":
            return ["background-color: lightblue"] * len(row)
        else:
            return [""] * len(row)
    
    st.dataframe(
        call_logs.style.apply(highlight_status, axis=1),
        use_container_width=True
    )
    
    # Legend
    st.markdown("""
    **Status Legend:**
    - 🟢 **En Route**: Ambulance is on the way
    - 🟡 **Dispatched**: Ambulance has been assigned
    - 🔵 **Completed**: Case has been resolved
    """)

elif option == "📊 Database":
    st.title("📊 Case Database")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Cases", len(case_database))
    with col2:
        st.metric("Active Cases", len(case_database[case_database['Status'] == 'Active']))
    with col3:
        st.metric("Completed Cases", len(case_database[case_database['Status'] == 'Completed']))
    
    # Filter options
    st.subheader("Filters")
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Active", "Completed"])
    with col2:
        injury_filter = st.selectbox("Filter by Injury Type", ["All"] + list(case_database['Nature of Injury'].unique()))
    
    # Apply filters
    filtered_data = case_database.copy()
    if status_filter != "All":
        filtered_data = filtered_data[filtered_data['Status'] == status_filter]
    if injury_filter != "All":
        filtered_data = filtered_data[filtered_data['Nature of Injury'] == injury_filter]
    
    # Style active cases
    def highlight_active(row):
        if row.Status == "Active":
            return ["background-color: lightcoral"] * len(row)
        else:
            return [""] * len(row)
    
    st.dataframe(
        filtered_data.style.apply(highlight_active, axis=1),
        use_container_width=True
    )

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Last Updated:** " + datetime.now().strftime("%H:%M:%S"))
st.sidebar.markdown("**System Status:** 🟢 Online")
