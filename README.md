# Sentiment Analysis with Python, Twitter, AlchemyAPI, MongoDB, and Angular

This app will let you query Twitter using Python, send each tweet returned into a Mongo database, and then using another Python script pull records out of MongoDB to populate a table in the UI.

## Install Steps

#### This instruction sets assumes the following:
+ You have installed [MongoDB](http://mongodb.org)
+ You have obtained the correct application authentication keys from [Twitter](https://apps.twitter.com/)
+ You have [Python](https://www.python.org/downloads/) installed
+ You have registered for an [API key](http://www.alchemyapi.com/api/register.html) from Alchemy API.

#### Running the App:

##### Populating the Database
+ Clone the TwitterAngular Repo
+ Run the requirements.txt script with pip to install the python dependencies

``` python
pip install -r requirements.txt
```

+ Run the alchemyapi.py python script with your Alchemy API key as an argument

``` python
python alchemyapi.py <YOUR_ALCHEMY_API_KEY>
```

+ On line 28, change <SEARCH_TERM> to the search term you would like to use.
+ Open tweetSensor.py and replace the variable values on lines 41-44 with your Twitter credentials.

``` python
ts = TwitterSearch(
    consumer_key = '<YOUR_TWITTER_CONSUMER_KEY_HERE>',
    consumer_secret = '<YOUR_TWITTER_CONSUMER_SECRET_HERE>',
    access_token = '<YOUR_TWITTER_ACCESS_TOKEN_HERE>',
    access_token_secret = '<YOUR_TWITTER_ACCESS_TOKEN_SECRET_HERE>'
 )
```

+ Run the tweetSensor.py script and pass your search term as an argument. If your search term includes a hashtag, substitute the # with .

    To search for #mheducation:

``` python
python tweetSensor.py .mheducation
```

+ If no errors appear in the terminal, check your Mongo database and collection to make sure the tweets are there.

##### Querying the results
+ Run the resultService.py script, passing the number of tweets you'd like to have returned and the collection to search as arguments (the same as the search term you used to collect the tweets).

    To retrieve the last 10 tweets from your search for #mheducation:

``` python
python resultService.py <RESULT_COUNT> .mheducation
```

+ This script places a JSON file in /app/js/ which the UI will use.

##### Starting the app
+ Start a web server using Python (or the method of your choice) whose root is the /app folder

``` python
cd app
python -m SimpleHTTPServer
```

+ In your browser open [localhost:8000](http://localhost:8000)
