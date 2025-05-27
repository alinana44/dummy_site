import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import datetime
import numpy as np

# Enhanced dummy data for ongoing cases (accident sites)
ongoing_cases = pd.DataFrame({
    'lat': [8.5241, 8.5180, 8.5290, 8.5160],
    'lon': [76.9366, 76.9290, 76.9420, 76.9250],
    'case_id': ['CASE001', 'CASE002', 'CASE005', 'CASE006'],
    'location': ['MG Road Junction', 'Kowdiar Palace', 'Thampanoor Railway Station', 'East Fort'],
    'severity': ['High', 'Medium', 'High', 'Low'],
    'description': ['Multi-vehicle accident', 'Cardiac emergency', 'Platform slip incident', 'Minor injury']
})

# Ambulances en route to cases - with different colors for different types
ambulances_enroute = pd.DataFrame({
    'lat': [8.5275, 8.5201, 8.5310, 8.5140],
    'lon': [76.9400, 76.9333, 76.9450, 76.9220],
    'ambulance_id': ['AMB001', 'AMB002', 'AMB007', 'AMB008'],
    'type': ['Advanced Life Support', 'Basic Life Support', 'Cardiac Care Unit', 'Basic Life Support'],
    'destination_lat': [8.5241, 8.5180, 8.5290, 8.5160],
    'destination_lon': [76.9366, 76.9290, 76.9420, 76.9250],
    'case_id': ['CASE001', 'CASE002', 'CASE005', 'CASE006'],
    'eta': ['3 min', '5 min', '7 min', '4 min'],
    'status': ['En Route', 'En Route', 'Dispatched', 'En Route']
})

# Enhanced available ambulances (not assigned) - more ambulances added
available_ambulances = pd.DataFrame({
    'lat': [8.5301, 8.5150, 8.5320, 8.5200, 8.5280, 8.5350, 8.5120, 8.5260, 8.5380, 8.5100],
    'lon': [76.9450, 76.9280, 76.9380, 76.9320, 76.9390, 76.9300, 76.9340, 76.9460, 76.9270, 76.9350],
    'ambulance_id': ['AMB003', 'AMB004', 'AMB005', 'AMB009', 'AMB010', 'AMB011', 'AMB012', 'AMB013', 'AMB014', 'AMB015'],
    'type': ['Advanced Life Support', 'Basic Life Support', 'Cardiac Care Unit', 'Basic Life Support', 
             'Advanced Life Support', 'Neonatal Transport', 'Trauma Unit', 'Basic Life Support',
             'Advanced Life Support', 'Mental Health Response'],
    'base_station': ['General Hospital', 'Medical College', 'Specialty Center', 'District Hospital',
                    'Private Hospital A', 'Maternity Center', 'Trauma Center', 'Community Health',
                    'Emergency Hub', 'Psychiatric Center']
})

# Create enhanced route data with curved paths for better visualization
def create_route_data():
    routes = []
    for _, ambulance in ambulances_enroute.iterrows():
        # Create curved path points for more realistic route visualization
        start_lat, start_lon = ambulance['lat'], ambulance['lon']
        end_lat, end_lon = ambulance['destination_lat'], ambulance['destination_lon']
        
        # Create intermediate points for curved path
        mid_lat = (start_lat + end_lat) / 2 + np.random.uniform(-0.002, 0.002)
        mid_lon = (start_lon + end_lon) / 2 + np.random.uniform(-0.002, 0.002)
        
        route = {
            'path': [
                [start_lon, start_lat],
                [mid_lon, mid_lat],
                [end_lon, end_lat]
            ],
            'ambulance_id': ambulance['ambulance_id'],
            'case_id': ambulance['case_id'],
            'status': ambulance['status'],
            'eta': ambulance['eta']
        }
        routes.append(route)
    return pd.DataFrame(routes)

route_data = create_route_data()

# Enhanced call logs
call_logs = pd.DataFrame({
    'time': ["07:30 AM", "08:15 AM", "09:00 AM", "10:15 AM", "11:00 AM", "12:30 PM", "01:45 PM", "02:20 PM"],
    'caller': ["Rajesh Kumar", "Priya Nair", "John Doe", "Mary Roy", "Ravi Kumar", "Sarah Joseph", "Alex Thomas", "Deepa Menon"],
    'location': ["Palayam", "Statue Junction", "MG Road", "Kowdiar", "Pattom", "East Fort", "Kesavadasapuram", "Thampanoor"],
    'status': ["Completed", "Completed", "En Route", "En Route", "Dispatched", "Completed", "En Route", "Dispatched"],
    'priority': ["Medium", "High", "High", "Medium", "Low", "Medium", "High", "Medium"]
})

# Enhanced case database
case_database = pd.DataFrame({
    'Case ID': ['CASE001', 'CASE002', 'CASE003', 'CASE004', 'CASE005', 'CASE006', 'CASE007', 'CASE008'],
    'Location': ['MG Road Junction', 'Kowdiar Palace', 'Pattom Signal', 'Statue Junction', 'Thampanoor Station', 'East Fort', 'Palayam', 'Medical College'],
    'Nature of Injury': ['Vehicle Accident', 'Heart Attack', 'Slip and Fall', 'Breathing Difficulty', 'Platform Accident', 'Minor Injury', 'Chest Pain', 'Emergency Surgery'],
    'Number of Patients': [2, 1, 1, 1, 1, 1, 1, 1],
    'Caller Details': ['John Doe, 9999999999', 'Mary Roy, 8888888888', 'Ravi K, 7777777777', 'Sarah J, 6666666666', 
                      'Station Master, 5555555555', 'Local Police, 4444444444', 'Rajesh K, 3333333333', 'Hospital Staff, 2222222222'],
    'Special Remarks': ['Multiple vehicles involved', 'Needs defibrillator', 'Elderly patient', 'Asthma patient',
                       'Railway platform incident', 'Walking difficulty', 'Cardiac symptoms', 'Critical condition'],
    'Status': ['Active', 'Active', 'Completed', 'Completed', 'Active', 'Active', 'Completed', 'Completed'],
    'Time Called': ['09:00 AM', '10:15 AM', '08:30 AM', '07:45 AM', '11:00 AM', '02:20 PM', '07:30 AM', '06:15 AM'],
    'Priority': ['High', 'Medium', 'Low', 'Medium', 'High', 'Low', 'High', 'High']
})

# Enhanced page configuration
st.set_page_config(
    layout="wide", 
    page_title="Unified Emergency Services Dashboard",
    page_icon="🚨",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    .dataframe {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
    }
    .status-active { 
        background-color: #ffebee !important; 
        color: #c62828 !important;
        font-weight: bold;
    }
    .status-enroute { 
        background-color: #e8f5e8 !important; 
        color: #2e7d32 !important;
        font-weight: bold;
    }
    .status-completed { 
        background-color: #e3f2fd !important; 
        color: #1565c0 !important;
        font-weight: bold;
    }
    .status-dispatched { 
        background-color: #fff3e0 !important; 
        color: #ef6c00 !important;
        font-weight: bold;
    }
    /* Enhanced table styling */
    .stDataFrame {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    /* Make all text in dataframes darker for better visibility */
    .stDataFrame td {
        color: #333333 !important;
        font-weight: 500;
    }
    .stDataFrame th {
        background-color: #f1f3f4 !important;
        color: #1f1f1f !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Sidebar
st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin-bottom: 1rem;'>
    <h2>🚨 Unified Emergency Dashboard</h2>
    <p>Real-time Emergency Response System</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
option = st.sidebar.radio(
    "Select a view:", 
    ["🚑 Live Operations Map", "🏥 Fleet Management", "📞 Call Center Logs", "📊 Case Database"]
)

# System status in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### System Status")
st.sidebar.markdown("🟢 **Emergency Services**: Online")
st.sidebar.markdown("🟢 **GPS Tracking**: Active")
st.sidebar.markdown("🟢 **Communication**: Connected")
st.sidebar.markdown(f"🕒 **Last Updated**: {datetime.now().strftime('%H:%M:%S')}")

if option == "🚑 Live Operations Map":
    st.markdown('<div class="main-header"><h1>🚑 Live Emergency Operations Dashboard</h1><p>Real-time tracking of ongoing cases and ambulance deployment</p></div>', unsafe_allow_html=True)
    
    # Enhanced metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🚨 Active Cases", len(ongoing_cases), delta=2)
    with col2:
        st.metric("🚑 En Route", len(ambulances_enroute[ambulances_enroute['status'] == 'En Route']), delta=1)
    with col3:
        st.metric("📋 Dispatched", len(ambulances_enroute[ambulances_enroute['status'] == 'Dispatched']), delta=-1)
    with col4:
        avg_eta = np.mean([int(eta.split()[0]) for eta in ambulances_enroute['eta']])
        st.metric("⏱️ Avg ETA", f"{avg_eta:.1f} min", delta=-0.5)
    
    # Enhanced map with multiple layers
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=pdk.ViewState(
            latitude=8.5241,
            longitude=76.9366,
            zoom=13,
            pitch=50,
            bearing=0
        ),
        layers=[
            # Routes layer with different colors based on status
            pdk.Layer(
                'PathLayer',
                data=route_data,
                get_path='path',
                get_color='[255, 165, 0, 200]',  # Orange for en route
                get_width=8,
                width_scale=1,
                pickable=True
            ),
            # Emergency sites layer with pulsing effect
            pdk.Layer(
                'ScatterplotLayer',
                data=ongoing_cases,
                get_position='[lon, lat]',
                get_color='[255, 0, 0, 220]',  # Bright red for emergencies
                get_radius=200,
                pickable=True,
                stroked=True,
                get_line_color='[255, 255, 255, 255]',
                get_line_width=3
            ),
            # En route ambulances
            pdk.Layer(
                'ScatterplotLayer',
                data=ambulances_enroute[ambulances_enroute['status'] == 'En Route'],
                get_position='[lon, lat]',
                get_color='[0, 255, 0, 200]',  # Green for en route
                get_radius=120,
                pickable=True
            ),
            # Dispatched ambulances
            pdk.Layer(
                'ScatterplotLayer',
                data=ambulances_enroute[ambulances_enroute['status'] == 'Dispatched'],
                get_position='[lon, lat]',
                get_color='[255, 140, 0, 200]',  # Orange for dispatched
                get_radius=120,
                pickable=True
            )
        ],
        tooltip={
            "html": """
            <div style="background: rgba(0,0,0,0.8); color: white; padding: 10px; border-radius: 5px;">
                <b>🚑 Ambulance:</b> {ambulance_id}<br/>
                <b>📍 Case:</b> {case_id}<br/>
                <b>🏥 Type:</b> {type}<br/>
                <b>⏰ ETA:</b> {eta}<br/>
                <b>📊 Status:</b> {status}
            </div>
            """,
            "style": {"backgroundColor": "rgba(0,0,0,0.8)", "color": "white"}
        }
    ))
    
    # Current assignments with enhanced styling
    st.subheader("🎯 Current Emergency Assignments")
    assignment_display = ambulances_enroute.merge(
        ongoing_cases, 
        left_on='case_id', 
        right_on='case_id', 
        suffixes=('_ambulance', '_case')
    )[['ambulance_id', 'type', 'case_id', 'location', 'severity', 'eta', 'status', 'description']]
    
    st.dataframe(assignment_display, use_container_width=True)

elif option == "🏥 Fleet Management":
    st.markdown('<div class="main-header"><h1>🏥 Fleet Management System</h1><p>Complete overview of available emergency vehicles</p></div>', unsafe_allow_html=True)
    
    # Enhanced metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🚑 Total Available", len(available_ambulances))
    with col2:
        als_count = len(available_ambulances[available_ambulances['type'] == 'Advanced Life Support'])
        st.metric("🏥 Advanced LS", als_count)
    with col3:
        bls_count = len(available_ambulances[available_ambulances['type'] == 'Basic Life Support'])
        st.metric("🚐 Basic LS", bls_count)
    with col4:
        specialty_count = len(available_ambulances) - als_count - bls_count
        st.metric("⚕️ Specialty Units", specialty_count)
    
    # Enhanced map for available ambulances
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v10',
        initial_view_state=pdk.ViewState(
            latitude=8.5241,
            longitude=76.9366,
            zoom=12,
            pitch=30
        ),
        layers=[
            # Available ambulances with different colors by type
            pdk.Layer(
                'ScatterplotLayer',
                data=available_ambulances,
                get_position='[lon, lat]',
                get_color=[
                    'type == "Advanced Life Support" ? [0, 150, 0, 200] : '
                    'type == "Basic Life Support" ? [0, 100, 255, 200] : '
                    '[128, 0, 128, 200]'
                ],
                get_radius=100,
                pickable=True,
                stroked=True,
                get_line_color='[255, 255, 255, 200]',
                get_line_width=2
            )
        ],
        tooltip={
            "html": """
            <div style="background: rgba(0,100,0,0.9); color: white; padding: 10px; border-radius: 5px;">
                <b>🚑 ID:</b> {ambulance_id}<br/>
                <b>🏥 Type:</b> {type}<br/>
                <b>🏢 Base:</b> {base_station}<br/>
                <b>✅ Status:</b> Available
            </div>
            """,
            "style": {"backgroundColor": "rgba(0,100,0,0.9)", "color": "white"}
        }
    ))
    
    # Fleet details with filtering
    st.subheader("🚑 Fleet Details & Management")
    
    col1, col2 = st.columns(2)
    with col1:
        type_filter = st.selectbox("Filter by Type", ["All"] + list(available_ambulances['type'].unique()))
    with col2:
        base_filter = st.selectbox("Filter by Base Station", ["All"] + list(available_ambulances['base_station'].unique()))
    
    filtered_ambulances = available_ambulances.copy()
    if type_filter != "All":
        filtered_ambulances = filtered_ambulances[filtered_ambulances['type'] == type_filter]
    if base_filter != "All":
        filtered_ambulances = filtered_ambulances[filtered_ambulances['base_station'] == base_filter]
    
    st.dataframe(filtered_ambulances, use_container_width=True)

elif option == "📞 Call Center Logs":
    st.markdown('<div class="main-header"><h1>📞 Emergency Call Center</h1><p>Real-time call management and dispatch logs</p></div>', unsafe_allow_html=True)
    
    # Enhanced call metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📞 Total Calls Today", len(call_logs))
    with col2:
        enroute_count = len(call_logs[call_logs['status'] == 'En Route'])
        st.metric("🚑 En Route", enroute_count)
    with col3:
        completed_count = len(call_logs[call_logs['status'] == 'Completed'])
        st.metric("✅ Completed", completed_count)
    with col4:
        dispatched_count = len(call_logs[call_logs['status'] == 'Dispatched'])
        st.metric("📋 Dispatched", dispatched_count)
    
    # Enhanced call logs with priority
    def style_call_logs(row):
        if row.status == "En Route":
            return ["background-color: #c8e6c9; color: #2e7d32; font-weight: bold"] * len(row)
        elif row.status == "Dispatched":
            return ["background-color: #fff3e0; color: #ef6c00; font-weight: bold"] * len(row)
        elif row.status == "Completed":
            return ["background-color: #e3f2fd; color: #1565c0; font-weight: bold"] * len(row)
        else:
            return ["color: #333333; font-weight: 500"] * len(row)
    
    st.subheader("📋 Today's Emergency Calls")
    st.dataframe(
        call_logs.style.apply(style_call_logs, axis=1),
        use_container_width=True
    )
    
    # Status legend with colors
    st.markdown("""
    **📊 Status Legend:**
    - 🟢 **En Route**: Ambulance responding to emergency
    - 🟡 **Dispatched**: Unit assigned, preparing to respond  
    - 🔵 **Completed**: Emergency resolved successfully
    - 🔴 **High Priority**: Critical emergency requiring immediate response
    """)

elif option == "📊 Case Database":
    st.markdown('<div class="main-header"><h1>📊 Emergency Case Database</h1><p>Comprehensive case management and tracking system</p></div>', unsafe_allow_html=True)
    
    # Enhanced database metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📋 Total Cases", len(case_database))
    with col2:
        active_count = len(case_database[case_database['Status'] == 'Active'])
        st.metric("🔴 Active Cases", active_count)
    with col3:
        completed_count = len(case_database[case_database['Status'] == 'Completed'])
        st.metric("✅ Completed", completed_count)
    with col4:
        high_priority = len(case_database[case_database['Priority'] == 'High'])
        st.metric("⚡ High Priority", high_priority)
    
    # Enhanced filtering
    st.subheader("🔍 Case Filters")
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Active", "Completed"])
    with col2:
        injury_filter = st.selectbox("Filter by Injury Type", ["All"] + list(case_database['Nature of Injury'].unique()))
    with col3:
        priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    
    # Apply filters
    filtered_data = case_database.copy()
    if status_filter != "All":
        filtered_data = filtered_data[filtered_data['Status'] == status_filter]
    if injury_filter != "All":
        filtered_data = filtered_data[filtered_data['Nature of Injury'] == injury_filter]
    if priority_filter != "All":
        filtered_data = filtered_data[filtered_data['Priority'] == priority_filter]
    
    # Enhanced styling for case database
    def highlight_cases(row):
        if row.Status == "Active" and row.Priority == "High":
            return ["background-color: #ffcdd2; color: #c62828; font-weight: bold"] * len(row)  # Red for active high priority
        elif row.Status == "Active":
            return ["background-color: #fff3e0; color: #ef6c00; font-weight: bold"] * len(row)  # Orange for active
        elif row.Status == "Completed":
            return ["background-color: #e8f5e8; color: #2e7d32; font-weight: bold"] * len(row)  # Green for completed
        else:
            return ["color: #333333; font-weight: 500"] * len(row)
    
    st.subheader("📋 Case Records")
    st.dataframe(
        filtered_data.style.apply(highlight_cases, axis=1),
        use_container_width=True
    )

# Enhanced footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 🏥 Emergency Contacts")
st.sidebar.markdown("**Fire Department**: 101")
st.sidebar.markdown("**Police**: 100") 
st.sidebar.markdown("**Medical Emergency**: 108")
st.sidebar.markdown("**Disaster Management**: 1077")
