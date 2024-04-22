import requests
from requests_oauthlib import OAuth1Session, OAuth1
from urllib.parse import parse_qs
from zipfile import ZipFile
import os
import json
import time
import sys


def pre_clean():
    if not os.path.exists('likes.json'):
        with ZipFile('archive.zip', 'r') as z:
            with open('likes.json', 'wb') as f:
                f.write(z.read('data/like.js')[23:])

def post_clean(likes, number):
    likes = likes[number:]
    with open('likes.json', 'w') as outfile:
        outfile.write(json.dumps(likes , sort_keys=False, indent=2))

def loadLikes():
    with open('./likes.json', errors="ignore") as f:
        likes = json.load(f)

    return likes

def printLike(like):
    print("Unliking tweet: " + like['like']['expandedUrl'])
    print(like['like']['fullText'])

def auth():

    with open('./keys.json', errors="ignore") as f:
        data = json.load(f)

    auth = data[0]

    consumer_key = auth['consumer_key']
    consumer_secret = auth['consumer_secret']
    bearer_token = auth['bearer_token']
    access_token = auth['access_token']
    access_token_secret = auth['access_token_secret']
    user_id = auth['user_id']

    request_token_url = "https://api.twitter.com/oauth/request_token"

    # oauth = OAuth1Session(consumer_key, client_secret=consumer_secret) # standard v.1.1
    oauth = OAuth1(consumer_key, client_secret=consumer_secret) # API v2

    try:
        # credentials = oauth.fetch_request_token(request_token_url) # standard v.1.1
        r = requests.post(url=request_token_url, auth=oauth) # API v2
        credentials = parse_qs(r.content)

    except ValueError:
        print(
            "There may have been an issue with your consumer_key or consumer_secret."
        )
    # resource_owner_key = credentials.get('oauth_token')[0] # v1.1
    # resource_owner_secret = credentials.get('oauth_token_secret')[0] # v1.1
    resource_owner_key = credentials.get('oauth_token') # token and secret must be bytes literal in v2 (b'oauth_token')
    resource_owner_secret = credentials.get('oauth_token_secret')
    print(f"OAuth success! (token {resource_owner_key})")


    # oauth = OAuth1Session(
    #     consumer_key,
    #     client_secret=consumer_secret,
    #     resource_owner_key=access_token,
    #     resource_owner_secret=access_token_secret,
    # ) # standard v1.1

    oauth = OAuth1(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    ) # API v2

    return oauth, user_id, bearer_token

def removeLike(tweet_id, oauth, user_id, bearer_token):

    try:
        # response = oauth.post("https://api.twitter.com/1.1/favorites/destroy.json?id="+tweet_id) # standard v1.1
        response = requests.delete(url=f'https://api.twitter.com/2/users/{user_id}/likes/{tweet_id}', headers={'Authorization': f'Bearer {bearer_token}'}, auth=oauth) # unliking in API v2 uses the delete method but it does not exist in OAuth1Session. Use OAuth1 helper instead.

    except response.status_code != 200:
        raise Exception(
            f"Request returned an error: {response.status_code} {response.text}"
        )

    return response


def removeLikes(likes, number_to_remove, oauth, user_id, bearer_token):

    count = 0
    for like in likes:

        printLike(like)

        code = removeLike(like['like']['tweetId'], oauth, user_id, bearer_token)

        extra = ''
        if code.status_code == 403 or code.status_code == 401:
            try:
                extra = '(' + json.loads(code.text)['errors'][0]['message'] + ')'
            except:
                extra = '(' + json.loads(code.text)['detail'] + ')'
        elif code.status_code == 404:
            extra = " Already deleted"
        elif code.status_code == 405:
            extra = " Method not allowed"

        print(f"Response code: {code.status_code} {extra}")
        print('______________________________________________________________ \n')

        count = count + 1
        if(count > number_to_remove):
            break
        time.sleep(18)

def main():
    pre_clean()
    number_to_remove = int(sys.argv[1])
    oauth, user_id, bearer_token = auth()
    likes = loadLikes()
    removeLikes(likes, number_to_remove, oauth, user_id, bearer_token)
    post_clean(likes, number_to_remove)


if __name__ == '__main__':
    main()
