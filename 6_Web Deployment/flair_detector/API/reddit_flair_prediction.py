import sklearn
import pickle
import praw
import re
from bs4 import BeautifulSoup
import nltk

from nltk.corpus import stopwords

### Variable Declarations and Utility Functions

reddit = praw.Reddit(client_id='#', client_secret='#', user_agent='#', username='#', password='#')
loaded_model = pickle.load(open('Model/finalized_model.sav', 'rb'))

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
   
    text = BeautifulSoup(text, "lxml").text
    text = text.lower()
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub('', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    return text

"""### Detect Reddit India Post Flair"""

def detect_flair(url,loaded_model):

  submission = reddit.submission(url=url)

  data = {}

  data['title'] = submission.title
  data['url'] = submission.url

  submission.comments.replace_more(limit=None)
  comment = ''
  for top_level_comment in submission.comments:
    comment = comment + ' ' + top_level_comment.body
  data["comment"] = comment
  data['title'] = clean_text(data['title'])
  data['comment'] = clean_text(data['comment'])
  data['combine'] = data['title'] + data['comment'] + data['url']
  
  return loaded_model.predict([data['combine']])