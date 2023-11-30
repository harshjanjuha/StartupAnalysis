import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='StartUp Analysis')

df = pd.read_csv('cleaned_startup_data.csv')


def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount'].sum())
    # max funding
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # average funding
    average_funding = round(df.groupby('startup')['amount'].sum().mean())
    # total funded startups
    num_startups = df['startup'].nunique()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + 'Cr')
    with col2:
        st.metric('Max', str(max_funding) + 'Cr')
    with col3:
        st.metric('Average', str(average_funding) + 'Cr')
    with col4:
        st.metric('Funded Startups', str(num_startups))

    # month on month chart
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    st.header('Month on Month Graph')
    selected_opt = st.selectbox('Select Type', ['Total Amount', 'Count'])
    if selected_opt == 'Total Amount':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x-axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig, ax = plt.subplots()
    ax.plot(temp_df['x-axis'], temp_df['amount'])
    st.pyplot(fig)


def load_investor_details(investor):
    st.title(investor)
    # Load the recent 5 investments of the investor
    investments = df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']].reset_index().drop('index', axis=1)
    st.subheader('Most Recent Investments')
    st.dataframe(investments)
    col1, col2 = st.columns(2)
    with col1:
        # biggest investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)
    with col2:
        # Most invested sector
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('Most Invested Sectors')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series.values, labels=vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)
    with col1:
        # Stage
        stage_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Stage')
        fig2, ax2 = plt.subplots()
        ax2.pie(stage_series.values, labels=stage_series.index, autopct="%0.01f%%")
        st.pyplot(fig2)
    with col2:
        stage_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('City')
        fig3, ax3 = plt.subplots()
        ax3.pie(stage_series.values, labels=stage_series.index, autopct="%0.01f%%")
        st.pyplot(fig3)
    with col1:
        # year-on-year investment graph
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('Year on Year Investment')
        fig4, ax4 = plt.subplots()
        ax4.plot(year_series.index, year_series.values)
        st.pyplot(fig4)
        ## Find similar investor which invest closest to selected investor


st.sidebar.title('Startup Funding analysis')
option = st.sidebar.selectbox('Select One', ['Overall', 'StartUp', 'Investor'])

if option == 'Overall':
    st.title('Overall Analysis')
    # btn0 = st.sidebar.button('Show Overall Analysis')
    # if btn0:
    load_overall_analysis()

elif option == 'StartUp':
    st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('StartUp Analysis')

if option == 'Investor':
    st.title('Investor Analysis')
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find investor details')
    if btn2:
        load_investor_details(selected_investor)
