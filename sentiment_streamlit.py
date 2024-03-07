import streamlit
import pandas as pd
import re

# import labelled metoo data
meTooData = pd.read_csv('data/metooInINSTAGRAM_ME_TOO_labelled_all.csv')

sentiment_like_counts = meTooData[['SENTIMENT', 'LIKES_COUNT']]

senti_like_counts = sentiment_like_counts.groupby('SENTIMENT').mean()
# print(senti_like_counts)

sentiment_like_counts_with_hashtags = meTooData[['SENTIMENT', 'LIKES_COUNT', 'HASHTAGS']]
# get most common hashtags for each sentiment
# for each row in the dataframe, split the hashtags and get the top 10 most common for each row 
sentiment_like_counts_with_hashtags['common_hashtags'] = sentiment_like_counts_with_hashtags['HASHTAGS'].apply(lambda x: re.findall(r'#\w+', x)).apply(lambda x: pd.Series(x).value_counts().index[:10].tolist())

sentiment_like_counts_with_hashtags = sentiment_like_counts_with_hashtags.explode('common_hashtags')
tag_counts = sentiment_like_counts_with_hashtags.groupby(['SENTIMENT', 'common_hashtags'])['common_hashtags'].count()

def get_top_tags(group, n=10):  # Get top 'n' tags
    return group.nlargest(n)

top_tags_per_sentiment = tag_counts.groupby(level='SENTIMENT').apply(get_top_tags)
negative_tags = []
neutral_tags = []
positive_tags = []
for i in range(30):
    if i < 10:
        negative_tags.append(top_tags_per_sentiment.keys()[i][2])
    elif i < 20:
        neutral_tags.append(top_tags_per_sentiment.keys()[i][2])
    else:
        positive_tags.append(top_tags_per_sentiment.keys()[i][2])
                      
        

print(negative_tags)
print(neutral_tags)
print(positive_tags)

# add a title to the streamlit app
streamlit.title('Sentiment Analysis of #MeToo Posts on Instagram')
streamlit.write('This bar chart shows the average number of likes for posts with different sentiments')

# create a streamlit bar chart with a title and axis labels
streamlit.bar_chart(senti_like_counts)

# get a few example posts 2 negative, 2 positive, 2 neutral
negative = meTooData[meTooData['SENTIMENT'] == 'negative'].iloc[100:102]
positive = meTooData[meTooData['SENTIMENT'] == 'positive'].iloc[100:102]
neutral = meTooData[meTooData['SENTIMENT'] == 'neutral'].iloc[100:102]

streamlit.write('Here are some examples of positive posts')
streamlit.write(positive['DESCRIPTION'])
streamlit.write('Here are the tags associated with positive posts')
streamlit.write(positive_tags)


streamlit.write('Here are some examples of negative posts')
streamlit.write(negative['DESCRIPTION'])
streamlit.write('Here are the tags associated with negative posts')
streamlit.write(negative_tags)


streamlit.write('Here are some examples of neutral posts')
streamlit.write(neutral['DESCRIPTION'])
streamlit.write('Here are the tags associated with neutral posts')
streamlit.write(neutral_tags)

conclusion = 'Based on the data, negative posts have the highest average number of likes, followed by positive posts, and then neutral posts. The posts that are considered "negative" have a tendency to be posts that are recounting negative personal experiences, so the fact that they have the largest number of likes shows that other people emapathise and offer their support.'

streamlit.write(conclusion)