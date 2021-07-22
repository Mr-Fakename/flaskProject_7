from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def parse(req):
    return [word for word in word_tokenize(req) if word not in stopwords.words('english')]
