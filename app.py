import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("city_personality_joined2.csv")

joined = load_data()

st.title("City Personality Traits Map")

# Sidebar
st.sidebar.header("Filters")

# Personality variable selection for coloring
personality_vars = ["extraversion_scaled", "neuroticism_scaled", "agreeableness_scaled", "conscientiousness_scaled", "openness_scaled"]
personality_var = st.sidebar.selectbox(
    "Select personality variable to color cities by:",
    personality_vars
)

# Function to create filters for each personality trait
def create_trait_filter(trait):
    min_val = joined[trait].min()
    max_val = joined[trait].max()
    return st.sidebar.slider(
        f"{trait.split('_')[0].capitalize()} range",
        min_value=float(min_val),
        max_value=float(max_val),
        value=(float(min_val), float(max_val)),
        step=0.1
    )

# Create filters for each personality trait
trait_filters = {trait: create_trait_filter(trait) for trait in personality_vars}

# Population filter with log scale
st.sidebar.subheader("Population Filter")
min_pop = joined['pop'].min()
max_pop = joined['pop'].max()
log_min = np.log10(min_pop)
log_max = np.log10(max_pop)

log_pop_range = st.sidebar.slider(
    "Population range (log scale)",
    min_value=log_min,
    max_value=log_max,
    value=(log_min, log_max),
    step=0.1
)

# Convert log values back to linear scale
pop_range = (10**log_pop_range[0], 10**log_pop_range[1])

st.sidebar.write(f"Selected population range: {int(pop_range[0]):,} to {int(pop_range[1]):,}")

# Filter data based on all selected ranges
filtered_data = joined[
    (joined['pop'] >= pop_range[0]) & (joined['pop'] <= pop_range[1]) &
    (joined['extraversion_scaled'] >= trait_filters['extraversion_scaled'][0]) & (joined['extraversion_scaled'] <= trait_filters['extraversion_scaled'][1]) &
    (joined['neuroticism_scaled'] >= trait_filters['neuroticism_scaled'][0]) & (joined['neuroticism_scaled'] <= trait_filters['neuroticism_scaled'][1]) &
    (joined['agreeableness_scaled'] >= trait_filters['agreeableness_scaled'][0]) & (joined['agreeableness_scaled'] <= trait_filters['agreeableness_scaled'][1]) &
    (joined['conscientiousness_scaled'] >= trait_filters['conscientiousness_scaled'][0]) & (joined['conscientiousness_scaled'] <= trait_filters['conscientiousness_scaled'][1]) &
    (joined['openness_scaled'] >= trait_filters['openness_scaled'][0]) & (joined['openness_scaled'] <= trait_filters['openness_scaled'][1])
]

# Create map
fig = px.scatter_mapbox(filtered_data,
                        lat="lat",
                        lon="long",
                        color=personality_var,
                        size="pop",
                        hover_name="city",
                        hover_data={
                            "state": True,
                            "extraversion_scaled": ':.2f',
                            "neuroticism_scaled": ':.2f',
                            "agreeableness_scaled": ':.2f',
                            "conscientiousness_scaled": ':.2f',
                            "openness_scaled": ':.2f',
                            "pop": True,
                            "lat": False,
                            "long": False
                        },
                        color_continuous_scale=px.colors.diverging.RdBu_r,
                        size_max=50,
                        zoom=3,
                        mapbox_style="carto-positron")

fig.update_traces(marker=dict(sizemin=5))

# Make the map bigger
fig.update_layout(height=800, width=1000)

# Use the full width of the page for the map
st.plotly_chart(fig, use_container_width=True)

# Display the number of cities shown
st.write(f"Number of cities displayed: {len(filtered_data)}")

st.text("Hover over a point to see details of personality traits")
