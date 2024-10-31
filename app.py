import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('vehicles_us.csv')


st.markdown("<h1 style='text-align: center;'>EDA Car Advertisement</h1>", unsafe_allow_html=True)
st.markdown('##### The purpose of this project is to use Exploratory Data Analysis (EDA) to better understand the driving factors behind vehicle pricing and how it interrelates to the rate at which vehicles sell.  The value gained from these relationships should help us to better maximize pricing without maintaining excess inventory. ')

#upload = st.file_uploader('Upload file here')
#st.write(df.info())
#Clean data
df['date_posted'] = pd.to_datetime(df['date_posted'])
df['model_year'] = df['model_year'].fillna(9999).astype(int)
df['odometer'] = df['odometer'].fillna(999999).astype(int)
df['paint_color'] = df['paint_color'].astype('str', errors='ignore')
#drop unessary columns and rows
df = df.drop(['cylinders', 'fuel', 'transmission', 'is_4wd'], axis=1)
df = df.drop_duplicates()
# drop duplicate values
df['type'] = df['type'].replace({'pickup': 'truck'})
df['type'] = df['type'].replace({'offroad': 'SUV'})

df_clean =df.astype(str)

#st.write(df_clean.head())
#st.markdown('Above we see a sample of the data we obtained from the vehicles_us.csv file')
st.markdown("<h1 style='text-align: center;'>Vehicle Pricing</h1>", unsafe_allow_html=True)

#average price by vehicle type
avg_type = df.groupby('type')['price'].mean().reset_index()
avg_type = avg_type.sort_values(by='price', ascending=True)

# average price by model year
avg_year = df.groupby('model_year')['price'].mean().reset_index()

# removed extreme values for year to prevent data being skewed
avg_year = avg_year[(avg_year['model_year'] <= 2020) & (avg_year['model_year'] >= 1995)]

# average price by condition 
avg_condition = df.groupby('condition')['price'].mean().reset_index()
avg_condition = avg_condition.sort_values(by='price', ascending=True)
# Create bar charts
fig1 = px.bar(avg_type, x='type', y='price', title='Average Price by Vehicle Type',  color_discrete_sequence=['#33ccff'], labels={'type': 'Vehicle Type', 'price': 'Average Price'})
fig1.update_traces(marker_line_color='black', marker_line_width=1.5)

fig2 = px.bar(avg_year, x='model_year', y='price', title='Average Price by Model Year',  color_discrete_sequence=['#8585e0'], labels={'model_year': 'Model Year', 'price': 'Average Price'})
fig2.update_traces(marker_line_color='black', marker_line_width=1.5)

fig3 = px.bar(avg_condition, x='condition', y='price', title='Average Price by Condition',  color_discrete_sequence=['#b300b3'], labels={'model_year': 'Model Year', 'price': 'Average Price'})
fig3.update_traces(marker_line_color='black', marker_line_width=1.5)


st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(fig3)


st.markdown('##### From the charts above we see three of the biggest factors which influence pricing: Type, Model Year, and Condition')
st.markdown("<h1 style='text-align: center;'>Average Days To Sell</h1>", unsafe_allow_html=True)

# average days listed by type
avg_days_listed_type = df.groupby('type')['days_listed'].mean().reset_index()
avg_days_listed_type = avg_days_listed_type[avg_days_listed_type['type'] != 'other']
# average days listed by model year
avg_year_days = df.groupby('model_year')['days_listed'].mean().reset_index()
avg_year_days = avg_year_days.sort_values(by='days_listed', ascending=False)
avg_days_listed_year = avg_year_days.groupby('model_year')['days_listed'].mean().reset_index()
avg_days_listed_year = avg_days_listed_year[(avg_days_listed_year['model_year'] <= 2020) & (avg_days_listed_year['model_year'] >= 1995)]

# average days listed by color
avg_days_listed_color = df.groupby('paint_color')['days_listed'].mean().reset_index()

# average days listed by condition
avg_days_listed_condition = df.groupby('condition')['days_listed'].mean().reset_index()

# create scatter plots
# create scatter plots
fig4 = px.scatter(avg_days_listed_type, x='type', y='days_listed', title='Average Days Listed by Vehicle Type', labels={'days_listed': 'Days Listed', 'type': 'Vehicle Type'})
fig4.update_traces(marker=dict(size=30, color='#33ccff'))
fig4.update_traces(marker_line_color='black', marker_line_width=2.5)

fig5 = px.scatter(avg_days_listed_year, x='model_year', y='days_listed', title='Average Days Listed by Model Year', labels={'days_listed': 'Days Listed', 'model_year': 'Model Year'})
fig5.update_traces(marker=dict(size=30, color='#8585e0'))
fig5.update_traces(marker_line_color='black', marker_line_width=2.5)

fig6 = px.scatter(avg_days_listed_color, x='paint_color', y='days_listed', title='Average Days Listed by Paint Color', labels={'days_listed': 'Days Listed', 'paint_color': 'Paint Color'})
fig6.update_traces(marker=dict(size=30, color='#ff0066', line=dict(color='black', width=2.5)))

# Create scatter plot for average days listed by condition
fig7 = px.scatter(avg_days_listed_condition, x='condition', y='days_listed', title='Average Days Listed by Condition', labels={'days_listed': 'Days Listed', 'condition': 'Vehicle Condition'})
fig7.update_traces(marker=dict(size=30, color= '#b300b3', line=dict(color='black', width=2.5)))

st.plotly_chart(fig7)
st.plotly_chart(fig6)
st.plotly_chart(fig4)
st.plotly_chart(fig5)

st.markdown('##### There are several variables that influence how long it can take for a vehicle to sell.  The condition (especially new), type and color all contribute to whether a vehicle sells a few days before or after the average.')

st.markdown("<h1 style='text-align: center;'>Distribution of Sales</h1>", unsafe_allow_html=True)

 # Filter average days listed by prices, for vehicles less than 60 days
avg_days_listed_price = df.groupby('price')['days_listed'].mean().reset_index()
avg_days_listed_price = avg_days_listed_price[avg_days_listed_price['days_listed'] <= 60]

# distribution of vehicles price more than 20,000 by days, and less 60 days
avg_days_listed_price_above_20000 = avg_days_listed_price[avg_days_listed_price['price'] >= 20000]

# distribution of vehicles price less than 20,000 by days, and less 60 days
avg_days_listed_price_below_20000 = avg_days_listed_price[avg_days_listed_price['price'] < 20000]

# create histograms
fig8 = px.histogram(avg_days_listed_price_above_20000, x='days_listed', nbins=30, title='Average Days Vehicles Listed Above 20,000 Dollars', labels={'days_listed': 'Average Days Listed'}, color_discrete_sequence=['#00ff99'])

fig8.update_traces(marker_line_color='black', marker_line_width=1.5)
fig8.update_yaxes(range=[0, 160])

fig9 = px.histogram(avg_days_listed_price_below_20000, x='days_listed', nbins=30, title='Average Days Vehicles Listed Below 20,000 Dollars', labels={'days_listed': 'Average Days Listed'}, color_discrete_sequence=['#00e64d'])

fig9.update_traces(marker_line_color='black', marker_line_width=1.5)
fig9.update_yaxes(range=[0, 160])   

if st.checkbox('Show Average Days Vehicles Listed Above 20,000 Dollars'):
    st.plotly_chart(fig8)

if st.checkbox('Show Average Days Vehicles Listed Below 20,000 Dollars'):
    st.plotly_chart(fig9)


# stats on histogram
average_below = avg_days_listed_price_below_20000['days_listed'].mean()
average_below = round(average_below, 1)
#print("Average Days Listed for vehicles priced below 20,000:", average_below)

average_above = avg_days_listed_price_above_20000['days_listed'].mean()
average_above = round(average_above, 1)
#print("Average Days Listed for vehicles priced above 20,000:", average_above)
#print()
sd_below = avg_days_listed_price_below_20000['days_listed'].std()
sd_below = round(sd_below, 1)
#print("Standard Deviation for vehicles priced below 20,000:", sd_below)

sd_above = avg_days_listed_price_above_20000['days_listed'].mean()
sd_above = round(sd_above, 1)
st.write("")
st.write(f"Average Days Listed for vehicles priced above 20,000: {average_above}")
st.write(f"Average Days Listed for vehicles priced below 20,000: {average_below}")
st.write("")
st.markdown(f"Standard Deviation for vehicles priced above 20,000: **{sd_above}**")
st.markdown(f"Standard Deviation for vehicles priced below 20,000: **{sd_below}**")


st.markdown('##### On average we see vehicles which cost more or less than 20,000 dollars take about 33 days to sell.  However when we look at the distribution of these sales, the more expensive cars sell more gradually and the cars below 20,000 do not really start selling until after about 30 day.')

st.markdown('### Looking at the above information we can start to understand the variables that drive sales.  Certain new vehicles like Trucks and Convertibles tend to sell themselves, where used vans, wagons, and buses take more time to sell.')
st.markdown('### **The largest change in a trend we see is sales of cars below 20,000 dollars, before and after the 30 days mark.  We can infer that the prices of these vehicles might drop after 30 days which leads to the spike we see in sales.  If pricing of these vehicles is moderated sooner it could help sell these vehicle faster and at a higher price, which would save in costs to maintain them while maximizing profits.** ')


url = "https://github.com/Tom-Kinstle/sprint_4/tree/main"
st.write("GetHub [link](%s)" % url)
#st.markdown("check out this [link](%s)" % url)