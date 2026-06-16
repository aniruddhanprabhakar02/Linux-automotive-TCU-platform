import streamlit as st
import sqlite3
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

from geopy.distance import geodesic

from streamlit_autorefresh import st_autorefresh

# -----------------------------
# Page Config
# -----------------------------

st_autorefresh(
    interval=4000,
    key="dashboard_refresh"
)

st.set_page_config(
    page_title="TCU Dashboard",
    layout="wide"
)

st.title("Linux-Based TCU Dashboard")

# -----------------------------
# Database Connection
# -----------------------------

conn = sqlite3.connect(
    "vehicle_telematics_v2.db"
)



#-------analytics window func---------------#

@st.cache_data(ttl=10)
def get_analytics():

    return pd.read_sql_query(
        """
        SELECT
            COUNT(*) AS total_records,
            AVG(speed) AS avg_speed,
            MAX(rpm) AS max_rpm,
            AVG(fuel) AS avg_fuel,
            MAX(engine_temp) AS max_temp
        FROM telematics
        """,
        conn
    )


#---------distance calc func---------------------#

@st.cache_data(ttl=10)
def get_total_distance():

    gps_data = pd.read_sql_query(
        """
        SELECT latitude, longitude
        FROM telematics
        ORDER BY id ASC
        """,
        conn
    )

    total_distance = 0.0

    for i in range(1, len(gps_data)):

        point1 = (
            gps_data.iloc[i-1]["latitude"],
            gps_data.iloc[i-1]["longitude"]
        )

        point2 = (
            gps_data.iloc[i]["latitude"],
            gps_data.iloc[i]["longitude"]
        )

        total_distance += geodesic(
            point1,
            point2
        ).kilometers

    return total_distance


# -----------------------------
# Latest Data
# -----------------------------

latest = pd.read_sql_query(
    """
    SELECT *
    FROM telematics
    ORDER BY id DESC
    LIMIT 1
    """,
    conn
)

if not latest.empty:

    row = latest.iloc[0]

    # =========================================
    # INSTRUMENT CLUSTER
    # =========================================

    st.header("Instrument Cluster")

    speed_col, rpm_col = st.columns(2)
    
    # -----------------------------------------
    # SPEED GAUGE
    # -----------------------------------------

    with speed_col:

        fig_speed_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=row["speed"],
                title={"text": "Speed (km/h)"},
                gauge={
                    "axis": {"range": [0, 120]},

                    "bar": {"color": "white"},

                    "steps": [
                        {"range": [0, 80], "color": "green"},
                        {"range": [80, 100], "color": "yellow"},
                        {"range": [100, 120], "color": "red"}
                    ]
                }
            )
        )

        st.plotly_chart(
            fig_speed_gauge,
            use_container_width=True
        )

    # -----------------------------------------
    # RPM GAUGE
    # -----------------------------------------

    with rpm_col:

        fig_rpm_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=row["rpm"],
                title={"text": "RPM"},
                gauge={
                    "axis": {"range": [0, 6000]},

                    "bar": {"color": "white"},

                    "steps": [
                        {"range": [0, 4000], "color": "green"},
                        {"range": [4000, 5000], "color": "yellow"},
                        {"range": [5000, 6000], "color": "red"}
                    ]
                }
            )
        )

        st.plotly_chart(
            fig_rpm_gauge,
            use_container_width=True
        )

    # -----------------------------------------
    # FUEL + TEMP GAUGES
    # -----------------------------------------

    fuel_col, temp_col = st.columns(2)

    with fuel_col:

        fig_fuel_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=row["fuel"],
                title={"text": "Fuel (%)"},
                gauge={
                    "axis": {"range": [0, 100]},

                    "bar": {"color": "white"},

                    "steps": [
                        {"range": [0, 15], "color": "red"},
                        {"range": [15, 30], "color": "yellow"},
                        {"range": [30, 100], "color": "green"}
                    ]
                }
            )
        )

        st.plotly_chart(
            fig_fuel_gauge,
            use_container_width=True
        )

    with temp_col:

        fig_temp_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=row["engine_temp"],
                title={"text": "Engine Temp (C)"},
                gauge={
                    "axis": {"range": [80, 120]},

                    "bar": {"color": "white"},

                    "steps": [
                        {"range": [80, 95], "color": "green"},
                        {"range": [95, 100], "color": "yellow"},
                        {"range": [100, 120], "color": "red"}
                    ]
                }
            )
        )

        st.plotly_chart(
            fig_temp_gauge,
            use_container_width=True
        )

    # =========================================
    # VEHICLE ALERT PANEL (V2.2 + V2.2.1)
    # =========================================

    st.markdown("---")
    st.subheader("Vehicle Alerts")

    alerts = []

    # -----------------------------
    # Engine Temperature
    # -----------------------------

    if row["engine_temp"] >= 100:

        alerts.append(
            "ENGINE OVERHEATING"
        )

    # -----------------------------
    # Fuel
    # -----------------------------

    if row["fuel"] <= 15:

        alerts.append(
            "LOW FUEL"
        )

# -----------------------------
# RPM
# -----------------------------

    if row["rpm"] >= 5000:

        alerts.append(
            "HIGH RPM"
        )

# -----------------------------
# Speed
# -----------------------------

    if row["speed"] >= 100:

        alerts.append(
            "OVERSPEED"
        )

# -----------------------------
# Display Alert Panel
# -----------------------------

    if len(alerts) == 0:

        st.success(
            "VEHICLE HEALTHY"
        )

    else:

        alert_text = "<br><br>".join(alerts)

        st.markdown(
            f"""
            <div style="
                border:2px solid red;
                padding:20px;
                border-radius:10px;
                background-color:#330000;
                font-size:22px;
                font-weight:bold;
            ">
            {alert_text}
            </div>
            """,
            unsafe_allow_html=True
        )
    # =========================================
    # LIVE METRICS
    # =========================================

    st.markdown("---")
    st.header("Live Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Speed",
        f"{row['speed']} km/h"
    )

    col2.metric(
        "RPM",
        int(row["rpm"])
    )

    col3.metric(
        "Fuel",
        f"{row['fuel']} %"
    )

    col4.metric(
        "Engine Temp",
        f"{row['engine_temp']} C"
    )

    # =========================================
    # GPS INFORMATION
    # =========================================

    st.markdown("---")
    st.header("GPS Information")

    gps1, gps2 = st.columns(2)

    gps1.metric(
        "Latitude",
        f"{row['latitude']:.4f}"
    )

    gps2.metric(
        "Longitude",
        f"{row['longitude']:.4f}"
    )
    
    # =========================================
    # GPS MAP
    # =========================================

    st.markdown("---")
    st.header("Live Vehicle Tracking")
    gps_df = pd.read_sql_query(
    """
    SELECT latitude, longitude
    FROM telematics
    ORDER BY id DESC
    LIMIT 50
    """,
    conn
    )
    
    gps_df = gps_df.iloc[::-1]
    # -----------------------------------------
    # Route Line
    # -----------------------------------------

    fig_map = px.line_map(
        gps_df,
        lat="latitude",
        lon="longitude",
        zoom=14,
        height=600
    )

    # -----------------------------------------
    # Current Vehicle Position
    # -----------------------------------------

    current_lat = gps_df.iloc[-1]["latitude"]
    current_lon = gps_df.iloc[-1]["longitude"]

    fig_map.add_scattermap(
        lat=[current_lat],
        lon=[current_lon],
        mode="markers",
        marker=dict(
            size=18
        ),
        name="Current Position"
    )

    fig_map.update_layout(
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        )
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True
    )
    




# =========================================
# ANALYTICS SUMMARY
# =========================================

st.markdown("---")
st.header("Analytics Summary")

analytics = get_analytics()
distance_km = get_total_distance()

stats = analytics.iloc[0]

a1, a2, a3, a4, a5, a6 = st.columns(6)

a1.metric(
    "Total Records",
    int(stats["total_records"])
)

a2.metric(
    "Average Speed",
    f"{stats['avg_speed']:.1f} km/h"
)

a3.metric(
    "Maximum RPM",
    int(stats["max_rpm"])
)

a4.metric(
    "Average Fuel",
    f"{stats['avg_fuel']:.1f} %"
)

a5.metric(
    "Maximum Temp",
    f"{stats['max_temp']} C"
)

a6.metric(
    "Distance Travelled",
    f"{distance_km:.2f} km"
)


# -----------------------------
# Historical Data
# -----------------------------

df = pd.read_sql_query(
    """
    SELECT *
    FROM telematics
    ORDER BY id DESC
    LIMIT 50
    """,
    conn
)

df = df.sort_values("id")

df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)

st.markdown("---")
st.header("Historical Telemetry")

# =========================================
# SPEED HISTORY
# =========================================

st.subheader("Speed History")

fig_speed = px.line(
    df,
    x="timestamp",
    y="speed",
    title="Speed vs Time"
)

st.plotly_chart(
    fig_speed,
    use_container_width=True
)

# =========================================
# RPM HISTORY
# =========================================

st.subheader("RPM History")

fig_rpm = px.line(
    df,
    x="timestamp",
    y="rpm",
    title="RPM vs Time"
)

st.plotly_chart(
    fig_rpm,
    use_container_width=True
)

# =========================================
# FUEL HISTORY
# =========================================

st.subheader("Fuel History")

fig_fuel = px.line(
    df,
    x="timestamp",
    y="fuel",
    title="Fuel vs Time"
)

st.plotly_chart(
    fig_fuel,
    use_container_width=True
)

# =========================================
# ENGINE TEMPERATURE HISTORY
# =========================================

st.subheader("Engine Temperature History")

fig_temp = px.line(
    df,
    x="timestamp",
    y="engine_temp",
    title="Engine Temperature vs Time"
)

st.plotly_chart(
    fig_temp,
    use_container_width=True
)

conn.close()
