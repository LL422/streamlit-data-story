import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --- Title and Introduction ---
st.title("The Relationship and the Impact Between Economic Growth and Meat Consumption")

st.markdown("""
### Main Idea
This project explores the relationship between economic growth (measured by GDP per capita) and meat consumption in various countries, focusing on:
- **Developed Countries:** United States & Germany  
- **Developing Countries:** India & Nigeria  

By analyzing these trends, we aim to uncover how economic prosperity influences dietary habits and how cultural, environmental, and economic factors shape meat consumption patterns globally.

---
            
### Why These Countries?
We selected these countries because they represent different economic stagtes and dietary habits:
- **United States & Germany:** High-income countries with strong food industries and high meat consumption. The U.S. leads in beef and poultry, while Germany consumes more pork.
- **India & Nigeria:** Lower-income countries where cultural and economic factors limit meat consumption. India has a large vegetarian population, while Nigeria's meat intake depends on affordability and availability.

---                         

### Why This Matters
As economies grow, diets change. Meat consumption is more than just a food choice—it reflects income levels, cultural traditions, and environmental impacts.

**Economic Impact:**
- Higher GDP means people can afford more meat, often viewed as a sign of wealth and improved nutrition.            

**Cultural Influence:**
- Culture shapes food choices, sometimes limiting meat consumption regardless of income.
- **Example:** In India, many avoid beef due to religious beliefs, even though economic growth allows them to afford it. In contrast, pork is deeply rooted in German cuisine, where it remains a staple in traditional dishes.

**Environmental Concerns:**
- Meat productions requires large amounts of land, water and energy. Some meats, like beef, have a high environmental cost.
- **Example:** In the United States, large-scale beef production contributes to high greenhouse gas emissions. Meanwhile, Nigeria's lower meat consumption has a smaller environmental footprint, but as the economy grows, demand for meat may increase, potentially leading to environmental challenges.             
---

Why We Use These Charts:

- **Line Charts:** Best for showing trends over time, making it easy to see how meat consumption has increased or decreased.

- **Bar Charts:** Useful for comparing meat consumption between countries in a single year.

- **Scatter Plots:** Help visualize the relationship between GDP per capita and meat consumption.

- **Heatmaps:** Show correlations between GDP and different types of meat consumption, helping to highlight patterns across multiple variables.

Each chart type was chosen to make complex data easier to understand and to highlight different aspects of the relationship between economic growth and meat consumption.
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

    # Filter data for the four selected countries
    selected_countries = ['United States', 'Germany', 'India', 'Nigeria']
    merged_data = merged_data[merged_data['Entity'].isin(selected_countries)]

    return merged_data

# Load data
df = load_data()

# --- User Inputs ---
st.title("Explore Meat Consumption Trends")
st.markdown("Select countries and meat types below to see how consumption and GDP have changed over time.")

col1, col2 = st.columns(2)

with col1:
    countries = df["Entity"].unique()
    selected_countries = st.multiselect("Select Countries:", countries, default=["United States", "India", "Germany", "Nigeria"])

with col2:
    meat_types = ["Poultry", "Beef", "Sheep and goat", "Pork", "Other meats", "Fish and seafood"]
    selected_meat = st.selectbox("Select Meat Type:", meat_types)

# Filter Data
filtered_df = df[df["Entity"].isin(selected_countries)]

# --- Visualization ---
st.subheader(f"{selected_meat} Consumption Over Time")

fig = px.line(
    filtered_df, 
    x="Year", 
    y=selected_meat, 
    color="Entity",
    title=f"{selected_meat} Consumption in Selected Countries (1961-2020)",
    labels={selected_meat: f"{selected_meat} Consumption (kg per capita)"}
)

st.plotly_chart(fig)

# --- Dynamic Analysis ---
st.markdown(f"""
### **Analysis Based on Selection**
This chart displays **{selected_meat} consumption per capita (kg per year)** from **1961 to 2020** for the selected countries.

#### **What to Look For:**
- **General Trends:** Are some countries increasing or decreasing their {selected_meat} consumption?
- **Developed vs. Developing:** Do richer countries consume more {selected_meat} than poorer ones?
- **Cultural & Economic Influences:** Some countries may have stable or low consumption due to traditions or affordability.

#### **Key Insights for Your Selection:**
""")

# Generate Insights Based on User Selections
for country in selected_countries:
    country_data = filtered_df[filtered_df["Entity"] == country]

    if country_data[selected_meat].isnull().all():
        st.markdown(f"- **{country}:** No available data for {selected_meat}.")
        continue

    start_value = country_data[selected_meat].iloc[0]
    end_value = country_data[selected_meat].iloc[-1]

    trend = "increased" if end_value > start_value else "decreased"

    st.markdown(f"- **{country}:** {selected_meat} consumption has **{trend}** from **{start_value:.2f} kg per capita** in {country_data['Year'].iloc[0]} to **{end_value:.2f} kg per capita** in {country_data['Year'].iloc[-1]}.")

st.markdown("""
---
**Explore more:** Adjust the selections above to see different patterns across countries and meat types.
""")

# --- GDP Trend Over Time for Selected Countries ---
st.subheader(f"GDP per Capita Over Time")

gdp_fig = px.line(filtered_df, x='Year', y='GDP_per_capita', color='Entity',
                  title=f"GDP per Capita in Selected Countries (1961-2020)",
                  labels={'GDP_per_capita': 'GDP per Capita (constant 2017 international $)'})

st.plotly_chart(gdp_fig)

st.markdown("""
**Analysis:** This graph shows how GDP per capita has grown in the selected countries over the years. The United States and Germany have seen steady economic growth, with a noticeable rise in GDP per capita, reflecting their status as developed nations. In contrast, Nigeria and India, as developing countries, have lower GDP per capita values, although they show signs of gradual improvement. These differences in economic status are important because they can influence what people can afford to eat, including different types of meat.
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
**Analysis:** This scatter plot shows a clear relationship between GDP per capita and total meat consumption. In general, countries with higher GDP per capita, like the United States and Germany, also have higher levels of meat consumption. This suggests that as people have more money, they are more likely to include meat in their diets. However, in countries like India and Nigeria, the relationship isn't as straightforward. Cultural and religious factors, such as dietary restrictions in India, play a big role in shaping meat consumption regardless of economic status.
""")

# --- Bar Chart: Meat Consumption Comparison in a Specific Year ---
st.subheader(f"{selected_meat} Consumption Comparison in 2020")

latest_year_df = filtered_df[filtered_df['Year'] == 2020]
bar_fig = px.bar(latest_year_df, x='Entity', y=selected_meat, color='Entity',
                 title=f"{selected_meat} Consumption in Selected Countries (2020)",
                 labels={selected_meat: f"{selected_meat} Consumption (kg per capita)"})

st.plotly_chart(bar_fig)

st.markdown(f"""
**Analysis:** This bar chart compares {selected_meat} consumption in 2020 across the selected countries. The United States and Germany have higher consumption levels, which aligns with their economic strength and dietary preferences. In contrast, India and Nigeria have much lower consumption levels. This could be due to a combination of economic factors and cultural practices that influence dietary choices.
""")

# --- Correlation Heatmap ---
st.subheader("Correlation Heatmap of Meat Consumption and GDP")

correlation_columns = ['GDP_per_capita', 'Total_meat_consumption', 'Poultry', 'Beef', 'Sheep and goat', 'Pork', 'Other meats', 'Fish and seafood']
corr_matrix = df[correlation_columns].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', mask=np.triu(np.ones_like(corr_matrix, dtype=bool)))
st.pyplot(plt)

st.markdown("""
**Analysis:** The heatmap shows how closely different types of meat consumption are related to GDP per capita. We can see strong positive correlations between GDP and the consumption of certain meats like beef and pork. This means that in wealthier countries, people tend to eat more of these types of meat. However, some types of meat, like fish and seafood, may not be as strongly linked to economic status and could depend more on regional availability or cultural preferences.
""")

# --- Additional Charts ---

# Pork Consumption Comparison Across Countries
st.subheader("Pork Consumption Across Countries (2020)")

pork_fig = px.bar(latest_year_df, x='Entity', y='Pork', color='Entity',
                  title="Pork Consumption in Selected Countries (2020)",
                  labels={'Pork': 'Pork Consumption (kg per capita)'})

st.plotly_chart(pork_fig)

st.markdown("""
**Analysis:** This chart highlights the differences in pork consumption between countries. Germany has high pork consumption, which reflects its traditional cuisine. On the other hand, India and Nigeria show very low pork consumption due to cultural and religious practices that discourage or prohibit eating pork.
""")

# Sheep and Goat Consumption Comparison Across Countries
st.subheader("Sheep and Goat Consumption Across Countries (2020)")

sheep_goat_fig = px.bar(latest_year_df, x='Entity', y='Sheep and goat', color='Entity',
                        title="Sheep and Goat Consumption in Selected Countries (2020)",
                        labels={'Sheep and goat': 'Sheep and Goat Consumption (kg per capita)'})

st.plotly_chart(sheep_goat_fig)

st.markdown("""
**Analysis:** Sheep and goat consumption is more common in countries like Nigeria, where these animals are a traditional part of the diet. In contrast, countries like the United States and Germany consume less of these meats, likely due to different dietary preferences and agricultural practices.
""")

# Beef Consumption Comparison Across Countries
st.subheader("Beef Consumption Across Countries (2020)")

beef_fig = px.bar(latest_year_df, x='Entity', y='Beef', color='Entity',
                  title="Beef Consumption in Selected Countries (2020)",
                  labels={'Beef': 'Beef Consumption (kg per capita)'})

st.plotly_chart(beef_fig)

st.markdown("""
**Analysis:** Beef consumption varies widely between countries. The United States shows high beef consumption, reflecting both its cultural preference and its strong beef industry. In contrast, India's beef consumption is very low due to religious beliefs that discourage eating beef. Nigeria and Germany fall somewhere in between, reflecting a mix of cultural and economic influences.
""")

# Other Meats Consumption Comparison Across Countries
st.subheader("Other Meats Consumption Across Countries (2020)")

other_meats_fig = px.bar(latest_year_df, x='Entity', y='Other meats', color='Entity',
                         title="Other Meats Consumption in Selected Countries (2020)",
                         labels={'Other meats': 'Other Meats Consumption (kg per capita)'})

st.plotly_chart(other_meats_fig)

st.markdown("""
**Analysis:** The "Other Meats" category includes less common types of meat, and their consumption can vary greatly depending on local traditions and availability. Nigeria, for example, might have higher consumption of these meats due to diverse local diets, while countries like the United States and Germany may consume less.
""")

# --- Reflection ---
st.markdown("""
### Reflection on the Process

When I first started this project, I thought the relationship between economic growth and meat consumption would be simple—more money equals more meat. But the deeper I went, the more I realized it’s not that straightforward. I struggled a bit with cleaning and merging the datasets, especially getting the years to match up and making sure the country names were consistent. There were also times when the graphs didn’t look the way I expected, and I had to adjust how I was handling the data.

One thing that surprised me was how much cultural and religious factors affect meat consumption. For instance, India’s low beef consumption has little to do with income levels and more to do with religious beliefs. This made me rethink how I was interpreting the data.

If I had more time, I would probably explore other factors like environmental policies or health trends that might also affect meat consumption. I’d also look into more specific data on different types of meat in more countries.

What I liked best about this project was seeing how data visualization makes complex information easier to understand. Turning raw data into charts and graphs really helped me (and hopefully others) see patterns that aren’t obvious in a spreadsheet.

---
""")

# --- Conclusion ---
st.markdown("""
### Conclusion
This project shows that economic growth plays a big role in influencing meat consumption patterns. Developed countries like the United States and Germany tend to have higher meat consumption due to greater economic prosperity and accessibility.

For example, in India, religious beliefs have a strong influence on meat consumption, leading to lower levels of beef and pork consumption. In contrast, Nigeria shows varying patterns influenced by local traditions and economic conditions.

Overall, while economic growth often leads to higher meat consumption, it's clear that other factors like culture, religion, and regional preferences also shape dietary habits. This highlights the complex relationship between economy and food consumption across different countries.
""")

# --- Citation ---

st.markdown("""
### References

Scibearia. (2024, December 12). Meat consumption per capita. Kaggle. https://www.kaggle.com/datasets/scibearia/meat-consumption-per-capita 

""")
