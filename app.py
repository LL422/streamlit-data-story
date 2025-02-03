import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --- Title and Introduction ---
st.title("The Relationship Between Economic Growth and Meat Consumption")

st.markdown("""
### Main Idea
This project explores the relationship between economic growth (measured by GDP per capita) and meat consumption in various countries, with a focus on comparing developed and developing nations. By analyzing these trends, we aim to uncover how economic prosperity influences dietary habits and how cultural, environmental, and economic factors shape meat consumption patterns globally.

---
""")

# --- Load Data ---
@st.cache_data
def load_data():
    meat_data = pd.read_csv('Consumption of meat per capita.csv')
    gdp_data = pd.read_csv('GDP per capita PPP.csv')

    # Prepare GDP data
    gdp_data.rename(columns={'GDP per capita, PPP (constant 2017 international $)': 'GDP_per_capita'}, inplace=True)
    meat_data['Year'] = meat_data['Year'].astype(int)
    gdp_data['Year'] = gdp_data['Year'].astype(int)

    # Merge datasets
    merged_data = pd.merge(meat_data, gdp_data[['Entity', 'Year', 'GDP_per_capita']], on=['Entity', 'Year'], how='inner')

    # Calculate total meat consumption per capita
    meat_columns = ['Poultry', 'Beef', 'Sheep and goat', 'Pork', 'Other meats', 'Fish and seafood']
    merged_data['Total_meat_consumption'] = merged_data[meat_columns].sum(axis=1, skipna=True)

    return merged_data

# Load the merged data
df = load_data()

# --- Move Filters to Main Page ---
st.markdown("""
### Explore Meat Consumption Trends
Select countries and meat types below to see how consumption and GDP have changed over time.
""")

# Country and Meat Type Selection
col1, col2 = st.columns(2)

with col1:
    countries = df['Entity'].unique()
    selected_countries = st.multiselect("Select Countries:", countries, default=['United States', 'India', 'Germany', 'Nigeria'])

with col2:
    meat_types = ['Poultry', 'Beef', 'Sheep and goat', 'Pork', 'Other meats', 'Fish and seafood']
    selected_meat = st.selectbox("Select Meat Type:", meat_types)

# Filter the Data
filtered_df = df[df['Entity'].isin(selected_countries)]

# --- Visualization: Trend Over Time for Selected Countries ---
st.subheader(f"{selected_meat} Consumption Over Time")

fig = px.line(filtered_df, x='Year', y=selected_meat, color='Entity',
              title=f"{selected_meat} Consumption in Selected Countries (1961-2020)",
              labels={selected_meat: f"{selected_meat} Consumption (kg per capita)"})

st.plotly_chart(fig)

st.markdown(f"""
**Analysis:** The line chart above illustrates how {selected_meat} consumption has evolved in selected countries from 1961 to 2020. Developed countries like the United States and Germany show a consistent increase in {selected_meat} consumption, reflecting economic growth and changing dietary preferences. Conversely, developing countries such as India and Nigeria display slower growth or stable consumption patterns, influenced by cultural factors and economic constraints.
""")

# --- GDP Trend Over Time for Selected Countries ---
st.subheader(f"GDP per Capita Over Time")

gdp_fig = px.line(filtered_df, x='Year', y='GDP_per_capita', color='Entity',
                  title=f"GDP per Capita in Selected Countries (1961-2020)",
                  labels={'GDP_per_capita': 'GDP per Capita (constant 2017 international $)'})

st.plotly_chart(gdp_fig)

st.markdown("""
**Analysis:** This graph shows the growth of GDP per capita in the selected countries. The United States and Germany exhibit steady economic growth over the decades, with a noticeable rise in GDP per capita. In contrast, countries like Nigeria and India have lower GDP per capita values, reflecting their developing status. These economic differences have significant implications for dietary habits and access to various types of meat.
""")

# --- Combined Visualization: GDP vs Total Meat Consumption ---
st.subheader(f"Comparison of GDP per Capita and Total Meat Consumption")

comparison_fig = px.scatter(filtered_df, x='GDP_per_capita', y='Total_meat_consumption', color='Entity',
                            title=f"GDP per Capita vs Total Meat Consumption in Selected Countries",
                            labels={'GDP_per_capita': 'GDP per Capita (constant 2017 international $)',
                                    'Total_meat_consumption': 'Total Meat Consumption (kg per capita)'},
                            trendline='ols')

st.plotly_chart(comparison_fig)

st.markdown("""
**Analysis:** The scatter plot highlights the correlation between GDP per capita and total meat consumption across different countries. A positive correlation is evident, especially in developed countries, where higher GDP per capita aligns with increased meat consumption. However, developing countries show more varied patterns, indicating that factors beyond economic capacity, such as cultural norms and dietary restrictions, also influence meat consumption.
""")

# --- Bar Chart: Meat Consumption Comparison in a Specific Year ---
st.subheader(f"{selected_meat} Consumption Comparison in 2020")

latest_year_df = filtered_df[filtered_df['Year'] == 2020]
bar_fig = px.bar(latest_year_df, x='Entity', y=selected_meat, color='Entity',
                 title=f"{selected_meat} Consumption in Selected Countries (2020)",
                 labels={selected_meat: f"{selected_meat} Consumption (kg per capita)"})

st.plotly_chart(bar_fig)

st.markdown(f"""
**Analysis:** The bar chart compares {selected_meat} consumption in 2020 across selected countries. Developed nations like the United States and Germany show higher consumption levels compared to developing countries like India and Nigeria. This comparison underscores how economic prosperity often translates to greater access to diverse food options, while cultural preferences and affordability continue to shape consumption patterns in developing regions.
""")

# --- Correlation Heatmap ---
st.subheader("Correlation Heatmap of Meat Consumption and GDP")

correlation_columns = ['GDP_per_capita', 'Total_meat_consumption', 'Poultry', 'Beef', 'Sheep and goat', 'Pork', 'Other meats', 'Fish and seafood']
corr_matrix = df[correlation_columns].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', mask=np.triu(np.ones_like(corr_matrix, dtype=bool)))
st.pyplot(plt)

st.markdown("""
**Analysis:** The correlation heatmap illustrates the relationships between GDP per capita and various meat consumption types. Strong positive correlations between GDP and certain meat types (e.g., beef and pork) suggest that higher economic status often correlates with increased consumption of specific meats. Conversely, weaker correlations or negative trends may indicate cultural or regional preferences that deviate from purely economic influences.
""")

# --- Additional Charts ---

# Pork Consumption Comparison Across Countries
st.subheader("Pork Consumption Across Countries (2020)")

pork_fig = px.bar(latest_year_df, x='Entity', y='Pork', color='Entity',
                  title="Pork Consumption in Selected Countries (2020)",
                  labels={'Pork': 'Pork Consumption (kg per capita)'})

st.plotly_chart(pork_fig)

st.markdown("""
**Analysis:** The pork consumption chart reveals interesting cultural differences. Countries like Germany have high pork consumption, reflecting their traditional cuisine, while countries like India and Nigeria show minimal pork consumption due to cultural and religious restrictions.
""")

# Sheep and Goat Consumption Comparison Across Countries
st.subheader("Sheep and Goat Consumption Across Countries (2020)")

sheep_goat_fig = px.bar(latest_year_df, x='Entity', y='Sheep and goat', color='Entity',
                        title="Sheep and Goat Consumption in Selected Countries (2020)",
                        labels={'Sheep and goat': 'Sheep and Goat Consumption (kg per capita)'})

st.plotly_chart(sheep_goat_fig)

st.markdown("""
**Analysis:** Sheep and goat consumption is more prevalent in countries like Nigeria, reflecting traditional dietary preferences, while it remains lower in countries like the United States and Germany. This highlights the influence of local agriculture and food culture on meat consumption patterns.
""")

# Beef Consumption Comparison Across Countries
st.subheader("Beef Consumption Across Countries (2020)")

beef_fig = px.bar(latest_year_df, x='Entity', y='Beef', color='Entity',
                  title="Beef Consumption in Selected Countries (2020)",
                  labels={'Beef': 'Beef Consumption (kg per capita)'})

st.plotly_chart(beef_fig)

st.markdown("""
**Analysis:** The beef consumption chart highlights distinct patterns across countries. The United States shows high beef consumption, aligning with its strong beef industry and cultural preference for beef. In contrast, countries like India have very low beef consumption due to religious practices, while Nigeria and Germany fall somewhere in between, reflecting diverse dietary influences.
""")

# Other Meats Consumption Comparison Across Countries
st.subheader("Other Meats Consumption Across Countries (2020)")

other_meats_fig = px.bar(latest_year_df, x='Entity', y='Other meats', color='Entity',
                         title="Other Meats Consumption in Selected Countries (2020)",
                         labels={'Other meats': 'Other Meats Consumption (kg per capita)'})

st.plotly_chart(other_meats_fig)

st.markdown("""
**Analysis:** The "Other Meats" category encompasses less common meats, and its consumption varies widely depending on regional culinary traditions. Countries like Nigeria might show higher consumption of such meats due to diverse local diets, whereas Western countries may have lower consumption.
""")

# --- Conclusion ---
st.markdown("""
### Conclusion
This project demonstrates that economic growth significantly influences meat consumption patterns, with developed countries exhibiting higher levels of meat consumption compared to developing countries. However, cultural norms, dietary preferences, and religious practices also play crucial roles in shaping these patterns. Understanding these dynamics provides valuable insights into global dietary trends and the impact of economic development on food consumption.
""")