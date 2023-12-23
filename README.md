# Nuke all tweets

An automated command line tool to delete tweets.

## Requirements

- Python 3.8+

## Instructions

1. Get a Twitter Developer Account and save your credentials. Save the following values and add them to key.json.

   - consumer_key
   - consumer_secret
   - access_token
   - access_token_secret
   - user_id (this value is not present in your developer dashboard but instead can be obtained from your archive)

2. Rename your zipped archive to `archive.zip` and put it in root of the project. Don't unzip the file.

3. Install required dependencies. \
   `pip install -r requirements.txt`

4. Delete tweets! _(note: deleting too many at once may trigger Twitter for suspicious activity. Around 3000 should be safe.)_ \
   `python ./TweetEraser.py <#-of-tweets-to-delete>`

5. You can also remove your likes too.
   `python ./LikeRemover.py <#-of-likes-to-remove>`
