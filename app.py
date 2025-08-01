# app.py - Real Estate Recommendation System Web App (COMPLETE ENHANCED VERSION)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import warnings
import datetime
import json
import os
import uuid
import io # Added for CSV download
import base64 # Added for CSV download
from st_aggrid import AgGrid, GridOptionsBuilder # Added for interactive tables
from streamlit_plotly_events import plotly_events # Added for chart interactivity
warnings.filterwarnings('ignore')

# Configure Streamlit page settings
st.set_page_config(
    page_title="🏠 Real Estate Management System",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme CSS with light text fonts
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
    
    .stError {
        background-color: #7f1d1d !important;
        color: #fecaca !important;
        border: 1px solid #ef4444 !important;
    }
    
    /* Download buttons styling */
    .stDownloadButton button {
        background-color: #1a56db !important; /* A nice blue */
        color: #ffffff !important;
        border: 1px solid #1a56db !important;
        border-radius: 0.5rem;
        font-weight: 500;
        padding: 0.6rem 1.2rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        transition: background-color 0.3s ease, border-color 0.3s ease;
    }

    .stDownloadButton button:hover {
        background-color: #153e9b !important;
        border-color: #153e9b !important;
    }

    .stDownloadButton button:active {
        background-color: #0f2c6b !important;
        border-color: #0f2c6b !important;
    }
</style>
""", unsafe_allow_html=True)

# Data persistence functions
st.subheader("💾 Data Persistence Functions")
st.markdown("---")
def save_performance_data():
    """Save performance tracking data to JSON file"""
    try:
        # Convert datetime objects to strings for JSON serialization
        serializable_data = {}
        for key, actions in st.session_state.performance_tracking.items():
            serializable_data[key] = []
            for action in actions:
                serializable_action = action.copy()
                if isinstance(action.get('timestamp'), datetime.datetime):
                    serializable_action['timestamp'] = action['timestamp'].isoformat()
                serializable_data[key].append(serializable_action)
        
        with open('performance_data.json', 'w') as f:
            json.dump(serializable_data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving performance data: {e}")
        return False

def load_performance_data():
    """Load performance tracking data from JSON file"""
    try:
        if os.path.exists('performance_data.json'):
            with open('performance_data.json', 'r') as f:
                data = json.load(f)
            
            # Convert timestamp strings back to datetime objects
            for key, actions in data.items():
                for action in actions:
                    if 'timestamp' in action and isinstance(action['timestamp'], str):
                        try:
                            action['timestamp'] = datetime.datetime.fromisoformat(action['timestamp'])
                        except:
                            action['timestamp'] = action['timestamp']  # Keep as string if parsing fails
            
            return data
        return {}
    except Exception as e:
        show_toast(f"Error loading performance data: {e}", type="error")
        return {}

# Helper functions for formatting
def format_indian_currency(amount):
    """Format currency in Indian style with Crores and Lakhs"""
    if pd.isna(amount) or amount == 0:
        return "Not specified"
    
    if amount >= 10000000:  # 1 Crore or more
        return f"₹{amount/10000000:.2f} Cr"
    elif amount >= 100000:  # 1 Lakh or more
        return f"₹{amount/100000:.1f} L"
    else:
        return f"₹{amount:,}"

def format_area(area):
    """Format area with commas"""
    if pd.isna(area):
        return "N/A"
    return f"{area:,} sq ft"

# Data Management Functions for Excel Integration
def load_excel_data():
    """Load data directly from Excel files for editing"""
    try:
        excel_path = Path("real_estate_project/data/raw")
        
        # Try to load original Excel files
        clients_excel = excel_path / "Real_Estate_Clients.xlsx"
        properties_excel = excel_path / "Real_Estate_Properties.xlsx"
        
        if clients_excel.exists() and properties_excel.exists():
            clients_df = pd.read_excel(clients_excel)
            properties_df = pd.read_excel(properties_excel)
            return clients_df, properties_df, excel_path
        else:
            # Fallback to processed CSV files
            processed_path = Path("real_estate_project/data/processed")
            clients_df = pd.read_csv(processed_path / "clients_with_features.csv")
            properties_df = pd.read_csv(processed_path / "properties_with_features.csv")
            return clients_df, properties_df, processed_path
            
    except Exception as e:
        st.error(f"Error loading Excel data: {e}")
        return None, None, None

def save_to_excel(clients_df, properties_df, file_path):
    """Save updated data back to Excel files"""
    try:
        # Save clients
        clients_file = file_path / "Real_Estate_Clients.xlsx"
        clients_df.to_excel(clients_file, index=False)
        
        # Save properties  
        properties_file = file_path / "Real_Estate_Properties.xlsx"
        properties_df.to_excel(properties_file, index=False)
        
        # Also update processed CSV files for the app to use
        processed_path = Path("real_estate_project/data/processed")
        clients_df.to_csv(processed_path / "clients_with_features.csv", index=False)
        properties_df.to_csv(processed_path / "properties_with_features.csv", index=False)
        
        return True
    except Exception as e:
        st.error(f"Error saving to Excel: {e}")
        return False

def download_csv(df, name):
    """Generates a download link for a dataframe as CSV."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="{name}.csv">Download {name}.csv</a>'
    st.markdown(href, unsafe_allow_html=True)

def download_excel(dataframe, name="data"):
    output = io.BytesIO()
    dataframe.to_excel(output, index=False)
    st.download_button(
        label="⬇️ Download as Excel",
        data=output.getvalue(),
        file_name=f"{name}.xlsx",
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        use_container_width=True
    )

def show_aggrid(df, fit_columns=True, search=True, selection='multiple'):
    """Display an interactive table with sorting, column fit, and search."""
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()  # Allows toggling columns and search
    gb.configure_selection(selection_mode=selection, use_checkbox=True)
    if fit_columns:
        gb.configure_grid_options(domLayout='autoHeight')
    grid_options = gb.build()
    grid_return = AgGrid(
        df,
        gridOptions=grid_options,
        theme="streamlit",
        allow_unsafe_jscode=True if search else False,
        height=400,
        enable_enterprise_modules=True
    )
    return grid_return

def generate_property_id(property_type, listing_type):
    """Generate unique property ID"""
    prefix = "SALE" if listing_type == "Sale" else "RENT"
    type_code = property_type[:4].upper() if property_type else "PROP"
    unique_num = str(uuid.uuid4())[:6].upper()
    return f"{prefix}-{type_code}-{unique_num}"

def generate_client_id():
    """Generate unique client ID"""
    return f"CLI-{str(uuid.uuid4())[:8].upper()}"

# Initialize session state for performance tracking
if 'performance_tracking' not in st.session_state:
    st.session_state.performance_tracking = load_performance_data()

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
    
    # Path to column rename maps
    rename_map_path = Path(r"D:\Git repo\real_estate_listings\real_estate_project\meta\column_rename_maps.json")
    column_rename_maps = {}
    if rename_map_path.exists():
        with open(rename_map_path, 'r') as f:
            column_rename_maps = json.load(f)

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
            recommendations_df = pd.read_csv(recommendations_file)
            clients_df = pd.read_csv(clients_file)
            properties_df = pd.read_csv(properties_file)

            # Debugging: Print columns before renaming
            print(f"Properties columns before renaming: {properties_df.columns.tolist()}")

            # Apply column renaming for properties DataFrame
            if 'active' in column_rename_maps and not properties_df.empty:
                rename_dict = {}
                for old_name, new_name in column_rename_maps['active'].items():
                    # Check for exact match
                    if old_name in properties_df.columns:
                        rename_dict[old_name] = new_name
                    # Handle potential encoding variations for specific columns
                    elif old_name == "Asking Price (\u00e2\u201a\u00b9)" and "Asking Price (₹)" in properties_df.columns:
                        rename_dict["Asking Price (₹)"] = new_name
                    elif old_name == "Monthly Rent (\u00e2\u201a\u00b9)" and "Monthly Rent (₹)" in properties_df.columns:
                        rename_dict["Monthly Rent (₹)"] = new_name
                    # Fallback for other potential encoding variations if needed
                    elif old_name.replace('(\u00e2\u201a\u00b9)', '(₹)') in properties_df.columns: 
                        rename_dict[old_name.replace('(\u00e2\u201a\u00b9)', '(₹)')] = new_name
            
                print(f"Rename dictionary: {rename_dict}") # Debugging: Print rename_dict
                properties_df.rename(columns=rename_dict, inplace=True)

            # Debugging: Print columns after renaming
            print(f"Properties columns after renaming: {properties_df.columns.tolist()}")

            # Verify critical columns are present after renaming
            if 'asking_price' not in properties_df.columns:
                print("WARNING: 'asking_price' column not found after renaming.")
            if 'monthly_rent' not in properties_df.columns:
                print("WARNING: 'monthly_rent' column not found after renaming.")

            return recommendations_df, clients_df, properties_df
            
        except Exception as e:
            st.error(f"Error loading data from {data_path}: {e}")
            continue
    
    return None, None, None


# Feature Engineering for Recommendations
def compute_property_score(client, property_):
    """Simple rule-based (or ML) recommender logic—expandable."""
    # Score based on how close price, BHK, location matches client prefs
    score = 0

    # BHK match
    if 'client_bhk' in client and 'bedrooms__bhk' in property_:
        if client['client_bhk'] == property_['bedrooms__bhk']:
            score += 30

    # Budget match (within 20% for sale, 15% for rent)
    prop_price = property_.get('asking_price') if property_['listing_type'] == 'Sale' else property_.get('monthly_rent')
    if prop_price:
        if abs(prop_price - client['client_budget']) / max(client['client_budget'], 1) < 0.2:
            score += 40

    # Location match (case-insensitive substring)
    if 'client_location' in client and 'area___locality' in property_:
        if isinstance(client['client_location'], str) and isinstance(property_['area___locality'], str):
            if client['client_location'].lower() in property_['area___locality'].lower():
                score += 30

    # Expand: Add model/advanced criteria later! (amenities, area, etc)
    return score


def quick_match_properties(properties_df, budget_min, budget_max, bhk_preference, listing_type):
    """Quick matching algorithm for sidebar feature"""
    try:
        # Filter properties based on criteria
        filtered = properties_df.copy()
        
        # Filter by listing type
        filtered = filtered[filtered['listing_type'] == listing_type]
        
        # Filter by BHK
        if bhk_preference != "Any":
            filtered = filtered[filtered['bedrooms__bhk'] == bhk_preference]
        
        # Filter by budget
        if listing_type == 'Sale':
            filtered = filtered[
                (filtered['asking_price'] >= budget_min) & 
                (filtered['asking_price'] <= budget_max)
            ]
        elif listing_type == 'Rent':
            filtered = filtered[
                (filtered['monthly_rent'] >= budget_min) & 
                (filtered['monthly_rent'] <= budget_max)
            ]
        
        return filtered.head(5)  # Return top 5 matches
        
    except Exception as e:
        st.error(f"Error in quick match: {str(e)}")
        return pd.DataFrame()

def track_performance(recommendation_id, action, client_name, property_id):
    """Track recommendation performance with persistence"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if recommendation_id not in st.session_state.performance_tracking:
        st.session_state.performance_tracking[recommendation_id] = []
    
    st.session_state.performance_tracking[recommendation_id].append({
        'action': action,
        'timestamp': timestamp,
        'client_name': client_name,
        'property_id': property_id
    })
    
    # Save to file immediately
    save_performance_data()

def remove_performance_tracking(recommendation_id, action_to_remove):
    """Remove specific tracking action and handle cascading removals"""
    if recommendation_id in st.session_state.performance_tracking:
        # Get current actions
        actions = st.session_state.performance_tracking[recommendation_id]
        
        # Remove the specific action (keep only actions that don't match)
        updated_actions = [action for action in actions if action['action'] != action_to_remove]
        
        # If removing "Interested", also remove "Deal Closed" (business logic)
        if action_to_remove == "Interested":
            updated_actions = [action for action in updated_actions if action['action'] != "Deal Closed"]
        
        # Update the session state
        if updated_actions:
            st.session_state.performance_tracking[recommendation_id] = updated_actions
        else:
            # Remove the entire tracking record if no actions left
            del st.session_state.performance_tracking[recommendation_id]
        
        # Save to file immediately
        save_performance_data()
        return True
    return False

def get_tracking_status(recommendation_id):
    """Get current tracking status for a recommendation"""
    if recommendation_id not in st.session_state.performance_tracking:
        return {"interested": False, "closed": False, "actions": []}
    
    actions = st.session_state.performance_tracking[recommendation_id]
    action_types = [action['action'] for action in actions]
    
    return {
        "interested": 'Interested' in action_types,
        "closed": 'Deal Closed' in action_types,
        "actions": actions
    }

def show_latest_cards(data, label_fields, value_fields, date_field, extra_fields=None, card_color='#232f49'):
    """
    Display most recent entries from a DataFrame in a unified card layout.
    - data: DataFrame to display.
    - label_fields: fields (list/tuple) used for main label.
    - value_fields: fields (list/tuple) for summary/stat line.
    - date_field: field for the date.
    - extra_fields: (optional) list/tuple of (name, field, color) to display.
    - card_color: background color for the card.
    """
    for _, row in data.iterrows():
        label_line = " ".join(str(row.get(f, '')) for f in label_fields)
        value_line = " · ".join(str(row.get(f, '')) for f in value_fields)
        date = row.get(date_field, '')
        extras = ""
        if extra_fields:
            for name, field, color in extra_fields:
                val = row.get(field, '-')
                extras += f"<span style='color:{color};margin-left:0.8em'>{name}: {val}</span>"
        st.markdown(f"""
        <div style='background:{card_color};border-radius:12px;padding:0.7em 1em;margin-bottom:7px;
                    border:1px solid #334155;line-height:1.3'>
            <b style='color:#f472b6'>{label_line}</b> <span style='color:#818cf8;font-size:0.95em'>({date})</span><br>
            <span style='color:#94a3b8;'>{value_line}</span>
            {extras}
        </div>
        """, unsafe_allow_html=True)


def show_toast(message, type="success", duration=3, sidebar=False):
    """
    Shows a floating toast notification that auto-hides.
    type: "success", "error", "info", or "warning"
    duration: seconds before fade-out
    """
    # Simple color mapping
    colors = {
        "success": "#16a34a",
        "info": "#2563eb",
        "error": "#b91c1c",
        "warning": "#f59e42"
    }
    color = colors.get(type, "#16a34a")
    position_css = "left: 2rem;" if sidebar else "right: 2rem;"
    st.markdown(f"""
    <style>
    .toast {{
        position: fixed;
        top: 2rem; {position_css}
        min-width: 260px; z-index: 99999;
        background: {color}; color: #fff;
        border-radius: 8px; box-shadow: 0 6px 32px #0007;
        padding: 1.13rem 2.4rem 1.13rem 1.3rem;
        font-size: 1.09rem; font-weight: 500;
        animation: fadein 0.5s, fadeout 0.6s {duration}s forwards;
        pointer-events: none; opacity: 0.95;
    }}
    @keyframes fadein {{ from {{opacity: 0; top:0.5rem;}} to {{opacity: 0.95; top:2rem;}}}}
    @keyframes fadeout {{ from {{opacity: 0.95;}} to {{opacity: 0; top:-2rem;}}}}
    </style>
    <div class="toast">{message}</div>
    """, unsafe_allow_html=True)


def pretty_card(title, left, right, chips, status, color="#1e2a38"):
    chip_html = " ".join(f"<span style='background:#334155; color:#fff; border-radius:14px; padding:2px 10px;font-size:0.97em;margin-right:5px'>{chip}</span>" for chip in chips)
    st.markdown(f"""
    <div style="background:{color};border-radius:15px;padding:1.05em 1.6em;margin-bottom:15px;box-shadow:0 3px 15px #151c275a;">
        <div style="display:flex; align-items:center; justify-content:space-between;">
            <span style="font-size:1.19em; color:#51cdff;"><b>{title}</b></span>
            <span style="background:#05966922; color:#22d3ee; border-radius:9px; padding:4px 15px;">
                <b>{status}</b>
            </span>
        </div>
        <div style="margin-top:0.6em; margin-bottom:0.5em;"><b>{left}</b> <span style="float:right;">{right}</span></div>
        <div>{chip_html}</div>
    </div>
    """, unsafe_allow_html=True)


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

    # Data loading with spinner
    with st.spinner('Loading data...'):
        recommendations_df, clients_df, properties_df = load_data()

    # Check if data loaded successfully
    if recommendations_df is None or clients_df is None or properties_df is None:
        st.error("Failed to load data. Please ensure all necessary CSV files are in 'real_estate_project/data/processed'.")
        return # Stop execution if data loading failed

    # Sidebar navigation
    st.sidebar.header("Navigation")
    selected_page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Property Search", "Client Management", "Analytics", "Data Management"]
    )

    # Quick Stats
    st.markdown("""
    <div style="margin-top: 20px; padding: 15px; background-color: #1e2a38; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);">
        <h2 style="color: #51cdff; text-align: center; margin-bottom: 15px;">Quick Stats</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        pretty_card("Total Properties", f"{properties_df['property_id'].nunique()}", "", [], "Active", "#1e2a38")
    with col2:
        pretty_card("Total Clients", f"{clients_df['clientid'].nunique()}", "", [], "Engaged", "#1e2a38")
    with col3:
        pretty_card("Avg. Price", f"${properties_df['asking_price'].mean():,.0f}", "", [], "Market", "#1e2a38")

    # Display content based on selected page
    if selected_page == "Dashboard":
        dashboard_page(recommendations_df, clients_df, properties_df)
    elif selected_page == "Property Search":
        property_search_page(properties_df)
    elif selected_page == "Client Management":
        client_management_page(clients_df)
    elif selected_page == "Analytics":
        analytics_page(recommendations_df, clients_df, properties_df)
    elif selected_page == "Data Management":
        data_management_page(clients_df, properties_df)

    tour_steps = [
        {"title": "Welcome!", "content": "This tour will guide you through the main features of our Real Estate Management System."},
        {"title": "Navigation", "content": "Use the sidebar to switch between different sections: Dashboard, Property Search, Client Management, and Analytics."},
        {"title": "Quick Match", "content": "Find properties that match client preferences instantly with our Quick Match feature."},
        {"title": "Analytics", "content": "Track performance metrics and visualize data with interactive charts."},
        {"title": "Data Management", "content": "Add and manage clients and properties, and download raw data."},
        {"title": "Thank You!", "content": "You've completed the tour. Enjoy exploring the Real Estate Management System!"}
    ]

    if st.sidebar.button("🌟 Take an Interactive Tour"):
        st.session_state["show_tour"] = True
        st.session_state["tour_step"] = 0

    # Handle tour navigation based on button clicks
    if st.session_state["show_tour"]:
        current_step = tour_steps[st.session_state["tour_step"]]

        tour_html = f"""
        <div style='position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 10000; display: flex; justify-content: center; align-items: center;'>
            <div style='background:#1e293b; border-radius:12px; padding:1.5em; margin:1em; max-width: 600px; width: 90%;
                        border-left:5px solid #6366f1; box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1); position: relative;'>
                <button onclick="window.parent.postMessage({{type: 'tour', action: 'close'}}, '*')" 
                        style='position: absolute; top: 10px; right: 10px; background: none; border: none; color: #e2e8f0; font-size: 1.5em; cursor: pointer;'>
                    &times;
                </button>
                <h3 style='color:#f8fafc; margin-top:0'>{current_step['title']}</h3>
                <p style='color:#e2e8f0'>{current_step['content']}</p>
                <div style='display:flex; justify-content:space-between; margin-top:1em'>
        """

        # Previous button
        if st.session_state["tour_step"] > 0:
            tour_html += """
                    <button id='prev_tour_btn' style='background:#334155; color:#fff; border:none; padding:0.5em 1em; border-radius:6px; cursor:pointer'>
                        ← Previous
                    </button>
            """
        else:
            tour_html += "<div></div>"

        # Next/Finish button
        if st.session_state["tour_step"] < len(tour_steps) - 1:
            tour_html += """
                    <button id='next_tour_btn' style='background:#6366f1; color:#fff; border:none; padding:0.5em 1em; border-radius:6px; cursor:pointer'>
                        Next →
                    </button>
            """
        else:
            tour_html += """
                    <button id='finish_tour_btn' style='background:#10b981; color:#fff; border:none; padding:0.5em 1em; border-radius:6px; cursor:pointer'>
                        Finish Tour
                    </button>
            """

        tour_html += "</div></div></div>"

        st.markdown(tour_html, unsafe_allow_html=True)

        # Use Streamlit buttons to control state, triggered by JS clicks
        # This is a workaround since direct JS-to-Streamlit state updates are complex without custom components
        if st.session_state["show_tour"]:
            if st.session_state["tour_step"] < len(tour_steps) - 1:
                if st.button("Next Step", key="tour_next_hidden", help="Hidden button for tour navigation", disabled=True):
                    st.session_state["tour_step"] += 1
                    st.experimental_rerun()
            if st.session_state["tour_step"] > 0:
                if st.button("Previous Step", key="tour_prev_hidden", help="Hidden button for tour navigation", disabled=True):
                    st.session_state["tour_step"] -= 1
                    st.experimental_rerun()
            if st.button("Close Tour", key="tour_close_hidden", help="Hidden button for tour navigation", disabled=True):
                st.session_state["show_tour"] = False
                st.session_state["tour_step"] = 0
                st.experimental_rerun()

        # JavaScript to handle button clicks and communicate back to Streamlit
        st.markdown("""
        <script>
        const nextBtn = document.getElementById('next_tour_btn');
        if (nextBtn) {
            nextBtn.onclick = () => {
                const hiddenNextBtn = window.parent.document.querySelector('[data-testid="stButton-tour_next_hidden"]');
                if (hiddenNextBtn) hiddenNextBtn.click();
            };
        }

        const prevBtn = document.getElementById('prev_tour_btn');
        if (prevBtn) {
            prevBtn.onclick = () => {
                const hiddenPrevBtn = window.parent.document.querySelector('[data-testid="stButton-tour_prev_hidden"]');
                if (hiddenPrevBtn) hiddenPrevBtn.click();
            };
        }

        const finishBtn = document.getElementById('finish_tour_btn');
        if (finishBtn) {
            finishBtn.onclick = () => {
                const hiddenCloseBtn = window.parent.document.querySelector('[data-testid="stButton-tour_close_hidden"]');
                if (hiddenCloseBtn) hiddenCloseBtn.click();
            };
        }

        // For the 'x' close button
        window.addEventListener('message', (event) => {
            if (event.data.type === 'tour' && event.data.action === 'close') {
                const hiddenCloseBtn = window.parent.document.querySelector('[data-testid="stButton-tour_close_hidden"]');
                if (hiddenCloseBtn) hiddenCloseBtn.click();
            }
        });
        </script>
        """, unsafe_allow_html=True)
    
    # Load data with progress indication
    with st.spinner("🔄 Loading data..."):
        recommendations, clients, properties = load_data()
    
    if recommendations_df is None:
        st.error("❌ Could not load data. Please ensure all processed data files exist!")
        st.info("💡 Make sure you've completed the data processing pipeline first!")
        st.stop()
    
    # Clear success message
    st.success("🎉 Application loaded successfully!")

    
    # Add a collapsible sidebar with icons only in "mini" mode
    # --------- Collapsible Sidebar Implementation ----------
    if 'sidebar_collapsed' not in st.session_state:
        st.session_state['sidebar_collapsed'] = False

    col1, col2 = st.sidebar.columns([1, 8])
    toggle_label = "☰" if st.session_state['sidebar_collapsed'] else "🡸"
    if col1.button(toggle_label, help="Expand/collapse sidebar", key="nav_collapse"):
        st.session_state['sidebar_collapsed'] = not st.session_state['sidebar_collapsed']

    nav_items = [
        {"icon": "🏠", "label": "Dashboard"},
        {"icon": "🔍", "label": "Property Search"},
        {"icon": "👥", "label": "Client Management"},
        {"icon": "📈", "label": "Analytics"},
        {"icon": "⚙️", "label": "Data Management"},
    ]

    if st.session_state['sidebar_collapsed']:
        nav_choices = [x['icon'] for x in nav_items]
        page = st.sidebar.radio("", nav_choices, key="nav_radio", format_func=lambda x: x)
    else:
        nav_choices = [f"{x['icon']} {x['label']}" for x in nav_items]
        page = st.sidebar.radio("Navigation", nav_choices, key="nav_radio", format_func=str)

    # Normalize page value (get label)
    selected_label = None
    for x in nav_items:
        if page.endswith(x['label']) or page == x['icon']:
            selected_label = x['label']
    if selected_label is None:
        selected_label = "Dashboard"  # Fallback

    # Assign selected_label to page for compatibility with existing code
    st.session_state['page'] = selected_label # Use session state to persist page selection

    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    st.sidebar.metric("Total Clients", f"{len(clients_df) if clients_df is not None else 0:,}")
    st.sidebar.metric("Active Properties", f"{len(properties_df) if properties_df is not None else 0:,}")
    st.sidebar.metric("Recommendations", f"{len(recommendations_df):,}")
    
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
        
        quick_matches = quick_match_properties(properties_df, budget_min, budget_max, bhk_preference, listing_type)
        
        if len(quick_matches) > 0:
            for idx, prop in quick_matches.iterrows():
                price_col = 'asking_price__â_¹' if listing_type == 'Sale' else 'monthly_rent__â_¹'
                price_val = prop.get(price_col, 0)
                
                if isinstance(price_val, (int, float)) and not pd.isna(price_val):
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
    
    # Data management buttons
    if st.sidebar.button("💾 Save Data", help="Save current performance data"):
        if save_performance_data():
            show_toast("✅ Data saved!", type="success", sidebar=True)
        else:
            show_toast("❌ Save failed!", type="error", sidebar=True)

    if st.sidebar.button("🔄 Reset Data", help="Clear all performance tracking"):
        st.session_state.performance_tracking = {}
        if os.path.exists('performance_data.json'):
            os.remove('performance_data.json')
        show_toast("✅ Data reset!", type="success", sidebar=True)
        st.rerun()
    
    # Diagnostic block

    # Feedback Form
    with st.sidebar.expander("💬 Feedback?"):
        feedback = st.text_area("What do you love? What should we improve?")
        if st.button("Send Feedback"):
            # For now, just simulate feedback sending
            show_toast("Thank you for your feedback!", "success", sidebar=True)
            # For real apps: save to a file, Google Sheet, or send email

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style='text-align:center'>
            <span style='font-size:1.3em;font-weight:bold;'>👋 About the Developer</span><br>
            <span>Made with ❤️ by <b>Your Name</b></span><br>
            <a href='https://linkedin.com/in/your-linkedin' target='_blank'> <img src='https://cdn.simpleicons.org/linkedin/38bdf8/18181b' style='margin:0 5px;height:1.4em'></a>
            <a href='https://github.com/your-github' target='_blank'> <img src='https://cdn.simpleicons.org/github/38bdf8/18181b' style='margin:0 5px;height:1.4em'></a>
        </div>
        """, unsafe_allow_html=True
    )




    
    # Display selected page with error handling
    try:
        if st.session_state['page'] == "Dashboard":
            show_dashboard(recommendations_df, clients_df, properties_df)
        elif st.session_state['page'] == "Property Search":
            show_property_search(properties_df)
        elif st.session_state['page'] == "Client Management":
            show_client_management(clients_df, properties_df, recommendations_df)
        elif st.session_state['page'] == "Analytics":
            show_analytics(recommendations_df, clients_df, properties_df)
        elif st.session_state['page'] == "Data Management":
            show_data_management(clients_df, properties_df)
        else:
            st.info("Select a page from the sidebar.")
    except Exception as e:
        st.error(f"❌ Error displaying page: {str(e)}")

def show_dashboard(recommendations_df, clients_df, properties_df):
    """Display the main dashboard with key metrics"""

    # st.write("DEBUG - show_dashboard function called.")
    st.title("Dashboard")

    with st.expander("ℹ️ How to use this app", expanded=False):
        st.markdown("""
        **Welcome!**  
        Use the sidebar to navigate between Dashboard, Property Search, Client Management, Analytics, and Data Management.  
        - Add or search for clients/properties under management tabs. 
        - All notifications for add/remove actions pop up automatically. 
        - Download CSV/Excel with one click! 
        """)

    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="👥 Total Clients",
            value=f"{len(clients_df):,}",
            delta="N/A"
        )
    with col2:
        st.metric(
            label="🏠 Total Properties",
            value=f"{len(properties_df):,}",
            delta="N/A"
        )
    with col3:
        st.metric(
            label="💡 Total Recommendations",
            value=f"{len(recommendations_df):,}",
            delta="N/A"
        )
    with col4:
        # Calculate total interested leads and closed deals from performance_tracking
        interested_leads = sum(1 for actions in st.session_state.performance_tracking.values()
                              for action in actions if action['action'] == 'Interested')
        closed_deals = sum(1 for actions in st.session_state.performance_tracking.values()
                          for action in actions if action['action'] == 'Deal Closed')
        st.metric(
            label="🤝 Deals Closed",
            value=f"{closed_deals}",
            delta=f"{interested_leads} Leads"
        )

    st.markdown("--- ")

    # Latest Added Clients
    st.subheader("🆕 Latest Added Clients")
    latest_count = st.slider("How many?", 1, min(8, len(clients_df)), 3, key="latest_clients_count")
    if 'registration_date' in clients_df.columns:
        latest_clients = clients_df.sort_values('registration_date', ascending=False).head(latest_count)
    else:
        latest_clients = clients_df.tail(latest_count)
    show_latest_cards(
        latest_clients,
        label_fields=("client_name",),
        value_fields=("client_phone", "looking_for"),
        date_field="registration_date",
        extra_fields=[("Status", "status", "#fbbf24")]
    )

    st.markdown("--- ")

    # Latest Added Properties
    st.subheader("🏠 Latest Added Properties")
    latest_count = st.slider("How many?", 1, min(8, len(properties_df)), 3, key="latest_props_count")
    if 'listing_date' in properties_df.columns:
        latest_props = properties_df.sort_values('listing_date', ascending=False).head(latest_count)
    else:
        latest_props = properties_df.tail(latest_count)
    show_latest_cards(
        latest_props,
        label_fields=("property_id",),
        value_fields=("area___locality", "asking_price__â_¹"),
        date_field="listing_date",
        extra_fields=[("Status", "listing_status", "#a3e635")]
    )
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top Performing Properties")
        try:
            if 'property_id' in recommendations_df.columns:
                top_properties = recommendations_df['property_id'].value_counts().head(10)
                
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
        st.subheader("📊 Match Quality Distribution")
        try:
            if 'similarity_score' in recommendations_df.columns and len(recommendations_df) > 0:
                # Create quality bins with better error handling
                quality_bins = []
                valid_scores = recommendations_df['similarity_score'].dropna()
                
                if len(valid_scores) > 0:
                    for score in valid_scores:
                        if score >= 90:
                            quality_bins.append('Excellent (90-100%)')
                        elif score >= 80:
                            quality_bins.append('Very Good (80-89%)')
                        elif score >= 70:
                            quality_bins.append('Good (70-79%)')
                        else:
                            quality_bins.append('Fair (60-69%)')
                    
                    if quality_bins:
                        quality_counts = pd.Series(quality_bins).value_counts()
                        
                        # Dark theme pie chart
                        fig = px.pie(
                            values=quality_counts.values,
                            names=quality_counts.index,
                            title="Distribution of Match Quality",
                            color_discrete_sequence=['#10b981', '#3b82f6', '#f59e0b', '#ef4444']
                        )
                        
                        fig.update_layout(
                            height=400,
                            paper_bgcolor='#1f2937',
                            font=dict(color='#f9fafb'),
                            title_font=dict(color='#f9fafb', size=16),
                            showlegend=True,
                            legend=dict(
                                font=dict(color='#f9fafb'),
                                bgcolor='rgba(0,0,0,0)'
                            )
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No valid similarity scores to display")
                else:
                    st.warning("No similarity score data available")
            else:
                st.warning("Similarity scores not found in recommendations data")
        except Exception as e:
            st.error(f"Error creating quality distribution chart: {str(e)}")
    
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
            if 'listing_type' in recommendations_df.columns:
                rental_count = len(recommendations_df[recommendations_df['listing_type'] == 'Rent'])
                rental_pct = (rental_count / len(recommendations_df)) * 100 if len(recommendations_df) > 0 else 0
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

def show_property_search(properties_df):
    """Property search and matching interface with performance tracking"""
    st.title("Property Search and Matching")
    st.sidebar.header("Filter Properties")
    st.markdown("---")
    
    # Search filters with dark theme
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
    
    # Apply filters and show results - ENHANCED VERSION
    try:
        filtered_properties = properties_df.copy()
        
        # Apply listing type filter
        if search_type != "All":
            filtered_properties = filtered_properties[filtered_properties['listing_type'] == search_type]
            st.info(f"Filtered by type: {len(filtered_properties)} {search_type} properties")
        
        # Apply BHK filter
        if bhk_filter != "All":
            bhk_num = int(bhk_filter.split()[0])
            filtered_properties = filtered_properties[filtered_properties['bedrooms__bhk'] == bhk_num]
            st.info(f"Filtered by BHK: {len(filtered_properties)} properties with {bhk_num} BHK")
        
        # Apply location filter - FIXED
        if location_filter != "All":
            # Normalize location for matching
            location_matches = filtered_properties['area___locality'].str.contains(location_filter, case=False, na=False)
            filtered_properties = filtered_properties[location_matches]
            st.info(f"Filtered by location: {len(filtered_properties)} properties in {location_filter}")
        
        # Apply price range filter - FIXED
        if search_type == "Sale" or search_type == "All":
            price_min = price_range[0] * 10000000  # Convert crores to rupees
            price_max = price_range[1] * 10000000
            
            if 'asking_price__â_¹' in filtered_properties.columns:
                price_condition = (
                    (filtered_properties['asking_price__â_¹'] >= price_min) &
                    (filtered_properties['asking_price__â_¹'] <= price_max) &
                    (filtered_properties['asking_price__â_¹'].notna())
                )
                filtered_properties = filtered_properties[price_condition]
                st.info(f"Filtered by price: {len(filtered_properties)} properties between ₹{price_range[0]:.1f}Cr - ₹{price_range[1]:.1f}Cr")
        
        elif search_type == "Rent":
            rent_min = rent_range[0] * 1000  # Convert thousands to rupees
            rent_max = rent_range[1] * 1000
            
            if 'monthly_rent__â_¹' in filtered_properties.columns:
                rent_condition = (
                    (filtered_properties['monthly_rent__â_¹'] >= rent_min) &
                    (filtered_properties['monthly_rent__â_¹'] <= rent_max) &
                    (filtered_properties['monthly_rent__â_¹'].notna())
                )
                filtered_properties = filtered_properties[rent_condition]
                st.info(f"Filtered by rent: {len(filtered_properties)} properties between ₹{rent_range[0]}k - ₹{rent_range[1]}k")
        
        st.subheader(f"🏠 Search Results ({len(filtered_properties)} properties found)")
        
        if len(filtered_properties) > 0:
            # Display properties in expandable cards with performance tracking
            display_properties = filtered_properties.head(15)
            
            for idx, prop in display_properties.iterrows():
                # Create property title
                property_id = prop.get("property_id", "--")
                bhk_info = f"{prop.get('bedrooms__bhk', '?')} BHK" if pd.notna(prop.get('bedrooms__bhk')) else "? BHK"
                location_info = prop.get('area___locality', '--')
                
                # Determine price string based on listing type
                price_str = ""
                if prop.get('listing_type') == "Sale":
                    price_str = f"₹{prop.get('asking_price__â_¹', 0):,.0f}"
                elif prop.get('listing_type') == "Rent":
                    price_str = f"₹{prop.get('monthly_rent__â_¹', 0):,.0f}/mo"

                # Create chips for the card
                chips = [
                    prop.get('furnishing', '?'),
                    prop.get('facing_direction', '?'),
                    f"Floor: {prop.get('floor_number','?')}/{prop.get('total_floors','?')}"
                ]
                
                # Get status
                status = prop.get("listing_status","Available")

                pretty_card(
                    title=property_id,
                    left=f"{location_info} | {bhk_info}",
                    right=price_str,
                    chips=chips,
                    status=status
                )

                # The expander content remains the same, but it should be inside the pretty_card logic if possible
                # For now, keeping it separate as pretty_card is markdown based.
                with st.expander(f"Details for {property_id}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**📋 Basic Details**")
                        st.write(f"**Type:** {prop.get('property_type', 'N/A')}")
                        st.write(f"**Area:** {format_area(prop.get('area__sq__ft', 0))}")
                        st.write(f"**Furnishing:** {prop.get('furnishing', 'N/A')}")
                        st.write(f"**Age:** {prop.get('property_age__yrs', 'N/A')} years")
                    
                    with col2:
                        st.markdown("**💰 Pricing**")
                        if prop.get('listing_type') == 'Sale' and pd.notna(prop.get('asking_price__â_¹')):
                            price = prop['asking_price__â_¹']
                            st.write(f"**Asking Price:** {format_indian_currency(price)}")
                            if pd.notna(prop.get('price_per_sqft')):
                                st.write(f"**Price/sq ft:** ₹{prop['price_per_sqft']:,.0f}")
                        elif prop.get('listing_type') == 'Rent' and pd.notna(prop.get('monthly_rent__â_¹')):
                            rent = prop['monthly_rent__â_¹']
                            st.write(f"**Monthly Rent:** {format_indian_currency(rent)}")
                            if pd.notna(prop.get('rent_per_sqft')):
                                st.write(f"**Rent/sq ft:** ₹{prop['rent_per_sqft']:.0f}")
                        
                        if pd.notna(prop.get('maint___month__â_¹')) and prop['maint___month__â_¹'] > 0:
                            st.write(f"**Maintenance:** ₹{prop['maint___month__â_¹']:,}/month")
                    
                    with col3:
                        st.markdown("**🏢 Building Details**")
                        st.write(f"**Floor:** {prop.get('floor_number', 'N/A')}/{prop.get('total_floors', 'N/A')}")
                        st.write(f"**Parking:** {prop.get('parking__cars', 'N/A')} cars")
                        st.write(f"**Facing:** {prop.get('facing_direction', 'N/A')}")
                        st.write(f"**Building:** {prop.get('building___society', 'N/A')}")
                    
                    # 🎯 ENHANCED PERFORMANCE TRACKING with UNDO Feature
                    st.markdown("---")
                    st.markdown("**📈 Track Interest:**")

                    property_id = prop.get('property_id', f'prop_{idx}')
                    tracking_key = f"search_{property_id}_{idx}"

                    # Get current tracking status
                    status = get_tracking_status(tracking_key)

                    # Create button layout
                    button_col1, button_col2, button_col3 = st.columns([1, 1, 2])

                    with button_col1:
                        if status["interested"]:
                            # Show "Remove Interest" button instead of "Interested"
                            if st.button("❌ Remove Interest", key=f"remove_int_{property_id}_{idx}", 
                                        help="Remove interest status"):
                                if remove_performance_tracking(tracking_key, "Interested"):
                                    st.success("✅ Interest removed!")
                                    st.rerun()
                        else:
                            # Show "Interested" button
                            if st.button("👍 Interested", key=f"interested_{property_id}_{idx}", 
                                        help="Mark as interested"):
                                track_performance(tracking_key, "Interested", "Search User", property_id)
                                st.success("✅ Marked as Interested!")
                                st.rerun()

                    with button_col2:
                        if status["closed"]:
                            # Show "Reopen Deal" button
                            if st.button("🔄 Reopen Deal", key=f"reopen_{property_id}_{idx}", 
                                        help="Reopen this deal"):
                                if remove_performance_tracking(tracking_key, "Deal Closed"):
                                    st.success("✅ Deal reopened!")
                                    st.rerun()
                        else:
                            # Show "Deal Closed" button (only if interested)
                            button_disabled = not status["interested"]
                            button_help = "Mark deal as closed" if not button_disabled else "Must mark as interested first"
                            
                            if st.button("🤝 Deal Closed", key=f"closed_{property_id}_{idx}", 
                                        disabled=button_disabled, help=button_help):
                                track_performance(tracking_key, "Deal Closed", "Search User", property_id)
                                st.success("🎉 Deal Closed recorded!")
                                st.rerun()

                    with button_col3:
                        # Show current status with enhanced info
                        if status["actions"]:
                            latest_action = status["actions"][-1]
                            
                            # Status indicator with color coding
                            if status["closed"]:
                                st.success(f"🎉 CLOSED - {latest_action['timestamp']}")
                            elif status["interested"]:
                                st.info(f"👍 INTERESTED - {latest_action['timestamp']}")
                            else:
                                st.info("Status: Available")
                            
                            # Show action count if multiple actions
                            if len(status["actions"]) > 1:
                                st.caption(f"📊 {len(status['actions'])} total actions")
                        else:
                            st.info("Status: Available")
        else:
            st.warning("🔍 No properties match your search criteria. Try adjusting the filters.")
            
    except Exception as e:
        st.error(f"Error in property search: {str(e)}")

def show_client_management(clients_df, properties_df, recommendations_df):
    """Client management interface with enhanced performance tracking"""
    # st.write("DEBUG - show_client_management function called.")
    st.title("Client Management")

    # Search and Filter Clients
    # Client search
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_client = st.text_input("🔍 Search by Client Name or ID", placeholder="Enter client name or ID...")
    
    with col2:
        client_status_filter = st.selectbox("Filter by Status", ["All"] + list(clients_df['status'].unique()) if 'status' in clients_df.columns else ["All"])
    
    try:
        # Apply filters
        filtered_clients = clients_df.copy()
        
        if search_client:
            filtered_clients = filtered_clients[
                filtered_clients['client_name'].str.contains(search_client, case=False, na=False) |
                filtered_clients['clientid'].str.contains(search_client, case=False, na=False)
            ]
        
        if client_status_filter != "All":
            filtered_clients = filtered_clients[filtered_clients['status'] == client_status_filter]
        
        if len(filtered_clients) == 0:
            filtered_clients = clients_df.head(20)  # Show first 20 if no search
        
        st.subheader(f"👥 Clients ({len(filtered_clients)} shown)")
        
        # Client statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'looking_for' in clients_df.columns:
                rent_clients = len(clients_df[clients_df['looking_for'] == 'Rent'])
                st.metric("Rental Seekers", rent_clients)
        
        with col2:
            if 'looking_for' in clients_df.columns:
                sale_clients = len(clients_df[clients_df['looking_for'] == 'Sale'])
                st.metric("Property Buyers", sale_clients)
        
        with col3:
            if 'status' in clients_df.columns:
                active_statuses = ['Actively Searching', 'Negotiating', 'Site Visit Planned']
                active_clients = len(clients_df[clients_df['status'].isin(active_statuses)])
                st.metric("Active Clients", active_clients)
        
        with col4:
            if 'status' in clients_df.columns:
                closed_clients = len(clients_df[clients_df['status'] == 'Deal Closed'])
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
                            st.write(f"**Budget:** {format_indian_currency(client['client_budget'])}")
                    
                    if pd.notna(client.get('requirements')):
                        st.markdown("**📝 Detailed Requirements:**")
                        st.write(client['requirements'])
                    
                    # Add recommended properties
                    st.markdown("**🏆 ML-Powered Recommended Properties:**")
                    # Score all properties for this client
                    scored_props = properties_df.copy()
                    scored_props['score'] = scored_props.apply(lambda prop: compute_property_score(client, prop), axis=1)
                    top_recs = scored_props.sort_values('score', ascending=False).head(3)

                    for idx, prop in top_recs.iterrows():
                        match_desc = []
                        if client['client_bhk'] == prop.get('bedrooms__bhk'): match_desc.append("BHK match")
                        if 'client_location' in client and client['client_location'].lower() in str(prop.get('area___locality', '')).lower(): match_desc.append("Location match")
                        price = prop.get('asking_price__â_¹') if prop['listing_type']=="Sale" else prop.get('monthly_rent__â_¹')
                        if abs(price - client['client_budget']) / max(client['client_budget'], 1) < 0.2: match_desc.append("Budget match")
                        
                        st.markdown(f"""
                        <div style='background:#111e31;padding:0.78em 1em;margin-bottom:7px;border-radius:9px;border:1px solid #334155'>
                            <b>{prop.get('property_id', '—')}</b> — {prop.get('area___locality', 'N/A')}, {prop.get('bedrooms__bhk', '--')} BHK <br>
                            <span style='color:#38bdf8'>Price: ₹{price:,.0f}</span>
                            <span style='color:#a3e635;margin-left:0.8em'>{', '.join(match_desc)}</span>
                        </div>
                        """, unsafe_allow_html=True)

                    # Show top recommendations with ENHANCED performance tracking - WITH UNDO
                    if 'client_id' in recommendations_df.columns:
                        client_recs = recommendations_df[recommendations_df['client_id'] == client['clientid']].head(5)
                        if len(client_recs) > 0:
                            st.markdown("**🎯 Top Recommendations:**")
# Display recommendations in a dataframe
                            st.dataframe(client_recs, use_container_width=True)

                            # Add download button for recommendations
                            st.download_button(
                                label="Download Recommendations as CSV",
                                data=client_recs.to_csv(index=False).encode('utf-8'),
                                file_name=f"recommendations_for_{client['client_name'].replace(' ', '_')}.csv",
                                mime="text/csv",
                                help="Download the top property recommendations for this client as a CSV file."
                            )
                            
                            for rec_idx, rec in client_recs.iterrows():
                                price_str = f"₹{rec['price_match']:,.0f}" if pd.notna(rec.get('price_match')) else "Price N/A"
                                bhk_str = f"{rec.get('bhk_match', 'N/A')} BHK"
                                location_str = rec.get('location_match', 'Location N/A')
                                score_str = f"{rec.get('similarity_score', 0):.1f}%"
                                
                                # Create a unique tracking key for each recommendation
                                rec_key = f"client_{client['clientid']}_prop_{rec.get('property_id', 'unknown')}_{rec_idx}"
                                
                                # Get current tracking status
                                status = get_tracking_status(rec_key)
                                
                                # Display recommendation with enhanced performance tracking
                                rec_col1, rec_col2, rec_col3, rec_col4 = st.columns([2, 1, 1, 1])
                                
                                with rec_col1:
                                    st.write(f"• **{rec.get('property_id', 'Unknown')}** - {bhk_str} in {location_str} - {price_str} (Match: {score_str})")
                                
                                with rec_col2:
                                    if status["interested"]:
                                        if st.button("❌ Remove", key=f"remove_{rec_key}", help="Remove interest"):
                                            if remove_performance_tracking(rec_key, "Interested"):
                                                st.success("✅ Removed!")
                                                st.rerun()
                                    else:
                                        if st.button("👍 Interested", key=f"int_{rec_key}", help="Mark client as interested"):
                                            track_performance(rec_key, "Interested", client.get('client_name', 'Unknown'), rec.get('property_id', 'Unknown'))
                                            st.success("✅ Interest tracked!")
                                            st.rerun()
                                
                                with rec_col3:
                                    if status["closed"]:
                                        if st.button("🔄 Reopen", key=f"reopen_{rec_key}", help="Reopen deal"):
                                            if remove_performance_tracking(rec_key, "Deal Closed"):
                                                st.success("✅ Reopened!")
                                                st.rerun()
                                    else:
                                        button_disabled = not status["interested"]
                                        button_help = "Mark deal as closed" if not button_disabled else "Must be interested first"
                                        if st.button("🤝 Close Deal", key=f"closed_{rec_key}", help=button_help, disabled=button_disabled):
                                            track_performance(rec_key, "Deal Closed", client.get('client_name', 'Unknown'), rec.get('property_id', 'Unknown'))
                                            st.success("🎉 Deal closed!")
                                            st.rerun()
                                
                                with rec_col4:
                                    # Show compact status
                                    if status["closed"]:
                                        st.success("🎉 CLOSED")
                                    elif status["interested"]:
                                        st.info("👍 INTERESTED")
                                    else:
                                        st.write("Available")
        
    except Exception as e:
        st.error(f"Error in client management: {str(e)}")

def show_analytics(recommendations_df, clients_df, properties_df):
    # st.write("DEBUG - show_analytics function called.")
    st.title("Analytics and Market Trends")

    st.header("Market Overview")
    st.markdown("---")
    
    try:
        # Market overview metrics with performance tracking
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'asking_price__â_¹' in properties_df.columns:
                sale_properties = properties_df[properties_df['listing_type'] == 'Sale']
                total_sale_value = sale_properties['asking_price__â_¹'].sum()
                st.metric("Total Sale Inventory", f"₹{total_sale_value/10000000:.1f} Cr")
        
        with col2:
            if 'asking_price__â_¹' in properties_df.columns:
                avg_sale_price = properties_df[properties_df['listing_type'] == 'Sale']['asking_price__â_¹'].mean()
                st.metric("Avg Sale Price", f"₹{avg_sale_price/10000000:.2f} Cr")
        
        with col3:
            if 'monthly_rent__â_¹' in properties_df.columns:
                avg_rent = properties_df[properties_df['listing_type'] == 'Rent']['monthly_rent__â_¹'].mean()
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
                        font=dict(color='#f9fafb', size=16),
                        title_font=dict(color='#38bdf8', size=22),
                        xaxis=dict(gridcolor='#374151', color='#f9fafb', title_font=dict(size=18)),
                        yaxis=dict(gridcolor='#374151', color='#f9fafb', title_font=dict(size=18)),
                        hovermode='closest'
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
                    daily_actions = pd.DataFrame(timeline_df.groupby(['Date', 'Action']).size()).reset_index()
                    daily_actions.columns = ['Date', 'Action', 'Count']

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
                        font=dict(color='#f9fafb', size=16),
                        title_font=dict(color='#38bdf8', size=22),
                        xaxis=dict(gridcolor='#374151', color='#f9fafb', title_font=dict(size=18)),
                        yaxis=dict(gridcolor='#374151', color='#f9fafb', title_font=dict(size=18)),
                        hovermode='closest'
                    )

                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No timeline data available yet.")

# ... existing code ...

        
    except Exception as e:
        st.error(f"Error in analytics: {str(e)}")

def show_data_management(clients_df, properties_df):
    """Data Management interface for adding/editing/deleting clients and properties"""
    import pandas as pd # Explicitly import pandas here
    st.title("Data Management")
    st.markdown("---")
    
    # Load Excel data
    with st.spinner("Loading Excel data..."):
        clients_df, properties_df, file_path = load_excel_data()
    
    if clients_df is None or properties_df is None:
        st.error("❌ Could not load Excel data files!")
        return
    
    # Tab layout for different operations
    tab1, tab2, tab3, tab4 = st.tabs(["Add New Client", "Add New Property", "Manage Clients", "Manage Properties"])
    
    # TAB 1: ADD CLIENT (PROPERLY FIXED FORM STRUCTURE)
    with tab1:
        st.subheader("➕ Add New Client")
        
        # Create the form with proper context
        with st.form("add_client_form", clear_on_submit=False):
            # All form elements must be inside this context
            col1, col2 = st.columns(2)
            
            with col1:
                client_name = st.text_input("Client Name*", help="Full official name.")
                client_phone = st.text_input("Phone*", help="Format: +91-XXXXXXXXXX (required)")
                client_email = st.text_input("Email", help="Optional.")
            
            with col2:
                client_bhk = st.selectbox("Preferred BHK", [1, 2, 3, 4, 5], help="Type of property desired.")
                looking_for = st.selectbox("Looking For*", ["Rent", "Sale"], help="Select rent or sale.")
                budget = st.number_input("Budget (₹)", min_value=10000, step=10000, value=50000, help="Maximum budget.")
                location_pref = st.text_input("Preferred Location", help="e.g., Mira Road East, Borivali.")
            
            requirements = st.text_area("Detailed Requirements", help="Any specific needs—floor, society, amenities, etc.")
            status = st.selectbox("Status", ["Actively Searching", "Just Browsing", "Negotiating", "Site Visit Planned"], help="Current stage.")
            submit = st.form_submit_button("Add Client")
        
        # Form processing logic - OUTSIDE the form
        if submit:
            missing = []
            if not client_name: missing.append("Client Name")
            if not client_phone: missing.append("Phone")
            if not looking_for: missing.append("Looking For")
            if missing:
                show_toast(f"Please fill required fields: {', '.join(missing)}", type="error")
            else:
                # Create new client record
                new_client = {
                    'clientid': generate_client_id(),
                    'client_name': client_name,
                    'client_phone': client_phone,
                    'client_email': client_email if client_email else "",
                    'looking_for': looking_for,
                    'requirements': requirements if requirements else f"{client_bhk} BHK {looking_for} in {location_pref}, Budget ₹{budget:,}",
                    'status': status,
                    'registration_date': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'client_bhk': client_bhk,
                    'client_budget': budget,
                    'client_location': location_pref,
                    'client_listing_type': looking_for
                }
                
                # Add to dataframe
                clients_df = pd.concat([clients_df, pd.DataFrame([new_client])], ignore_index=True)
                
                # Save to Excel
                if save_to_excel(clients_df, properties_df, file_path):
                    show_toast("Client added with success!", type="success")
                    st.success(f"📋 Client ID: {new_client['clientid']}")
                    
                    # Show formatted budget
                    st.success(f"💰 Budget: {format_indian_currency(budget)}")
                    st.balloons()
                else:
                    st.error("❌ Failed to save client data!")
    
    # TAB 2: ADD PROPERTY (PROPERLY FIXED FORM STRUCTURE)
    with tab2:
        st.subheader("🏠 Add New Property")
        
        # Create the form with proper context
        with st.form("add_property_form", clear_on_submit=False):
            # Form content starts here - everything must be indented properly
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**🏢 Basic Details**")
                property_type = st.selectbox("Property Type*", ["Apartment", "Bungalow", "Villa", "Office Space", "Shop"])
                listing_type = st.selectbox("Listing Type*", ["Sale", "Rent"])
                
                # Conditional BHK field
                if property_type == "Shop":
                    st.info("🛍️ Shops don't require BHK - automatically set to 0")
                    bedrooms = 0
                else:
                    bedrooms = st.selectbox("BHK*", [1, 2, 3, 4, 5, 6], index=2)
                
                # Conditional bathroom/restroom field
                if property_type == "Shop":
                    bathrooms = st.selectbox("Restrooms", options=[0, 1, 2, 3], index=1)
                else:
                    bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, value=2)
                
                area_sqft = st.number_input("Area (Sq. Ft.)*", min_value=100, max_value=10000, value=1000)
            
            with col2:
                st.markdown("**📍 Location & Building**")
                city = st.text_input("City*", value="Mira Bhayandar")
                locality = st.text_input("Area/Locality*", placeholder="e.g., Mira Road East")
                building_name = st.text_input("Building/Society", placeholder="Building name")
                floor_number = st.number_input("Floor Number", min_value=0, max_value=50, value=1)
                total_floors = st.number_input("Total Floors", min_value=1, max_value=50, value=10)
            
            with col3:
                st.markdown("**💰 Pricing & Features**")
                
                # Pricing section
                if listing_type == "Sale":
                    asking_price = st.number_input("Asking Price (₹)*", min_value=100000, max_value=1000000000, step=100000, value=1000000)
                    monthly_rent = None
                    
                    # Show formatted price preview
                    st.success(f"💰 Price: {format_indian_currency(asking_price)}")
                else:
                    monthly_rent = st.number_input("Monthly Rent (₹)*", min_value=5000, max_value=1000000, step=1000, value=25000)
                    asking_price = None
                    
                    # Show formatted rent preview
                    st.success(f"🏠 Rent: {format_indian_currency(monthly_rent)}/month")
                
                maintenance = st.number_input("Maintenance (₹/month)", min_value=0, max_value=50000, value=2000)
                
                # Conditional furnishing
                if property_type == "Shop":
                    furnishing_options = ["Unfurnished", "Basic Furnishing", "Fully Equipped"]
                    furnishing = st.selectbox("Shop Setup", furnishing_options)
                else:
                    furnishing = st.selectbox("Furnishing", ["Unfurnished", "Semi-Furnished", "Fully Furnished"])
                
                parking = st.number_input("Parking (Cars)", min_value=0, max_value=5, value=1)
            
            # Additional details row
            st.markdown("**🏗️ Additional Details**")
            col4, col5, col6 = st.columns(3)
            
            with col4:
                property_age = st.number_input("Property Age (Years)", min_value=0, max_value=100, value=5)
            
            with col5:
                area_type = st.selectbox("Area Type", ["Carpet", "Built-up", "Super Built-up"])
            
            with col6:
                facing = st.selectbox("Facing Direction", ["North", "South", "East", "West", "North-East", "North-West", "South-East", "South-West"])
            
            # CRITICAL: Submit button MUST be at this indentation level (inside the form)
            st.markdown("---")
            submitted_prop = st.form_submit_button("🏠 Add Property", type="primary", use_container_width=True)
        
        # Form processing logic - OUTSIDE the form but still properly indented
        if submitted_prop:
            # Validation
            if not property_type or not listing_type or not locality or area_sqft <= 0:
                st.error("❌ Please fill in all required fields (marked with *)")
            elif listing_type == "Sale" and (not asking_price or asking_price <= 0):
                st.error("❌ Please enter a valid asking price for sale properties!")
            elif listing_type == "Rent" and (not monthly_rent or monthly_rent <= 0):
                st.error("❌ Please enter a valid rent amount for rental properties!")
            else:
                # Create new property record
                new_property = {
                    'property_id': generate_property_id(property_type, listing_type),
                    'listing_type': listing_type,
                    'property_type': property_type,
                    'city': city,
                    'area___locality': locality,
                    'building___society': building_name if building_name else "",
                    'bedrooms__bhk': bedrooms,
                    'bathrooms': bathrooms,
                    'area__sq__ft': area_sqft,
                    'area_type': area_type,
                    'floor_number': floor_number,
                    'total_floors': total_floors,
                    'property_age__yrs': property_age,
                    'furnishing': furnishing,
                    'parking__cars': parking,
                    'facing_direction': facing,
                    'asking_price__â_¹': asking_price,
                    'monthly_rent__â_¹': monthly_rent,
                    'maint___month__â_¹': maintenance,
                    'price_negotiable': "Yes",
                    'listing_status': "Available",
                    'listing_date': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'normalized_location': locality.lower(),
                    'price_per_sqft': asking_price / area_sqft if asking_price else None,
                    'rent_per_sqft': monthly_rent / area_sqft if monthly_rent else None
                }
                
                # Add to dataframe
                try:
                    properties_df = pd.concat([properties_df, pd.DataFrame([new_property])], ignore_index=True)
                    
                    # Save to Excel
                    if save_to_excel(clients_df, properties_df, file_path):
                        st.success(f"✅ Property added successfully!")
                        st.success(f"🏠 **Property ID:** {new_property['property_id']}")
                        
                        # Show success summary
                        if property_type == "Shop":
                            st.balloons()
                            st.success(f"🛍️ **{property_type}** successfully added!")
                        else:
                            st.balloons()
                            st.success(f"🏠 **{bedrooms} BHK {property_type}** successfully added!")
                        
                    else:
                        st.error("❌ Failed to save property data to Excel files!")
                        
                except Exception as e:
                    st.error(f"❌ Error adding property: {str(e)}")
    
    # TAB 3: MANAGE CLIENTS (FIXED VERSION)
    with tab3:
        st.subheader("👥 Manage Existing Clients")
        
        # Search and filter
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("🔍 Search Clients", placeholder="Search by name, phone, or ID")
        with col2:
            show_count = st.selectbox("Show", [10, 25, 50, 100])
        
        # Latest Clients Cards Layout
        with st.expander("🆕 Show Latest Added Clients", expanded=False):
            latest_clients_count = st.slider("How many?", 1, min(8, len(clients_df)), 3, key="latest_clients_count")
            if 'registration_date' in clients_df.columns:
                latest_clients = clients_df.sort_values('registration_date', ascending=False).head(latest_clients_count)
            else:
                latest_clients = clients_df.tail(latest_clients_count)
            for _, cli in latest_clients.iterrows():
                cid = cli.get('clientid', 'N/A')
                cname = cli.get('client_name', '--')
                phone = cli.get('client_phone', '')
                dt = cli.get('registration_date', '')
                typ = cli.get('looking_for', '')
                status = cli.get('status', '')
                pretty_card(
                    title=cname,
                    left=f"📞 {phone}",
                    right=f"🗓️ {dt}",
                    chips=[typ, status],
                    status=status
                )

        st.markdown("---") # Separator for clarity
        
        # Filter clients - FIXED to handle non-string values
        filtered_clients = clients_df.copy()
        if search_term:
            # Convert to string and handle NaN values properly
            mask = (
                filtered_clients['client_name'].astype(str).str.contains(search_term, case=False, na=False) |
                filtered_clients['client_phone'].astype(str).str.contains(search_term, case=False, na=False) |
                filtered_clients['clientid'].astype(str).str.contains(search_term, case=False, na=False)
            )
            filtered_clients = filtered_clients[mask]
        
        st.write(f"📊 Showing {len(filtered_clients):,} clients")
        
        # Display clients with delete option
        if len(filtered_clients) > 0:
            for idx, client in filtered_clients.head(show_count).iterrows():
                with st.expander(f"👤 {client['client_name']} - {client['clientid']}"):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write(f"**Phone:** {client['client_phone']}")
                        st.write(f"**Email:** {client.get('client_email', 'N/A')}")
                        st.write(f"**Looking For:** {client['looking_for']}")
                    
                    with col2:
                        st.write(f"**Status:** {client['status']}")
                        budget = client.get('client_budget', 0)
                        if budget > 0:
                            st.write(f"**Budget:** {format_indian_currency(budget)}")
                        else:
                            st.write(f"**Budget:** Not specified")
                        st.write(f"**Location:** {client.get('client_location', 'N/A')}")
                    
                    with col3:
                        # Add confirmation checkbox before delete button
                        confirm_delete = st.checkbox(
                            "Confirm deletion", 
                            key=f"confirm_del_{idx}",
                            help="Check this box to enable delete button"
                        )
                        if st.button(
                            f"🗑️ Delete", 
                            key=f"del_client_{idx}", 
                            help="Delete this client",
                            disabled=not confirm_delete
                        ):
                            # Remove client from dataframe
                            clients_df_updated = clients_df.drop(idx).reset_index(drop=True)
                            
                            if save_to_excel(clients_df_updated, properties_df, file_path):
                                show_toast(f"✅ Client '{client['client_name']}' deleted!", type="success")
                                st.rerun()
                            else:
                                show_toast("❌ Failed to delete client!", type="error")
        else:
            st.info("No clients found matching your criteria.")
        
        st.markdown("---")
        st.subheader("Raw Client Data")
        st.subheader("👥 All Clients") # Added subheader
        if not clients_df.empty:
           selected = show_aggrid(clients_df) # Replaced st.dataframe with show_aggrid
           
           if st.button("Download Selected Clients (CSV)") and selected['selected_rows']:
               import pandas as pd
               sel_df = pd.DataFrame(selected['selected_rows'])
               st.download_button("⬇️ Download Selected", sel_df.to_csv(index=False), "selected_clients.csv", "text/csv")

           st.markdown("### Download Options")
           download_csv(clients_df, name="clients")
           download_excel(clients_df, name="clients")
        else:
            st.info("No clients to display.")
    
    # TAB 4: MANAGE PROPERTIES (FIXED VERSION)
    with tab4:
        st.subheader("🏢 Manage Existing Properties")
        
        # Search and filter
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search_prop = st.text_input("🔍 Search Properties", placeholder="Search by ID, location, or type")
        with col2:
            filter_type = st.selectbox("Filter Type", ["All", "Sale", "Rent"])
        with col3:
            show_prop_count = st.selectbox("Show Properties", [10, 25, 50])
            


        # Filter properties - FIXED to handle non-string values
        filtered_props = properties_df.copy()
        if search_prop:
            # Convert to string and handle NaN values properly
            mask = (
                filtered_props['property_id'].astype(str).str.contains(search_prop, case=False, na=False) |
                filtered_props['area___locality'].astype(str).str.contains(search_prop, case=False, na=False) |
                filtered_props['property_type'].astype(str).str.contains(search_prop, case=False, na=False)
            )
            filtered_props = filtered_props[mask]
        
        if filter_type != "All":
            filtered_props = filtered_props[filtered_props['listing_type'] == filter_type]
        
        st.write(f"🏠 Showing {len(filtered_props):,} properties")
        
        # Latest Properties Cards Layout
        with st.expander("🆕 Show Latest Added Properties", expanded=False):
            latest_count = st.slider("How many?", 1, min(8, len(properties_df)), 3, key="latest_props_count")
            if 'listing_date' in properties_df.columns:
                latest_df = properties_df.sort_values('listing_date', ascending=False).head(latest_count)
            else:
                latest_df = properties_df.tail(latest_count)
            for _, prop in latest_df.iterrows():
                propid = prop.get('property_id', 'N/A')
                locality = prop.get('area___locality', 'N/A')
                price = prop.get('asking_price__â_¹') or prop.get('monthly_rent__â_¹', 0)
                date = prop.get('listing_date', '')
                status = prop.get('listing_status', 'Available')
                pretty_card(
                    title=f"🏠 {propid}",
                    left=f"📍 {locality}",
                    right=f"💰 {format_indian_currency(price)}",
                    chips=[status, date],
                    status=status
                )

        # Display properties with delete option
        if len(filtered_props) > 0:
            for idx, prop in filtered_props.head(show_prop_count).iterrows():
                bhk_info = ""
                if prop['property_type'] != 'Shop' and pd.notna(prop['bedrooms__bhk']):
                    bhk_info = f" - {prop['bedrooms__bhk']} BHK"
                
                with st.expander(f"🏠 {prop['property_id']}{bhk_info} in {prop['area___locality']}"):
                    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                    
                    with col1:
                        st.write(f"**Type:** {prop['property_type']}")
                        st.write(f"**Area:** {format_area(prop['area__sq__ft'])}")
                        st.write(f"**Furnishing:** {prop['furnishing']}")
                    
                    with col2:
                        st.write(f"**Floor:** {prop['floor_number']}/{prop['total_floors']}")
                        st.write(f"**Parking:** {prop['parking__cars']} cars")
                        st.write(f"**Facing:** {prop['facing_direction']}")
                    
                    with col3:
                        if prop['listing_type'] == 'Sale':
                            price = prop['asking_price__â_¹']
                            st.write(f"**Price:** {format_indian_currency(price)}")
                            if pd.notna(prop.get('price_per_sqft')):
                                st.write(f"**Per Sq Ft:** ₹{prop['price_per_sqft']:,.0f}")
                        else:
                            rent = prop['monthly_rent__â_¹']
                            st.write(f"**Monthly Rent:** {format_indian_currency(rent)}")
                            if pd.notna(prop.get('rent_per_sqft')):
                                st.write(f"**Rent/Sq Ft:** ₹{prop['rent_per_sqft']:.0f}")
                        st.write(f"**Status:** {prop.get('listing_status', 'Available')}")
                    
                    with col4:
                        if st.button(f"🗑️ Delete", key=f"del_prop_{idx}", help="Delete this property"):
                            # Remove property from dataframe
                            properties_df_updated = properties_df.drop(idx).reset_index(drop=True)
                            
                            if save_to_excel(clients_df, properties_df_updated, file_path):
                                st.success(f"✅ Property '{prop['property_id']}' deleted!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete property!")
        else:
            st.info("No properties found matching your criteria.")
        
        st.markdown("---")
        st.subheader("Raw Property Data")
        st.subheader("🏢 All Properties") # Added subheader
        if not properties_df.empty:
            selected_props = show_aggrid(properties_df) # Replaced st.dataframe with show_aggrid
            download_csv(properties_df, name="properties")
            download_excel(properties_df, name="properties")
        else:
            st.info("No properties found matching your criteria.")
        
        # Summary statistics
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Properties", len(properties_df))
        with col2:
            sale_count = len(properties_df[properties_df['listing_type'] == 'Sale'])
            st.metric("For Sale", sale_count)
        with col3:
            rent_count = len(properties_df[properties_df['listing_type'] == 'Rent'])
            st.metric("For Rent", rent_count)
        with col4:
            total_clients = len(clients_df)
            st.metric("Total Clients", total_clients)

if __name__ == "__main__":
    main()
