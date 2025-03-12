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

### Why We Use These Charts:

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
**Explore more:** Adjust the selections above to see different patterns across countries and meat types.
""")

# --- GDP Trend Over Time for Selected Countries ---
st.subheader(f"GDP per Capita Over Time")

st.markdown("""
This line chart tracks how GDP per capita (a measure of economic wealth per person) has changed over time in the selected countries. Each line represents a country, helping to compare their economic growth.
""")

gdp_fig = px.line(filtered_df, x='Year', y='GDP_per_capita', color='Entity',
                  title=f"GDP per Capita in Selected Countries (1961-2020)",
                  labels={'GDP_per_capita': 'GDP per Capita (constant 2017 international $)'})

st.plotly_chart(gdp_fig)

st.markdown("""
**Analysis:**

- **United States & Germany:** These countries have consistently high GDP per capita, indicating economic stability and steady growth.

- **India & Nigeria:** These nations show lower GDP per capita, though both have seen gradual increases over time. Economic constraints in these countries often affect people's ability to afford meat in their diets.

- **Key takeaway:** Higher GDP generally means better food security and more diverse diets, while lower GDP can limit access to certain foods, including meat.
""")

# --- Combined Visualization: GDP vs Total Meat Consumption ---
st.subheader(f"Comparison of GDP per Capita and Total Meat Consumption")

st.markdown("""
This scatter plot helps us understand if there’s a connection between a country’s economic strength (GDP per capita) and how much meat its people consume. Each dot represents a country in a specific year, showing whether wealthier nations eat more meat.
            """)

comparison_fig = px.scatter(filtered_df, x='GDP_per_capita', y='Total_meat_consumption', color='Entity',
                            title=f"GDP per Capita vs Total Meat Consumption in Selected Countries",
                            labels={'GDP_per_capita': 'GDP per Capita (constant 2017 international $)',
                                    'Total_meat_consumption': 'Total Meat Consumption (kg per capita)'},
                            trendline='ols')

st.plotly_chart(comparison_fig)

st.markdown("""
**What This Chart Tells Us:**

- **United States & Germany:** These countries have high GDP per capita, meaning people earn more money on average. This allows them to afford more meat, making it a regular part of their diet.

- **India & Nigeria:** These countries have lower GDP per capita, meaning less money is available for food. Meat is more expensive, so people eat less of it. However, in India, religious and cultural beliefs also limit meat consumption, even for wealthier individuals.

**Why This Matters:**

- Economic growth allows for greater access to meat, but affordability isn’t the only factor—cultural and religious beliefs still shape what people eat.

- Higher GDP generally leads to higher meat consumption, but this trend isn’t universal. India is a clear example where cultural preferences override economic factors.
---
            """)

# --- Bar Chart: Meat Consumption Comparison in a Specific Year ---
st.subheader(f"Poultry Consumption Comparison in 2020")
st.markdown("""This bar chart shows how much poultry people in each country ate per person in 2020. The taller the bar, the more poultry people consumed on average.""")
latest_year_df = filtered_df[filtered_df['Year'] == 2020]
bar_fig = px.bar(latest_year_df, x='Entity', y='Poultry', color='Entity',
                 title=f"Poultry Consumption in Selected Countries (2020)",
                 labels={'Poultry': 'Poultry Consumption (kg per capita)'})

st.plotly_chart(bar_fig)

st.markdown(f"""
**What This Chart Tells Us:**

- **United States & Germany:** People in these countries eat a lot of poultry. This is because poultry is affordable, widely available, and a common part of their diets. In the U.S., fast food and processed poultry products also contribute to higher consumption.

- **India & Nigeria:** People in these countries eat much less poultry. In India, religious and cultural beliefs influence meat consumption, and many people follow vegetarian diets. In Nigeria, lower incomes and limited access to poultry make it harder for people to afford and eat as much chicken.

**Why This Matters:**

- Countries with more money generally have easier access to poultry, making it a bigger part of their diet.

- Cultural traditions and food preferences still play a big role—just because a country can afford more meat doesn’t always mean people will eat it.
""")

# --- Correlation Heatmap ---
st.subheader("Correlation Heatmap of Meat Consumption and GDP")
st.markdown("""This heatmap shows how different types of meat consumption are related to GDP per capita. Darker colors indicate a stronger connection between GDP and meat consumption.""")
correlation_columns = ['GDP_per_capita', 'Total_meat_consumption', 'Poultry', 'Beef', 'Sheep and goat', 'Pork', 'Other meats', 'Fish and seafood']
corr_matrix = df[correlation_columns].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', mask=np.triu(np.ones_like(corr_matrix, dtype=bool)))
st.pyplot(plt)

st.markdown("""
**What This Chart Tells Us:**

- **Beef and Pork:** These meats show a strong link to GDP. This means that wealthier countries tend to eat more beef and pork, likely due to better affordability and dietary preferences.

- **Fish and Seafood:** The connection between GDP and fish consumption is weaker. This suggests that fish consumption depends more on availability and cultural habits rather than just economic status.

**Why This Matters:**

- Countries with higher GDP usually have higher meat consumption, but the type of meat varies based on cultural preferences and regional availability.

- Understanding these patterns helps explain why economic growth doesn’t always lead to the same dietary changes in every country.

""")

# --- Additional Charts ---

# Pork Consumption Comparison Across Countries
st.subheader("Pork Consumption Across Countries (2020)")
st.markdown("""This bar chart compares pork consumption per person across different countries in 2020.""")
pork_fig = px.bar(latest_year_df, x='Entity', y='Pork', color='Entity',
                  title="Pork Consumption in Selected Countries (2020)",
                  labels={'Pork': 'Pork Consumption (kg per capita)'})

st.plotly_chart(pork_fig)
st.markdown("""
**What This Chart Tells Us:**

- **Germany:** Pork is a major part of German cuisine, which is why consumption is much higher compared to the other countries.

- **United States:** Pork consumption is significant but lower than Germany, as poultry and beef are more popular in American diets.

- **India & Nigeria:** Pork consumption is extremely low in both countries. In India, religious beliefs—particularly among Hindus and Muslims—strongly discourage pork consumption. In Nigeria, pork is not widely eaten due to both religious restrictions and lower availability.

**Why This Matters:**

- Economic growth does not always mean higher pork consumption—cultural and religious influences play a big role.

- In some countries, even if people can afford more meat, they may avoid pork due to religious reasons, making diet trends more complex than just income levels.
""")


# Sheep and Goat Consumption Comparison Across Countries
st.subheader("Sheep and Goat Consumption Across Countries (2020)")
st.markdown("""This bar chart compares how much sheep and goat meat people ate per person in different countries in 2020.""")

sheep_goat_fig = px.bar(latest_year_df, x='Entity', y='Sheep and goat', color='Entity',
                        title="Sheep and Goat Consumption in Selected Countries (2020)",
                        labels={'Sheep and goat': 'Sheep and Goat Consumption (kg per capita)'})

st.plotly_chart(sheep_goat_fig)

st.markdown("""
**What This Chart Tells Us:**

- **Nigeria:** Sheep and goat meat are a traditional part of Nigerian diets, which is why consumption is higher compared to other countries.

- **India:** Although India has lower overall meat consumption, sheep and goat meat are commonly eaten in some regions, particularly among communities that do not consume beef or pork.

- **United States & Germany:** These countries consume much less sheep and goat meat, as their diets mainly focus on beef, poultry, and pork. These meats are not as commonly farmed or eaten in large quantities.

**Why This Matters:**

- Some meats are more commonly eaten in certain parts of the world due to tradition rather than economic status.

- Availability also plays a role—countries that raise more sheep and goats tend to eat them more frequently.

- While GDP affects meat consumption, cultural preferences strongly determine which types of meat are most popular.
""")

# Beef Consumption Comparison Across Countries
st.subheader("Beef Consumption Across Countries (2020)")
st.markdown("""This bar chart compares beef consumption per person across different countries in 2020.""")
beef_fig = px.bar(latest_year_df, x='Entity', y='Beef', color='Entity',
                  title="Beef Consumption in Selected Countries (2020)",
                  labels={'Beef': 'Beef Consumption (kg per capita)'})

st.plotly_chart(beef_fig)

st.markdown("""
**What This Chart Tells Us:**

- **United States:** Beef consumption is high due to strong cultural demand, a well-developed beef industry, and affordability. Steak, burgers, and processed beef products are common in American diets.

- **Germany:** Beef consumption is lower than in the U.S. but still significant. Germany’s diet includes more pork, which reduces the reliance on beef.

- **India:** Beef consumption is very low, primarily due to religious beliefs. Hinduism, which is followed by the majority of Indians, discourages or prohibits beef consumption.

- **Nigeria:** Beef consumption is moderate but lower than in the U.S. and Germany. Economic factors and availability influence how much beef is eaten in Nigeria.

**Why This Matters:**

- Economic strength allows greater access to beef, but cultural and religious beliefs strongly influence consumption levels.

- While higher GDP countries tend to eat more beef, India is an exception where cultural traditions limit consumption despite economic growth.
""")

# Other Meats Consumption Comparison Across Countries
st.subheader("Other Meats Consumption Across Countries (2020)")

other_meats_fig = px.bar(latest_year_df, x='Entity', y='Other meats', color='Entity',
                         title="Other Meats Consumption in Selected Countries (2020)",
                         labels={'Other meats': 'Other Meats Consumption (kg per capita)'})

st.plotly_chart(other_meats_fig)

st.markdown("""
**What This Chart Tells Us:**

- **Nigeria:** Higher consumption of other meats is likely due to a diverse local diet that includes bushmeat, game, and other regionally available meats.

- **United States & Germany:** Consumption of other meats is lower since poultry, beef, and pork dominate their diets. Some alternative meats, like venison or bison, are eaten but not widely consumed.

- **India:** Due to cultural and religious dietary restrictions, consumption of alternative meats remains low, with a preference for plant-based proteins.

**Why This Matters:**

- Meat consumption isn’t just about economic status—local food traditions and availability shape what people eat.

- Countries with access to a variety of wildlife or game meat tend to have more diverse meat consumption patterns.""")

st.markdown("""
---

### Failed Attempts and Changes

At first, we considered using only static charts, but they didn’t allow for exploring different country and meat type combinations. Adding interactivity made it possible to see multiple perspectives in one place.

We also tried using only line charts, but they didn’t effectively show country comparisons at a single point in time, which is why bar charts were included. Additionally, scatter plots were added to better illustrate the link between GDP and meat consumption, which was unclear in other formats. Finally, heatmaps were introduced to visualize overall correlations more effectively.

If we were to improve this further, we might add more filtering options or deeper breakdowns by region and income level to give a broader global perspective.

            """)

st.markdown("""
---

Why These Visualizations Were Chosen

We used different types of charts to make the data easier to understand. Line charts help show trends over time, bar charts compare countries in a specific year, scatter plots highlight relationships between variables, and heatmaps reveal correlations. Each visualization was selected to highlight key insights about how economic growth and cultural factors influence meat consumption.

---
""")

st.markdown("""
---

Ethical Considerations

This project focuses on economic trends and food consumption patterns. However, it’s important to acknowledge ethical concerns like food security, sustainability, and cultural sensitivity. Meat production has environmental impacts, and economic inequalities affect access to food. These factors should be considered when interpreting the data.
---
""")

# --- Reflection ---
st.markdown("""
---
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
            
Jiao, Hongxia. “An Overview of Meat Consumption in the United States.” Farmdoc Daily, 12 May 2021, farmdocdaily.illinois.edu/2021/05/an-overview-of-meat-consumption-in-the-united-states.html. 
            
“The Meat Industry – Environmental Issues & Solutions.” Clean Water Action, cleanwater.org/meat-industry-environmental-issues-solutions. Accessed 12 Mar. 2025. 

González, Neus, et al. “Meat Consumption: Which Are the Current Global Risks? A Review of Recent (2010-2020) Evidences.” Food Research International (Ottawa, Ont.), U.S. National Library of Medicine, Nov. 2020, pmc.ncbi.nlm.nih.gov/articles/PMC7256495/. 

""")
