import re
from openai import OpenAI
import json
import pandas as pd

client = OpenAI(api_key='')

meTooData = pd.read_csv('data/metooInINSTAGRAM_ME_TOO.csv')

# get the rows in meToo data where the 'HASHTAGS' column contains the word 'metoo' or 'MeToo'
meTooData = meTooData[meTooData['HASHTAGS'].str.contains('metoo', flags=re.IGNORECASE, regex=True)]

# print(meTooData[['DESCRIPTION', 'HASHTAGS']].head())
MODEL = "gpt-3.5-turbo"

def get_sentiment_analysis(text):
    response = client.chat.completions.create(
      model=MODEL,
      messages=[
          {"role": "system", "content": "You are an expert in sentiment analysis. You can ask me to analyze the sentiment of a text. I will provide a categorization of either positive, negative or neutral. The format of my response will be: Sentiment: {positive/negative/neutral}. I will not provide any further details."},
          {"role": "user", "content": "Can you tell me the sentiment of this text: {}".format(text)},
      ],
      temperature=0.5,
    )
    sentiment_json = json.dumps(json.loads(response.model_dump_json()), indent=4)
    sentiment_string = json.loads(sentiment_json)['choices'][0]['message']['content']
    return sentiment_string

def get_sentiment_from_string_response(sentiment):
    sentiment = sentiment.replace('\n', ' ')
    # remove punctuation
    sentiment = re.sub(r'[^\w\s]', '', sentiment)
    return sentiment.split(' ')[1].lower()

# label the data and save as csv
# meTooData = meTooData.iloc[:1]
meTooData = meTooData[['DESCRIPTION', 'HASHTAGS', 'DATE_POSTED', 'COMMENTS_COUNT', 'LIKES_COUNT', 'VIDEO_VIEW_COUNT', 'COMMENT_TEXT']]
print(len(meTooData))
meTooData['SENTIMENT'] = meTooData['DESCRIPTION'].apply(get_sentiment_analysis).apply(get_sentiment_from_string_response)

meTooData.to_csv('data/metooInINSTAGRAM_ME_TOO_labelled_all.csv', index=False)
# print(meTooData[['DESCRIPTION', 'HASHTAGS', 'SENTIMENT']].head())