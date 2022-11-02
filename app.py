import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px

#titles
st.title('Sentiment Analysis')
st.sidebar.title('Sentiment Analysis')

#markdowns
st.markdown('Sentimemnt Analysis of tweets about US Airlines 🐦')
st.sidebar.markdown('Sentimemnt Analysis of tweets about US Airlines 🐦 ')

#filelocation
DATA_URL= "tweets.xlsx"

#readdata
@st.cache(persist =True)
def load_data():
	data = pd.read_excel(DATA_URL)
	data['tweet_created']= pd.to_datetime(data['tweet_created'])

	return data

data = load_data()

#random tweet selection based on sentiment
st.sidebar.subheader('Show Random Tweets')
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'negative', 'neutral'))

st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

#visalization
st.sidebar.markdown("### Number of tweets by sentiments")
select= st.sidebar.selectbox('Visualization',['Histogram','Pi Chart'], key=1)

#newdataframe
sentiment_count= data['airline_sentiment'].value_counts()
sentiment_count=pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})



st.markdown('### Number of tweets by Sentiment')
if select=='Histogram':
	fig=px.bar(sentiment_count, x='Sentiment',y='Tweets',color='Tweets',height=500)
	st.plotly_chart(fig)

else:
	fig=px.pie(sentiment_count, values='Tweets', names='Sentiment')
	st.plotly_chart(fig)


st.sidebar.subheader("when and where are our users twitting from?")
hour=st.sidebar.slider('Hour of day',0,23)
modified_data=data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox('close',True, key=2):
	st.markdown('### Tweets location based on the time of the day')
	
	st.map(modified_data)
