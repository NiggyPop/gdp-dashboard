
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the data
df = pd.read_csv("immigration_term_comparison.csv")

# Sidebar filters
st.sidebar.header("Filter Data")
selected_categories = st.sidebar.multiselect(
    "Select categories to display:",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

selected_years = st.sidebar.multiselect(
    "Select term years:",
    options=df["Term Year"].unique(),
    default=df["Term Year"].unique()
)

# Filtered data
filtered_df = df[
    df["Category"].isin(selected_categories) & 
    df["Term Year"].isin(selected_years)
]

# Define colorblind-friendly palette
colors = [
    "#332288", "#117733", "#44AA99", "#88CCEE", "#DDCC77",
    "#CC6677", "#AA4499", "#882255", "#661100", "#999933"
]
color_map = {cat: colors[i % len(colors)] for i, cat in enumerate(df["Category"].unique())}

# Plot
fig = go.Figure()
for cat in selected_categories:
    df_cat = filtered_df[filtered_df["Category"] == cat]
    fig.add_trace(go.Bar(
        x=df_cat["Term Year"],
        y=df_cat["Previous Term"],
        name=f"{cat} - Previous",
        marker_color=color_map[cat],
        offsetgroup=cat,
        legendgroup=cat
    ))
    fig.add_trace(go.Bar(
        x=df_cat["Term Year"],
        y=df_cat["Current Term"],
        name=f"{cat} - Current",
        marker_color=color_map[cat],
        offsetgroup=cat,
        legendgroup=cat,
        opacity=0.6
    ))

fig.update_layout(
    barmode="group",
    title="Immigration Data Comparison by Presidential Term Year",
    xaxis_title="Term Year",
    yaxis_title="Number of People",
    legend_title="Category",
    template="plotly_white"
)

# Display
st.title("Immigration Comparison Dashboard")
st.plotly_chart(fig, use_container_width=True)
