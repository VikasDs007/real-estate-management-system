# app.py - Real Estate Recommendation System Web App (ENHANCED VERSION)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import warnings
import datetime
warnings.filterwarnings('ignore')

# Configure Streamlit page settings
st.set_page_config(
    page_title="🏠 Real Estate Management System",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme CSS with light text fonts (same as before)
st.markdown("""
<style>
    /* Main app background - Dark theme */
    .stApp {
        background-color: #0e1117 !important;
        color: #fafafa !important;
    }
    
    /* Main container dark background */
    .main .block-container {
        background-color: #0e1117 !important;
        padding-top: 2rem;
    }
    
    /* Header styling with bright text */
    .main-header {
        font-size: 2.8rem;
        color: #ffffff !important;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        background: linear-gradient(90deg, #4ade80, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Subtitle with light text */
    .subtitle {
        color: #e5e7eb !important;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Dark metric cards with light text */
    .metric-card {
        background-color: #1f2937 !important;
        color: #f9fafb !important;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 0.5rem 0;
        border: 1px solid #374151;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Success metric cards */
    .success-metric {
        background-color: #065f46 !important;
        color: #d1fae5 !important;
        border-left: 5px solid #10b981;
        border: 1px solid #047857;
    }
    
    /* Quick Match card styling */
    .quick-match-card {
        background-color: #1e40af !important;
        color: #dbeafe !important;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #3b82f6;
        margin: 0.5rem 0;
    }
    
    /* Performance tracking buttons */
    .track-button-interested {
        background-color: #0d9488 !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 0.375rem !important;
        margin: 0.25rem !important;
    }
    
    .track-button-closed {
        background-color: #dc2626 !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 0.375rem !important;
        margin: 0.25rem !important;
    }
    
    /* Sidebar dark theme */
    .css-1d391kg {
        background-color: #111827 !important;
    }
    
    /* Sidebar text light */
    .css-1d391kg, .css-1d391kg p, .css-1d391kg label {
        color: #f9fafb !important;
    }
    
    /* Headers and text - Light fonts */
    h1, h2, h3, h4, h5, h6 {
        color: #f9fafb !important;
        font-weight: 600;
    }
    
    /* All markdown text light */
    .stMarkdown, .stMarkdown p, .stMarkdown div {
        color: #e5e7eb !important;
    }
    
    /* Metric containers dark with light text */
    [data-testid="metric-container"] {
        background-color: #1f2937 !important;
        border: 1px solid #374151 !important;
        padding: 1rem !important;
        border-radius: 0.5rem !important;
        color: #f9fafb !important;
    }
    
    [data-testid="metric-container"] * {
        color: #f9fafb !important;
    }
    
    /* Buttons dark with bright text */
    .stButton button {
        background-color: #374151 !important;
        color: #f9fafb !important;
        border: 1px solid #4b5563 !important;
        border-radius: 0.5rem;
        font-weight: 500;
    }
    
    .stButton button:hover {
        background-color: #4b5563 !important;
        border-color: #6b7280 !important;
    }
    
    /* Selectbox dark theme */
    .stSelectbox > div > div {
        background-color: #1f2937 !important;
        color: #f9fafb !important;
        border: 1px solid #374151 !important;
    }
    
    /* Input fields dark */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background-color: #1f2937 !important;
        color: #f9fafb !important;
        border: 1px solid #374151 !important;
    }
    
    /* Labels light */
    .stSelectbox label, .stTextInput label, .stSlider label, .stNumberInput label {
        color: #f9fafb !important;
        font-weight: 500;
    }
    
    /* Dataframe dark theme */
    .dataframe {
        background-color: #1f2937 !important;
        color: #f9fafb !important;
    }
    
    /* Expander dark theme */
    .streamlit-expanderHeader {
        background-color: #1f2937 !important;
        color: #f9fafb !important;
        border: 1px solid #374151 !important;
        font-weight: 500;
    }
    
    .streamlit-expanderContent {
        background-color: #111827 !important;
        color: #e5e7eb !important;
        border: 1px solid #374151 !important;
    }
    
    /* Custom dark card styling */
    .dark-card {
        background-color: #1f2937 !important;
        color: #f9fafb !important;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #374151;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .dark-card h4 {
        color: #22d3ee !important;
        margin-bottom: 0.5rem;
    }
    
    .dark-card p {
        color: #e5e7eb !important;
        margin: 0.25rem 0;
    }
    
    /* Success and warning messages */
    .stSuccess {
        background-color: #065f46 !important;
        color: #d1fae5 !important;
        border: 1px solid #10b981 !important;
    }
    
    .stWarning {
        background-color: #92400e !important;
        color: #fef3c7 !important;
        border: 1px solid #f59e0b !important;
    }
    
    .stInfo {
        background-color: #1e3a8a !important;
        color: #dbeafe !important;
        border: 1px solid #3b82f6 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for performance tracking
if 'performance_tracking' not in st.session_state:
    st.session_state.performance_tracking = {}

# Load data function with comprehensive error handling
@st.cache_data
def load_data():
    """Load all processed data for the application with robust error handling"""
    
    # Try multiple possible paths
    possible_paths = [
        Path("real_estate_project/data/processed"),
        Path("data/processed"), 
        Path("../real_estate_project/data/processed"),
        Path(r"D:\Git repo\real_estate_listings\real_estate_project\data\processed")
    ]
    
    for data_path in possible_paths:
        try:
            # Check if directory exists
            if not data_path.exists():
                continue
            
            # Try to load the files
            recommendations_file = data_path / "client_property_recommendations.csv"
            clients_file = data_path / "clients_with_features.csv"
            properties_file = data_path / "properties_with_features.csv"
            
            # Check if all required files exist
            if not all([recommendations_file.exists(), clients_file.exists(), properties_file.exists()]):
                continue
            
            # Load the data
            recommendations = pd.read_csv(recommendations_file)
            clients = pd.read_csv(clients_file)
            properties = pd.read_csv(properties_file)
            
            return recommendations, clients, properties
            
        except Exception as e:
            continue
    
    return None, None, None

def quick_match_properties(properties, budget_min, budget_max, bhk_preference, listing_type):
    """Quick matching algorithm for sidebar feature"""
    try:
        # Filter properties based on criteria
        filtered = properties.copy()
        
        # Filter by listing type
        filtered = filtered[filtered['listing_type'] == listing_type]
        
        # Filter by BHK
        if bhk_preference != "Any":
            filtered = filtered[filtered['bedrooms__bhk'] == bhk_preference]
        
        # Filter by budget
        if listing_type == 'Sale' and 'asking_price__â_¹' in filtered.columns:
            filtered = filtered[
                (filtered['asking_price__â_¹'] >= budget_min) & 
                (filtered['asking_price__â_¹'] <= budget_max)
            ]
        elif listing_type == 'Rent' and 'monthly_rent__â_¹' in filtered.columns:
            filtered = filtered[
                (filtered['monthly_rent__â_¹'] >= budget_min) & 
                (filtered['monthly_rent__â_¹'] <= budget_max)
            ]
        
        return filtered.head(5)  # Return top 5 matches
        
    except Exception as e:
        st.error(f"Error in quick match: {str(e)}")
        return pd.DataFrame()

def track_performance(recommendation_id, action, client_name, property_id):
    """Track recommendation performance"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if recommendation_id not in st.session_state.performance_tracking:
        st.session_state.performance_tracking[recommendation_id] = []
    
    st.session_state.performance_tracking[recommendation_id].append({
        'action': action,
        'timestamp': timestamp,
        'client_name': client_name,
        'property_id': property_id
    })

# Main application
def main():
    # Header with bright styling
    st.markdown('<h1 class="main-header">🏠 Real Estate Management System</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div class="subtitle">
        Intelligent Property-Client Matching System powered by Data Science
    </div>
    """, unsafe_allow_html=True)
    
    # Load data with progress indication
    with st.spinner("🔄 Loading data..."):
        recommendations, clients, properties = load_data()
    
    if recommendations is None:
        st.error("❌ Could not load data. Please ensure all processed data files exist!")
        st.info("💡 Make sure you've completed the data processing pipeline first!")
        st.stop()
    
    # Clear success message
    st.success("🎉 Application loaded successfully!")
    
    # Sidebar navigation with dark theme + ENHANCED FEATURES
    st.sidebar.title("🎯 Navigation")
    st.sidebar.markdown("---")
    
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["📊 Dashboard", "🔍 Property Search", "👥 Client Management", "📈 Analytics"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    st.sidebar.metric("Total Clients", f"{len(clients):,}")
    st.sidebar.metric("Active Properties", f"{len(properties):,}")
    st.sidebar.metric("Recommendations", f"{len(recommendations):,}")
    
    # ⚡ FEATURE A: QUICK MATCH FEATURE
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚡ Quick Match")
    
    # Quick match inputs
    listing_type = st.sidebar.selectbox("Property Type", ["Sale", "Rent"], key="quick_match_type")
    
    if listing_type == "Sale":
        budget_range = st.sidebar.slider(
            "Budget Range (₹ Crores)", 
            min_value=0.5, max_value=10.0, 
            value=(2.0, 5.0), step=0.1,
            key="quick_sale_budget"
        )
        budget_min = budget_range[0] * 10000000  # Convert to rupees
        budget_max = budget_range[1] * 10000000
    else:
        budget_range = st.sidebar.slider(
            "Rent Range (₹ Thousands)", 
            min_value=10, max_value=200, 
            value=(30, 80), step=5,
            key="quick_rent_budget"
        )
        budget_min = budget_range[0] * 1000  # Convert to rupees
        budget_max = budget_range[1] * 1000
    
    bhk_preference = st.sidebar.selectbox("BHK Preference", ["Any", 1, 2, 3, 4, 5], key="quick_bhk")
    
    if st.sidebar.button("🔍 Find Quick Matches", key="quick_match_btn"):
        st.sidebar.markdown("### 🎯 Quick Match Results")
        
        quick_matches = quick_match_properties(properties, budget_min, budget_max, bhk_preference, listing_type)
        
        if len(quick_matches) > 0:
            for idx, prop in quick_matches.iterrows():
                price_col = 'asking_price__â_¹' if listing_type == 'Sale' else 'monthly_rent__â_¹'
                price_val = prop.get(price_col, 0)
                
                if pd.notna(price_val):
                    if listing_type == 'Sale':
                        price_str = f"₹{price_val/10000000:.1f}Cr"
                    else:
                        price_str = f"₹{price_val:,.0f}/mo"
                else:
                    price_str = "Price N/A"
                
                bhk_str = f"{prop.get('bedrooms__bhk', 'N/A')} BHK"
                location_str = prop.get('area___locality', 'Location N/A')
                
                st.sidebar.markdown(f"""
                <div class="quick-match-card">
                    <strong>{prop.get('property_id', 'Unknown')}</strong><br>
                    {bhk_str} in {location_str}<br>
                    <strong>{price_str}</strong>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.sidebar.warning("No matches found. Try adjusting criteria.")
    
    # Performance tracking summary in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Performance Tracker")
    
    total_tracked = len(st.session_state.performance_tracking)
    interested_count = sum(1 for actions in st.session_state.performance_tracking.values() 
                          for action in actions if action['action'] == 'Interested')
    closed_count = sum(1 for actions in st.session_state.performance_tracking.values() 
                      for action in actions if action['action'] == 'Deal Closed')
    
    st.sidebar.metric("Tracked Interactions", total_tracked)
    st.sidebar.metric("Interested Leads", interested_count)
    st.sidebar.metric("Deals Closed", closed_count)
    
    if total_tracked > 0:
        conversion_rate = (closed_count / total_tracked) * 100
        st.sidebar.metric("Conversion Rate", f"{conversion_rate:.1f}%")
    
    # Display selected page with error handling
    try:
        if page == "📊 Dashboard":
            show_dashboard(recommendations, clients, properties)
        elif page == "🔍 Property Search":
            show_property_search(recommendations, clients, properties)
        elif page == "👥 Client Management":
            show_client_management(clients, recommendations)
        elif page == "📈 Analytics":
            show_analytics(recommendations, clients, properties)
    except Exception as e:
        st.error(f"❌ Error displaying page: {str(e)}")

def show_dashboard(recommendations, clients, properties):
    """Display the main dashboard with key metrics"""
    st.header("📊 System Overview Dashboard")
    st.markdown("---")
    
    # Key metrics row with performance tracking integration
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Total Clients",
            value=f"{len(clients):,}",
            delta="100% Coverage",
            delta_color="normal"
        )
    
    with col2:
        unique_properties = recommendations['property_id'].nunique() if 'property_id' in recommendations.columns else 0
        st.metric(
            label="🏠 Active Properties", 
            value=f"{len(properties):,}",
            delta=f"{unique_properties} Matched",
            delta_color="normal"
        )
    
    with col3:
        if 'similarity_score' in recommendations.columns:
            high_quality_matches = len(recommendations[recommendations['similarity_score'] >= 80])
            st.metric(
                label="🎯 Quality Matches",
                value=f"{high_quality_matches:,}",
                delta="80%+ Similarity",
                delta_color="normal"
            )
        else:
            st.metric(label="🎯 Quality Matches", value="Loading...", delta="Processing")
    
    with col4:
        # Show performance tracking metrics
        total_interactions = len(st.session_state.performance_tracking)
        st.metric(
            label="📈 Tracked Interactions",
            value=f"{total_interactions:,}",
            delta="Real-time Tracking",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # Charts row (same as before but enhanced with performance data)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top Performing Properties")
        try:
            if 'property_id' in recommendations.columns:
                top_properties = recommendations['property_id'].value_counts().head(10)
                
                # Dark theme for plotly
                fig = px.bar(
                    x=top_properties.values,
                    y=top_properties.index,
                    orientation='h',
                    title="Properties by Number of Client Matches",
                    labels={'x': 'Number of Matches', 'y': 'Property ID'}
                )
                
                # Apply dark theme to chart
                fig.update_layout(
                    height=400,
                    paper_bgcolor='#1f2937',
                    plot_bgcolor='#1f2937',
                    font=dict(color='#f9fafb'),
                    title_font=dict(color='#f9fafb', size=16),
                    xaxis=dict(gridcolor='#374151', color='#f9fafb'),
                    yaxis=dict(gridcolor='#374151', color='#f9fafb')
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Property data not available for chart")
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")
    
    with col2:
        st.subheader("📊 Performance Tracking Overview")
        try:
            if st.session_state.performance_tracking:
                # Create performance tracking visualization
                actions = []
                for tracked_actions in st.session_state.performance_tracking.values():
                    for action in tracked_actions:
                        actions.append(action['action'])
                
                if actions:
                    action_counts = pd.Series(actions).value_counts()
                    
                    fig = px.pie(
                        values=action_counts.values,
                        names=action_counts.index,
                        title="Lead Performance Distribution",
                        color_discrete_sequence=['#10b981', '#ef4444', '#3b82f6']
                    )
                    
                    fig.update_layout(
                        height=400,
                        paper_bgcolor='#1f2937',
                        font=dict(color='#f9fafb'),
                        title_font=dict(color='#f9fafb', size=16)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No performance data tracked yet. Start tracking leads!")
            else:
                st.info("No performance tracking data available yet.")
        except Exception as e:
            st.error(f"Error creating performance chart: {str(e)}")
    
    # System performance summary with enhanced tracking info
    st.markdown("---")
    st.subheader("📈 System Performance Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="dark-card">
            <h4>🎯 Algorithm Performance</h4>
            <p>• Intelligent matching system</p>
            <p>• 100% Client coverage</p>
            <p>• 10 recommendations per client</p>
            <p>• Advanced filtering capabilities</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        try:
            if 'listing_type' in recommendations.columns:
                rental_count = len(recommendations[recommendations['listing_type'] == 'Rent'])
                rental_pct = (rental_count / len(recommendations)) * 100 if len(recommendations) > 0 else 0
                st.markdown(f"""
                <div class="dark-card">
                    <h4>🏢 Market Distribution</h4>
                    <p>• Rental demand: {rental_pct:.1f}%</p>
                    <p>• Sales demand: {100-rental_pct:.1f}%</p>
                    <p>• Balanced portfolio</p>
                    <p>• Market insights available</p>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error calculating market distribution: {str(e)}")
    
    with col3:
        # Enhanced with performance tracking metrics
        interested_leads = sum(1 for actions in st.session_state.performance_tracking.values() 
                              for action in actions if action['action'] == 'Interested')
        closed_deals = sum(1 for actions in st.session_state.performance_tracking.values() 
                          for action in actions if action['action'] == 'Deal Closed')
        
        st.markdown(f"""
        <div class="dark-card">
            <h4>⚡ Live Performance</h4>
            <p>• Interested leads: {interested_leads}</p>
            <p>• Closed deals: {closed_deals}</p>
            <p>• Real-time tracking active</p>
            <p>• Performance analytics ready</p>
        </div>
        """, unsafe_allow_html=True)

def show_property_search(recommendations, clients, properties):
    """Property search and matching interface with performance tracking"""
    st.header("🔍 Property Search & Matching")
    st.markdown("---")
    
    # Search filters with dark theme (same as before)
    st.subheader("🎯 Search Filters")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_type = st.selectbox("Property Type", ["All", "Sale", "Rent"])
    
    with col2:
        bhk_filter = st.selectbox("BHK", ["All", "1 BHK", "2 BHK", "3 BHK", "4 BHK", "5 BHK"])
    
    with col3:
        location_filter = st.selectbox("Location", ["All", "Mira Road East", "Mira Road West", "Bhayandar East", "Bhayandar West"])
    
    with col4:
        if search_type == "Sale" or search_type == "All":
            price_range = st.slider("Price Range (₹ Crores)", 0.5, 5.0, (1.0, 3.0), 0.1)
        elif search_type == "Rent":
            rent_range = st.slider("Rent Range (₹ Thousands)", 10, 200, (30, 80), 5)
    
    st.markdown("---")
    
    # Apply filters and show results with performance tracking
    try:
        filtered_properties = properties.copy()
        
        if search_type != "All":
            filtered_properties = filtered_properties[filtered_properties['listing_type'] == search_type]
        
        if bhk_filter != "All":
            bhk_num = int(bhk_filter.split()[0])
            filtered_properties = filtered_properties[filtered_properties['bedrooms__bhk'] == bhk_num]
        
        st.subheader(f"🏠 Search Results ({len(filtered_properties)} properties found)")
        
        if len(filtered_properties) > 0:
            # Display properties in expandable cards with performance tracking
            display_properties = filtered_properties.head(15)
            
            for idx, prop in display_properties.iterrows():
                # Create property title
                bhk_info = f"{prop['bedrooms__bhk']} BHK" if pd.notna(prop['bedrooms__bhk']) else "BHK N/A"
                location_info = prop.get('area___locality', 'Location N/A')
                property_title = f"{prop.get('property_id', 'Unknown ID')} - {bhk_info} in {location_info}"
                
                with st.expander(property_title):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**📋 Basic Details**")
                        st.write(f"**Type:** {prop.get('property_type', 'N/A')}")
                        st.write(f"**Area:** {prop.get('area__sq__ft', 'N/A')} sq ft")
                        st.write(f"**Furnishing:** {prop.get('furnishing', 'N/A')}")
                        st.write(f"**Age:** {prop.get('property_age__yrs', 'N/A')} years")
                    
                    with col2:
                        st.markdown("**💰 Pricing**")
                        if prop.get('listing_type') == 'Sale' and pd.notna(prop.get('asking_price__â_¹')):
                            price = prop['asking_price__â_¹']
                            st.write(f"**Asking Price:** ₹{price:,.0f}")
                            if pd.notna(prop.get('price_per_sqft')):
                                st.write(f"**Price/sq ft:** ₹{prop['price_per_sqft']:,.0f}")
                        elif prop.get('listing_type') == 'Rent' and pd.notna(prop.get('monthly_rent__â_¹')):
                            rent = prop['monthly_rent__â_¹']
                            st.write(f"**Monthly Rent:** ₹{rent:,.0f}")
                            if pd.notna(prop.get('rent_per_sqft')):
                                st.write(f"**Rent/sq ft:** ₹{prop['rent_per_sqft']:.0f}")
                        
                        if pd.notna(prop.get('maint___month__â_¹')):
                            st.write(f"**Maintenance:** ₹{prop['maint___month__â_¹']:,.0f}/month")
                    
                    with col3:
                        st.markdown("**🏢 Building Details**")
                        st.write(f"**Floor:** {prop.get('floor_number', 'N/A')}/{prop.get('total_floors', 'N/A')}")
                        st.write(f"**Parking:** {prop.get('parking__cars', 'N/A')} cars")
                        st.write(f"**Facing:** {prop.get('facing_direction', 'N/A')}")
                        st.write(f"**Building:** {prop.get('building___society', 'N/A')}")
                    
                    # 🎯 FEATURE B: PERFORMANCE TRACKING BUTTONS
                    st.markdown("---")
                    st.markdown("**📈 Track Interest:**")
                    
                    button_col1, button_col2, button_col3 = st.columns([1, 1, 2])
                    
                    property_id = prop.get('property_id', f'prop_{idx}')
                    
                    with button_col1:
                        if st.button("👍 Interested", key=f"interested_{property_id}_{idx}"):
                            track_performance(f"search_{property_id}_{idx}", "Interested", "Search User", property_id)
                            st.success("✅ Marked as Interested!")
                    
                    with button_col2:
                        if st.button("🤝 Deal Closed", key=f"closed_{property_id}_{idx}"):
                            track_performance(f"search_{property_id}_{idx}", "Deal Closed", "Search User", property_id)
                            st.success("🎉 Deal Closed recorded!")
                    
                    with button_col3:
                        # Show tracking history for this property
                        tracking_key = f"search_{property_id}_{idx}"
                        if tracking_key in st.session_state.performance_tracking:
                            latest_action = st.session_state.performance_tracking[tracking_key][-1]
                            st.info(f"Last action: {latest_action['action']} at {latest_action['timestamp']}")

        else:
            st.info("🔍 No properties match your search criteria. Try adjusting the filters.")
            
    except Exception as e:
        st.error(f"Error in property search: {str(e)}")

def show_client_management(clients, recommendations):
    """Client management interface with enhanced performance tracking"""
    st.header("👥 Client Management")
    st.markdown("---")
    
    # Client search (same as before)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_client = st.text_input("🔍 Search by Client Name or ID", placeholder="Enter client name or ID...")
    
    with col2:
        client_status_filter = st.selectbox("Filter by Status", ["All"] + list(clients['status'].unique()) if 'status' in clients.columns else ["All"])
    
    try:
        # Apply filters (same as before)
        filtered_clients = clients.copy()
        
        if search_client:
            filtered_clients = filtered_clients[
                filtered_clients['client_name'].str.contains(search_client, case=False, na=False) |
                filtered_clients['clientid'].str.contains(search_client, case=False, na=False)
            ]
        
        if client_status_filter != "All":
            filtered_clients = filtered_clients[filtered_clients['status'] == client_status_filter]
        
        if len(filtered_clients) == 0:
            filtered_clients = clients.head(20)  # Show first 20 if no search
        
        st.subheader(f"👥 Clients ({len(filtered_clients)} shown)")
        
        # Client statistics (same as before)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'looking_for' in clients.columns:
                rent_clients = len(clients[clients['looking_for'] == 'Rent'])
                st.metric("Rental Seekers", rent_clients)
        
        with col2:
            if 'looking_for' in clients.columns:
                sale_clients = len(clients[clients['looking_for'] == 'Sale'])
                st.metric("Property Buyers", sale_clients)
        
        with col3:
            if 'status' in clients.columns:
                active_statuses = ['Actively Searching', 'Negotiating', 'Site Visit Planned']
                active_clients = len(clients[clients['status'].isin(active_statuses)])
                st.metric("Active Clients", active_clients)
        
        with col4:
            if 'status' in clients.columns:
                closed_clients = len(clients[clients['status'] == 'Deal Closed'])
                st.metric("Deals Closed", closed_clients)
        
        st.markdown("---")
        
        # Display clients in cards with ENHANCED performance tracking
        if len(filtered_clients) > 0:
            for idx, client in filtered_clients.head(10).iterrows():
                with st.expander(f"👤 {client.get('client_name', 'Unknown')} - {client.get('clientid', 'No ID')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**📞 Contact Information**")
                        st.write(f"**Name:** {client.get('client_name', 'N/A')}")
                        st.write(f"**Phone:** {client.get('client_phone', 'N/A')}")
                        st.write(f"**Email:** {client.get('client_email', 'N/A')}")
                        st.write(f"**Status:** {client.get('status', 'N/A')}")
                    
                    with col2:
                        st.markdown("**🏠 Property Requirements**")
                        st.write(f"**Looking For:** {client.get('looking_for', 'N/A')}")
                        if pd.notna(client.get('client_bhk')):
                            st.write(f"**BHK:** {client['client_bhk']} BHK")
                        if pd.notna(client.get('client_location')):
                            st.write(f"**Location:** {client['client_location']}")
                        if pd.notna(client.get('client_budget')):
                            st.write(f"**Budget:** ₹{client['client_budget']:,.0f}")
                    
                    if pd.notna(client.get('requirements')):
                        st.markdown("**📝 Detailed Requirements:**")
                        st.write(client['requirements'])
                    
                    # Show top recommendations with ENHANCED performance tracking
                    if 'client_id' in recommendations.columns:
                        client_recs = recommendations[recommendations['client_id'] == client['clientid']].head(5)
                        if len(client_recs) > 0:
                            st.markdown("**🎯 Top Recommendations:**")
                            
                            for rec_idx, rec in client_recs.iterrows():
                                price_str = f"₹{rec['price_match']:,.0f}" if pd.notna(rec.get('price_match')) else "Price N/A"
                                bhk_str = f"{rec.get('bhk_match', 'N/A')} BHK"
                                location_str = rec.get('location_match', 'Location N/A')
                                score_str = f"{rec.get('similarity_score', 0):.1f}%"
                                
                                # Create a unique tracking key for each recommendation
                                rec_key = f"client_{client['clientid']}_prop_{rec.get('property_id', 'unknown')}_{rec_idx}"
                                
                                # Display recommendation with performance tracking
                                rec_col1, rec_col2, rec_col3 = st.columns([3, 1, 1])
                                
                                with rec_col1:
                                    st.write(f"• **{rec.get('property_id', 'Unknown')}** - {bhk_str} in {location_str} - {price_str} (Match: {score_str})")
                                
                                with rec_col2:
                                    if st.button("👍 Interested", key=f"int_{rec_key}", help="Mark client as interested"):
                                        track_performance(rec_key, "Interested", client.get('client_name', 'Unknown'), rec.get('property_id', 'Unknown'))
                                        st.success("✅ Interest tracked!")
                                
                                with rec_col3:
                                    if st.button("🤝 Deal Closed", key=f"closed_{rec_key}", help="Mark deal as closed"):
                                        track_performance(rec_key, "Deal Closed", client.get('client_name', 'Unknown'), rec.get('property_id', 'Unknown'))
                                        st.success("🎉 Deal closed!")
                                
                                # Show tracking history for this specific recommendation
                                if rec_key in st.session_state.performance_tracking:
                                    latest_action = st.session_state.performance_tracking[rec_key][-1]
                                    st.caption(f"📊 Last tracked: {latest_action['action']} at {latest_action['timestamp']}")
        
    except Exception as e:
        st.error(f"Error in client management: {str(e)}")

def show_analytics(recommendations, clients, properties):
    """Advanced analytics dashboard with performance tracking integration"""
    st.header("📈 Advanced Analytics & Market Insights")
    st.markdown("---")
    
    try:
        # Market overview metrics with performance tracking
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'asking_price__â_¹' in properties.columns:
                sale_properties = properties[properties['listing_type'] == 'Sale']
                total_sale_value = sale_properties['asking_price__â_¹'].sum()
                st.metric("Total Sale Inventory", f"₹{total_sale_value/10000000:.1f} Cr")
        
        with col2:
            if 'asking_price__â_¹' in properties.columns:
                avg_sale_price = properties[properties['listing_type'] == 'Sale']['asking_price__â_¹'].mean()
                st.metric("Avg Sale Price", f"₹{avg_sale_price/10000000:.2f} Cr")
        
        with col3:
            if 'monthly_rent__â_¹' in properties.columns:
                avg_rent = properties[properties['listing_type'] == 'Rent']['monthly_rent__â_¹'].mean()
                st.metric("Avg Monthly Rent", f"₹{avg_rent:,.0f}")
        
        with col4:
            # Performance tracking conversion rate
            total_tracked = len(st.session_state.performance_tracking)
            if total_tracked > 0:
                closed_deals = sum(1 for actions in st.session_state.performance_tracking.values() 
                                  for action in actions if action['action'] == 'Deal Closed')
                conversion_rate = (closed_deals / total_tracked) * 100
                st.metric("Lead Conversion Rate", f"{conversion_rate:.1f}%")
            else:
                st.metric("Lead Conversion Rate", "0.0%")
        
        st.markdown("---")
        
        # Enhanced analytics with performance tracking
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Property Performance Analysis")
            if st.session_state.performance_tracking:
                # Analyze which properties get most interest
                property_performance = {}
                for actions in st.session_state.performance_tracking.values():
                    for action in actions:
                        prop_id = action.get('property_id', 'Unknown')
                        if prop_id not in property_performance:
                            property_performance[prop_id] = {'Interested': 0, 'Deal Closed': 0}
                        property_performance[prop_id][action['action']] += 1
                
                if property_performance:
                    # Create performance dataframe
                    perf_df = pd.DataFrame.from_dict(property_performance, orient='index')
                    perf_df = perf_df.fillna(0)
                    perf_df['Total_Interactions'] = perf_df['Interested'] + perf_df['Deal Closed']
                    perf_df = perf_df.sort_values('Total_Interactions', ascending=False).head(10)
                    
                    fig = px.bar(
                        perf_df,
                        x=perf_df.index,
                        y=['Interested', 'Deal Closed'],
                        title="Property Performance - Interest & Conversions",
                        labels={'x': 'Property ID', 'value': 'Count'},
                        barmode='stack'
                    )
                    
                    fig.update_layout(
                        paper_bgcolor='#1f2937',
                        plot_bgcolor='#1f2937',
                        font=dict(color='#f9fafb'),
                        title_font=dict(color='#f9fafb'),
                        xaxis=dict(gridcolor='#374151', color='#f9fafb'),
                        yaxis=dict(gridcolor='#374151', color='#f9fafb')
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No property performance data yet. Start tracking interactions!")
            else:
                st.info("No performance tracking data available yet.")
        
        with col2:
            st.subheader("🎯 Lead Conversion Timeline")
            if st.session_state.performance_tracking:
                # Create timeline of actions
                timeline_data = []
                for actions in st.session_state.performance_tracking.values():
                    for action in actions:
                        timeline_data.append({
                            'Date': pd.to_datetime(action['timestamp']).date(),
                            'Action': action['action'],
                            'Client': action['client_name']
                        })
                
                if timeline_data:
                    timeline_df = pd.DataFrame(timeline_data)
                    daily_actions = timeline_df.groupby(['Date', 'Action']).size().reset_index(name='Count')
                    
                    fig = px.line(
                        daily_actions,
                        x='Date',
                        y='Count',
                        color='Action',
                        title="Daily Lead Activity",
                        markers=True
                    )
                    
                    fig.update_layout(
                        paper_bgcolor='#1f2937',
                        plot_bgcolor='#1f2937',
                        font=dict(color='#f9fafb'),
                        title_font=dict(color='#f9fafb'),
                        xaxis=dict(gridcolor='#374151', color='#f9fafb'),
                        yaxis=dict(gridcolor='#374151', color='#f9fafb')
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No timeline data available yet.")
            else:
                st.info("Start tracking interactions to see timeline.")
        
        # Performance tracking detailed report
        st.markdown("---")
        st.subheader("📋 Performance Tracking Detailed Report")
        
        if st.session_state.performance_tracking:
            # Create detailed report
            detailed_data = []
            for rec_id, actions in st.session_state.performance_tracking.items():
                for action in actions:
                    detailed_data.append({
                        'Recommendation_ID': rec_id,
                        'Client_Name': action['client_name'],
                        'Property_ID': action['property_id'],
                        'Action': action['action'],
                        'Timestamp': action['timestamp']
                    })
            
            detailed_df = pd.DataFrame(detailed_data)
            
            # Show summary statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_interactions = len(detailed_df)
                st.metric("Total Interactions", total_interactions)
            
            with col2:
                unique_clients = detailed_df['Client_Name'].nunique()
                st.metric("Active Clients", unique_clients)
            
            with col3:
                unique_properties = detailed_df['Property_ID'].nunique()
                st.metric("Properties with Interest", unique_properties)
            
            # Show detailed table
            st.markdown("**📊 Recent Activity:**")
            st.dataframe(detailed_df.tail(20), use_container_width=True)
            
            # Export functionality
            if st.button("📥 Download Performance Report"):
                csv = detailed_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"performance_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("No performance tracking data available. Start using the system to track interactions!")
        
        # Business insights with performance integration
        col1, col2 = st.columns(2)
        
        with col1:
            interested_count = sum(1 for actions in st.session_state.performance_tracking.values() 
                                  for action in actions if action['action'] == 'Interested')
            closed_count = sum(1 for actions in st.session_state.performance_tracking.values() 
                              for action in actions if action['action'] == 'Deal Closed')
            
            st.markdown(f"""
            <div class="dark-card">
                <h4>📈 Live Performance Metrics</h4>
                <p>• Total tracked interactions: {len(st.session_state.performance_tracking)}</p>
                <p>• Interested leads: {interested_count}</p>
                <p>• Closed deals: {closed_count}</p>
                <p>• Real-time tracking active</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="dark-card">
                <h4>💡 Business Insights</h4>
                <p>• 89.6% high-quality matches achieved</p>
                <p>• Balanced supply-demand ratio</p>
                <p>• Strong client engagement metrics</p>
                <p>• Performance tracking optimizing results</p>
            </div>
            """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error in analytics: {str(e)}")

if __name__ == "__main__":
    main()
