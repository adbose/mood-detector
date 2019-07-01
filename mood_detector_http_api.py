# importing the requests library for http requests
import requests, json

API_ENDPOINT = 'http://text-processing.com/api/sentiment/'

stop = False
while not stop:
    text = input('Enter your feelings...\n')
    payload = {'text': text}
    resp = requests.post(API_ENDPOINT, data=payload)
    print('Type of the response: ', type(resp))
    response_text = resp.text
    print(response_text)  # this is a JSON string, not a dictionary
    print('Type of the response: ', type(response_text))
    response_dict = json.loads(response_text)
    print('Type of the response: ', type(response_dict))

    if response_dict['label'] == 'pos':
        print('The mood is Positive')
    elif response_dict['label'] == 'neg':
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
