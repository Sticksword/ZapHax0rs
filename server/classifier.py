import nltk
import pandas as pd
import numpy as np
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk import word_tokenize
import string
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.externals import joblib
import pickle

# pd.options.display.max_colwidth = 150
#
# a = pd.read_csv("/Users/tfeng/Development/DataScience/Hackathon/NPS-Classified-Comments.csv", encoding="ISO-8859-1",
#                 nrows=747)
# categories = ['Usability', 'Vague', 'Data', 'Photos', 'Agent Related', 'Bugs', 'Suggested Features',
#               'Undiscovered Features', 'Performance/site speed']
# df = a[['COMMENTS', 'Usability', 'Vague', 'Data', 'Photos', 'Agent Related', 'Bugs', 'Suggested Features',
#         'Undiscovered Features', 'Performance/site speed']]
#
# testset = pd.read_csv('/Users/tfeng/Development/DataScience/Hackathon/December-Raw-NPS-Data.csv', encoding="ISO-8859-1")
# testset.COMMENTS.fillna('', inplace=True)
#
# categories = ['Photos']
# df.COMMENTS.fillna('', inplace=True)
# df = df.loc[df.COMMENTS != ''].reset_index()  # remove all things without comments.


class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


class Model:
    exclude = set(string.punctuation)

    def remove_punctuations(word):
        filtered = ''.join(ch for ch in word if ch not in Model.exclude)
        return filtered

    def __init__(self, df, category):
        self.category = category
        print(df[category].sum())
        self.cv = CountVectorizer(tokenizer=LemmaTokenizer(), stop_words="english")
        self.cv.ngram_range = (1, 1)
        self.tfidf_transformer = TfidfTransformer()
        self.tf_transformer = TfidfTransformer(use_idf=True)

        self.Y = df[category].fillna(0).astype(np.int)
        self.X = df['COMMENTS'].apply(Model.remove_punctuations).astype('str')
        self.X_train_counts = self.cv.fit_transform(self.X)
        self.X_train_tfidf = self.tfidf_transformer.fit_transform(self.X_train_counts)
        # print(self.cv.vocabulary_)

    def transform_to_featureset(self, data):
        X = data.fillna('').astype('str')
        X_counts = self.cv.transform(X)
        X_tfidf = self.tfidf_transformer.transform(X_counts)
        return X_counts, X_tfidf

    def train_classifier(self, X_train, Y_train):
        print(self.category)

        ada = AdaBoostClassifier()
        sss = StratifiedShuffleSplit(n_splits=1, test_size=.25, random_state=4)
        sss.get_n_splits(X_train)
        for train_indices, test_indices in sss.split(X_train, Y_train):
            # partition the data
            X_train_partition, X_test_partition = X_train[train_indices], X_train[test_indices]
            Y_train_partition, Y_test_partition = Y_train[train_indices], Y_train[test_indices]
            tuned_parameters = [{'base_estimator': [DecisionTreeClassifier(max_depth=1),
                                                    DecisionTreeClassifier(max_depth=2),
                                                    DecisionTreeClassifier(max_depth=3)],
                                 'learning_rate': [.8, .9, 1, 1.1, 1.3, 1.4, 1.5, 1.6],
                                 'n_estimators': [80, 90, 100, 110, 120, 125, 130, 135, 140, 150, 160]}]
            clf = GridSearchCV(ada, tuned_parameters, cv=5, scoring='roc_auc')
            clf.fit(X_train_partition, Y_train_partition)
            print("Best parameters set found on development set:")
            print(clf)
            print(clf.best_params_)

            c = AdaBoostClassifier(learning_rate=clf.best_params_['learning_rate'],
                                   n_estimators=clf.best_params_['n_estimators'])
            classifier = c.fit(X_train_partition, Y_train_partition)
            y_hat = classifier.predict(X_test_partition).astype(np.float).astype(np.int)
            fpr, tpr, thresholds = roc_curve(Y_test_partition, y_hat)
            print(tpr)
            print(fpr)
            print(thresholds)
            auc_score = roc_auc_score(Y_test_partition, y_hat)
            # trscore = c.score(X_train_partition,Y_train_partition)
            tescore = c.score(X_test_partition, Y_test_partition)
            print("AUC ROC: ", auc_score)
            print("Accuracy: ", tescore)

            self.model = c.fit(X_train, Y_train)

    def predict(self, df):
        X_counts, X_tfidf = self.transform_to_featureset(df['COMMENTS'])
        Y_hat = self.model.predict(X_tfidf)
        return pd.concat([df['COMMENTS'], pd.DataFrame(Y_hat, columns=[self.category])], axis=1)

    def save_model(self, filename):
        output = open(filename, 'wb')
        pickle.dump(self, output)
        output.close()

    @staticmethod
    def load_model(filename):
        pkl_file = open(filename, 'rb')
        model = pickle.load(pkl_file)
        pkl_file.close()
        return model


# def classify_comments(csv):
#     m = Model.load_model("/Users/michen/Python-Projects/ZapHax0rs/server/model3.pkl")
#     df = pd.read_csv(csv, encoding="ISO-8859-1")
#     df.COMMENTS.fillna('', inplace=True)
#     results = m.predict(df)
#     return results.to_json()

def classify_comments(comment):
    m = Model.load_model("/Users/michen/Python-Projects/ZapHax0rs/server/model3.pkl")
    df = pd.DataFrame(data= {"COMMENTS":[comment]})
    df.COMMENTS.fillna('', inplace=True)
    results = m.predict(df)
    return results.to_json()


# model = Model(df, 'Photos')
# model.train_classifier(model.X_train_tfidf, model.Y)
# results = model.predict(testset)
# print(results['Photos'].astype(np.float).sum())
# model.save_model("model.pkl")
# results

# classify_comments('/Users/tfeng/Development/DataScience/Hackathon/test.csv')
