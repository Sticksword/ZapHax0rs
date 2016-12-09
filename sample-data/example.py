import argparse
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def main(movie_review_filename):
    '''Run a sentiment analysis request on text within a passed filename.'''

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('language', 'v1', credentials=credentials)

    with open(movie_review_filename, 'r') as review_file:
        service_request = service.documents().analyzeSentiment(
            body={
                'document': {
                    'type': 'PLAIN_TEXT',
                    'content': review_file.read(),
                }
            }
        )
        response = service_request.execute()

    score = response['documentSentiment']['score']
    magnitude = response['documentSentiment']['magnitude']

    for i, sentence in enumerate(response['sentences']):
        sentence_sentiment = sentence['sentiment']['score']
        print('Sentence {} has a sentiment score of {}'.format(i, sentence_sentiment))

    print('Overall Sentiment: score of {} with magnitude of {}'.format(score, magnitude))
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('movie_review_filename', help='The filename of the movie review you\'d like to analyze.')
    args = parser.parse_args()
    main(args.movie_review_filename)
