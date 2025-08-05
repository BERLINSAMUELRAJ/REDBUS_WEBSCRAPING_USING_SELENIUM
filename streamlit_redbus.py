import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# --- Inject Custom CSS ---
st.markdown("""
    <style>
        .title-container {
            padding-top: 10px;
            margin-bottom: 20px;
        }
        .big-title {
            font-size: 36px;
            font-weight: 700;
            text-align: center;
        }
        .metric-card {
            border: 1px solid #e0e0e0;
            border-radius: 15px;
            padding: 15px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 10px;
            text-align: center;
            background-color: #f9f9f9;
        }
        .metric-title {
            font-size: 18px;
            font-weight: 600;
            color: #444444;
        }
        .metric-value {
            font-size: 22px;
            font-weight: bold;
            color: #222222;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-container"><h1 class="big-title">Redbus India – Bus Routes & Operators</h1></div>', unsafe_allow_html=True)

# --- DB Connection ---
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        port=3306,
        database="redbus_data"
    )

# --- Fetch Data ---
def fetch_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM buses;", conn)
    conn.close()
    return df

st.set_page_config(layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🏠 HOME", use_container_width=True):
        st.session_state.page = "home"
with col2:
    if st.button("🗺️ States and Routes", use_container_width=True):
        st.session_state.page = "routes"

# Load and clean data
df_raw = fetch_data()

if 'id' in df_raw.columns:
    df_raw = df_raw.drop(columns=['id'])

df_raw['date_of_scrape'] = pd.to_datetime(df_raw['date_of_scrape']).dt.strftime('%d-%m-%Y')

transport_mapping = {
    "Kerala RTC Online Ticket Booking": ("KSRTC", "Kerala"),
    "APSRTC": ("APSRTC", "Andhra Pradesh"),
    "TSRTC Online Bus Ticket Booking": ("TGSRTC", "Telangana"),
    "Kadamba Transport Corporation Limited": ("KTCL", "Goa"),
    "RSRTC": ("RSRTC", "Rajasthan"),
    "South Bengal State Transport Corporation": ("SBSTC", "West Bengal"),
    "HRTC": ("HRTC", "Himachal Pradesh"),
    "Assam State Transport Corporation": ("ASTC", "Assam"),
    "Uttar Pradesh State Road Transport Corporation": ("UPSRTC", "Uttar Pradesh"),
    "WBTC (CTC)": ("WBTC", "West Bengal"),
}

def get_transport_info(state_name):
    for keyword, (corp, state) in transport_mapping.items():
        if keyword.lower() in str(state_name).lower():
            return corp, state
    return "", ""

df_raw.insert(2, 'TRANSPORT CORPORATION', df_raw['state_name'].apply(lambda x: get_transport_info(x)[0]))
df_raw.insert(3, 'STATE', df_raw['state_name'].apply(lambda x: get_transport_info(x)[1]))
df_raw.index = df_raw.index + 1
df_raw.index.name = "S.No"

# ==============================
# -------- HOME PAGE ----------
# ==============================
if st.session_state.page == "home":
    st.subheader("📊 Top-Level Transport Metrics")

    total_buses = len(df_raw)
    total_govt = len(df_raw[df_raw['type'].str.lower().str.contains('gov')])
    total_private = total_buses - total_govt
    unique_routes = df_raw['route_name'].nunique()
    unique_corporations = df_raw['TRANSPORT CORPORATION'].nunique()
    latest_scrape_date = df_raw['date_of_scrape'].max()

    def card(title, value):
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
        """, unsafe_allow_html=True)

    row1 = st.columns(3)
    with row1[0]: card("🚌 Total Buses", f"{total_buses:,}")
    with row1[1]: card("🏫 Govt Buses", f"{total_govt:,}")
    with row1[2]: card("🚍 Private Buses", f"{total_private:,}")

    row2 = st.columns(3)
    with row2[0]: card("📍 Unique Routes", unique_routes)
    with row2[1]: card("🏢 Transport Corporations", unique_corporations)
    with row2[2]: card("📅 Date Of Journey", latest_scrape_date)

    st.subheader("📈 Operational Insights: Bus Services")

    top_routes = df_raw['route_name'].value_counts().nlargest(10).reset_index()
    top_routes.columns = ['Route', 'Bus Count']
    fig_top_routes = px.bar(
        top_routes,
        x='Route',
        y='Bus Count',
        title="Top 10 Routes with Most Buses",
        color_discrete_sequence=["#1B93D9"]  # Teal
    )
    st.plotly_chart(fig_top_routes, use_container_width=True)

    fig_pie = px.pie(
        df_raw,
        names='type',
        title='Govt vs Private Bus Ratio',
        color='type',
        color_discrete_map={
            "Private": "#FF6F61",     # Coral
            "Government": "#054c80"   # Teal
        }
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("💰 Top 10 Routes by Average Ticket Price")
    price_df = df_raw.groupby("route_name")["price"].mean().sort_values(ascending=False).head(10).reset_index()
    price_df = price_df.rename(columns={"route_name": "Route", "price": "Price (Rs)"})
    fig_price = px.bar(
        price_df,
        x="Route",
        y="Price (Rs)",
        title="Top 10 Routes with Highest Avg. Price",
        text_auto='.2s',
        color_discrete_sequence=["#2E8B57"]  # Sea
    )
    st.plotly_chart(fig_price, use_container_width=True)

# ==============================
# ----- STATES & ROUTES -------
# ==============================
elif st.session_state.page == "routes":
    st.subheader("📍 States and Routes")

    with st.expander("🔎 Filter Options"):
        df_filtered = df_raw.copy()

        # Filter by Bus Type
        bus_type = st.selectbox("Select Bus Type", ["All", "Government", "Private"])
        if bus_type != "All":
            df_filtered = df_filtered[df_filtered['type'].str.lower().str.contains(bus_type.lower())]

        # Filter by State
        selected_state = st.selectbox("Select State", ["All"] + sorted(df_filtered['STATE'].dropna().unique().tolist()))
        if selected_state != "All":
            df_filtered = df_filtered[df_filtered['STATE'] == selected_state]

        # Filter by Price Range
        if not df_filtered['price'].isna().all():
            min_price = int(df_filtered['price'].min())
            max_price = int(df_filtered['price'].max())
            price_range = st.slider("Filter by Price Range", min_value=min_price, max_value=max_price, value=(min_price, max_price))
            df_filtered = df_filtered[(df_filtered['price'] >= price_range[0]) & (df_filtered['price'] <= price_range[1])]

        # A/C or Non A/C Bus Filter
        def classify_ac_type(bustype):
            text = str(bustype).lower()
            if any(ac in text for ac in ['a/c', 'ac', 'a c']):
                if 'non' in text:
                    return "Non A/C Bus"
                return "A/C Bus"
            return "Non A/C Bus"

        df_filtered['AC Type'] = df_filtered['bustype'].apply(classify_ac_type)

        selected_ac_type = st.selectbox("Select A/C or Non A/C Bus", ["All", "A/C Bus", "Non A/C Bus"])
        if selected_ac_type != "All":
            df_filtered = df_filtered[df_filtered['AC Type'] == selected_ac_type]

        # Filter by Departure Hour
        df_filtered['depart_hour'] = pd.to_datetime(df_filtered['departing_time'], format='%H:%M', errors='coerce').dt.hour
        if not df_filtered['depart_hour'].isna().all():
            min_hour = int(df_filtered['depart_hour'].min())
            max_hour = int(df_filtered['depart_hour'].max())
            hour_range = st.slider("Filter by Departure Hour", min_value=min_hour, max_value=max_hour, value=(min_hour, max_hour))
            df_filtered = df_filtered[(df_filtered['depart_hour'] >= hour_range[0]) & (df_filtered['depart_hour'] <= hour_range[1])]

    # Display Table
    display_df = df_filtered.drop(columns=['state_name', 'depart_hour'], errors='ignore').rename(columns={
        "route_name": "Route",
        "TRANSPORT CORPORATION": "Transport Corporation",
        "STATE": "State",
        "busname": "Bus Name",
        "price": "Price",
        "bustype": "Bus Type",
        "departing_time": "Departure",
        "duration": "Duration",
        "reaching_time": "Arrival",
        "star_rating": "Star Rating",
        "seats_available": "Seats Available",
        "type": "Govt/Private",
        "date_of_scrape": "Date Of Journey",
        "AC Type": "A/C Type"
    })

    st.dataframe(display_df, use_container_width=True, height=700)











