#import libraries
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Nigeria Jiji Housing Marketplace",
    page_icon="🏡",
    layout="wide"
)

def format_number(num):
        if num >= 1_000_000_000:
          return f"{num / 1_000_000_000:.1f}B"
        elif num >= 1_000_000:
          return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
          return f"{num / 1_000:.1f}K"
        else:
          return str(num)

#load_dataset
@st.cache_data
def load_data():
    df = pd.read_csv("jiji_housing_cleaned.csv")

    return df

df = load_data()

def main():
    #sidebar
    st.sidebar.header("🏡 Nigeria Jiji Housing Marketplace")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filter Options")

    title_filter = st.sidebar.selectbox(
            "Select Title:",
            options=["All Title"] + sorted(df["title"].unique().tolist())
        )

    region_parent_name_filter = st.sidebar.selectbox(
        "Select Regions:",
        options=["All Regions"] + sorted(df["region_parent_name"].unique().tolist())
    )

    is_boost_filter = st.sidebar.multiselect(
        "Select Package:",
        options=(df["is_boost"].unique().tolist())
    )

    furnishing_filter = st.sidebar.multiselect(
        "Select Furnish Type:",
        options=(df["furnishing"].unique().tolist())
    )

    #filter data
    filtered_data = df.copy()
    if title_filter != "All Title":
        filtered_data = filtered_data[filtered_data["title"] == title_filter]

    if region_parent_name_filter != "All Regions":
        filtered_data = filtered_data[filtered_data["region_parent_name"] == region_parent_name_filter]

    if is_boost_filter:
        filtered_data = filtered_data[filtered_data["is_boost"].isin(is_boost_filter)]

    if furnishing_filter:
        filtered_data = filtered_data[filtered_data["furnishing"].isin(furnishing_filter)]

    #main content
    st.title("🏡 Nigeria Jiji Housing Marketplace")
    st.markdown("---")


#KPI
    col1,  col2, col3, col4 = st.columns(4)
    with col1:
        total_price = filtered_data["price"].sum()
        st.metric("Total Price", f"₦{format_number(total_price)}")

    with col2:
        houses_available = len(filtered_data)
        st.metric("Available Houses", f"{houses_available:,}")

    with col3:
        avg_price = filtered_data["price"].mean()
        st.metric("Avg Price", f"₦{format_number(avg_price)}")

    with col4:
        furnish_type = filtered_data["furnishing"].nunique()
        st.metric("Furnish Types", furnish_type)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 5 Sales by Region")
        region_sales = filtered_data.groupby("region_parent_name")["price"].sum().sort_values(ascending=False).head(5).reset_index()
        fig_region = px.bar(
            region_sales,
            x="region_parent_name",
            y="price",
            text="price"
        )
    
        fig_region.update_layout(height=400)
        st.plotly_chart(fig_region, use_container_width=True)

    with col2:
        st.subheader("Furnishing Distribution")
        furnish_chart = filtered_data["furnishing"].value_counts().reset_index()
        furnish_chart.columns = ["Furnishing", "Count"]

        fig_furnish = px.pie(
                furnish_chart,
                names="Furnishing",
                values="Count",
                hole=0.4
        )

        fig_furnish.update_layout(height=400)
        st.plotly_chart(fig_furnish, use_container_width=True)

        
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Price Distribution")
        fig_price = px.histogram(
        df,
        x="price",
        nbins=50
        )

        fig_price.update_layout(
        height=400,
        xaxis_title="Price",
        yaxis_title="Number of Listings"
        )

        st.plotly_chart(fig_price, use_container_width=True)

    with col2:
        st.subheader("Boost Package Performance")

        boost_chart = (
            df.groupby("is_boost")["price"].mean().reset_index()
        )

        fig_boost = px.bar(
            boost_chart,
            x="is_boost",
            y="price",
            text="price"
        )

        fig_boost.update_traces(
            text=boost_chart["price"].apply(lambda x: f"₦{format_number(x)}"),
            textposition="outside"
        )

        fig_boost.update_layout(
            height=400,
            xaxis_title="Boost Status",
            yaxis_title="Average Price (₦)"
        )

        st.plotly_chart(fig_boost, use_container_width=True)

    st.markdown("---")
    st.caption("Nigeria Jiji Housing Marketplace Dashboard | Data update in real time.")

if __name__ == "__main__":
    main()