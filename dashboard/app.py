import streamlit as st
import pandas as pd
import plotly.express as px
import glob
from pathlib import Path

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="NYC Taxi Analytics Dashboard",
    page_icon="🚕",
    layout="wide"
)

# ==================================================
# LOAD CSS
# ==================================================

with open("dashboard/styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS = BASE_DIR / "artifacts"

# ==================================================
# DATA LOADER
# ==================================================

@st.cache_data
def load_spark_csv(folder_name):

    folder = ARTIFACTS / "data_marts" / folder_name

    csv_files = glob.glob(str(folder / "*.csv"))

    if len(csv_files) == 0:
        return None

    return pd.read_csv(csv_files[0])


# ==================================================
# CHART STYLING FUNCTION
# ==================================================

def style_chart(fig):

    fig.update_layout(
        template="plotly_white",

        paper_bgcolor="white",
        plot_bgcolor="white",

        font=dict(
            family="Arial",
            size=14,
            color="#1E293B"
        ),

        title_font=dict(
            size=20,
            color="#0F172A"
        ),

        xaxis=dict(
            title_font=dict(
                color="#1E293B",
                size=14
            ),
            tickfont=dict(
                color="#1E293B"
            ),
            gridcolor="#E2E8F0"
        ),

        yaxis=dict(
            title_font=dict(
                color="#1E293B",
                size=14
            ),
            tickfont=dict(
                color="#1E293B"
            ),
            gridcolor="#E2E8F0"
        ),

        legend=dict(
            font=dict(
                color="#1E293B"
            )
        ),

        margin=dict(
            l=40,
            r=40,
            t=60,
            b=40
        )
    )

    return fig


# ==================================================
# LOAD DATA
# ==================================================

revenue_df = load_spark_csv("mart_yearly_revenue")
payment_df = load_spark_csv("mart_payment_analysis")
distance_df = load_spark_csv("mart_distance_analysis")
location_df = load_spark_csv("mart_location_analysis")
peak_df = load_spark_csv("mart_peak_hours")

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🚕 NYC Taxi")
st.sidebar.markdown("### Dashboard Filters")

if revenue_df is not None:

    years = sorted(
        revenue_df.iloc[:, 0].unique()
    )

    selected_years = st.sidebar.multiselect(
        "Select Years",
        options=years,
        default=years
    )

    revenue_df = revenue_df[
        revenue_df.iloc[:, 0].isin(selected_years)
    ]

# ==================================================
# HEADER
# ==================================================

st.title("🚕 NYC Taxi Analytics Dashboard")

st.markdown("""
Analysis of **213+ Million NYC Taxi Trips**
processed using **Apache Spark & PySpark**
between **2021 and 2026**
""")

st.markdown("---")

# ==================================================
# KPI CARDS
# ==================================================

c1, c2, c3, c4, c5 = st.columns(5)

metrics = [
    ("187.2M", "Trips"),
    ("$4.79B", "Revenue"),
    ("$17.34", "Avg Fare"),
    ("$3.23", "Avg Tip"),
    ("2.4M", "Anomalies")
]

for col, (value, title) in zip(
    [c1, c2, c3, c4, c5],
    metrics
):

    col.markdown(
        f"""
        <div class='metric-card'>
            <h3>{value}</h3>
            <p>{title}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("## 📊 Business Insights")

# ==================================================
# ROW 1
# ==================================================

left, right = st.columns(2)

with left:

    st.subheader("💰 Revenue by Year")

    if revenue_df is not None:

        fig = px.bar(
            revenue_df,
            x=revenue_df.columns[0],
            y=revenue_df.columns[1],
            color=revenue_df.columns[1],
            text_auto=".2s"
        )

        fig.update_traces(
            textfont_color="#1E293B"
        )

        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            theme=None
        )

with right:

    st.subheader("💳 Payment Distribution")

    if payment_df is not None:

        fig = px.pie(
            payment_df,
            names=payment_df.columns[0],
            values=payment_df.columns[1],
            hole=0.55
        )

        fig.update_traces(
            textfont=dict(
                color="#1E293B",
                size=14
            )
        )

        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            theme=None
        )

# ==================================================
# ROW 2
# ==================================================

left, right = st.columns(2)

with left:

    st.subheader("🕒 Peak Hour Analysis")

    if peak_df is not None:

        fig = px.line(
            peak_df,
            x=peak_df.columns[0],
            y=peak_df.columns[1],
            markers=True
        )

        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            theme=None
        )

with right:

    st.subheader("📏 Distance Analysis")

    if distance_df is not None:

        fig = px.bar(
            distance_df,
            x=distance_df.columns[0],
            y=distance_df.columns[1],
            color=distance_df.columns[1],
            text_auto=".2s"
        )

        fig.update_traces(
            textfont_color="#1E293B"
        )

        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            theme=None
        )

# ==================================================
# LOCATION ANALYSIS
# ==================================================

st.subheader("📍 Location Analysis")

if location_df is not None:

    fig = px.bar(
        location_df,
        x=location_df.columns[0],
        y=location_df.columns[1],
        color=location_df.columns[1],
        text_auto=".2s"
    )

    fig.update_traces(
        textfont_color="#1E293B"
    )

    fig = style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        theme=None
    )

# ==================================================
# DATA QUALITY SECTION
# ==================================================

st.markdown("---")

st.subheader("🚨 Data Quality & Anomaly Detection")

st.success("""
✔ Processed 213+ Million taxi trips

✔ Removed 26+ Million invalid records

✔ Detected 2.4 Million suspicious transactions

✔ Corrected schema inconsistencies across 64 datasets
""")

st.info("""
Common anomalies discovered:

• Unrealistic trip durations

• Negative fare amounts

• Invalid passenger counts

• Corrupted timestamps

• Suspiciously large transactions
""")