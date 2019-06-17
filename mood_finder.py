# importing the requests library for http requests
import requests

API_ENDPOINT = 'http://text-processing.com/api/sentiment/'

stop = False
while not stop:
    text = input('Enter your feelings...\n')
    payload = {'text': text}
    resp = requests.post(API_ENDPOINT, data=payload)
    response_dict = resp.text
    # print(response_dict)
    if response_dict['label'] == 'pos':
        print('The mood is Positive')
    if response_dict['label'] == 'neg':
        print('The mood is Negative')
    else:
        print("It's complicated")

    c = input('Do you want to continue? (y/n): ')
    if c == 'n':
        stop = True
        print('Quitting judging your feelings...')
        break
    else:
        continue
