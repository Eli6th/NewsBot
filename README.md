# NewsBot

Before using pip install:
pip install requests 
pip install beautiful soup 4
pip install smtplib
pip install redis 
pip install time
pip install nytimesarticle
pip install GoogleNews

Automatically sends you an email from newsycombinator, google news, and the new york times at 7 am (time can be adjusted), using the keywords inputted by the user. I would 
recommend turning off the New York Times email, unless you would like to sign up for their free developer account and get your own API key.

At the moment it only works with two news sources, the New York Times, Google News, and news y combinator. These easily can be expanded upon if you so choose, just add an 
if statement to the parse method/def and figure out how the api works for that news source. Would highly recommend adding other news sources if you want.

Keywords are unlimited and defined seperately, thus you can have a wide variety of topics to get your news from.

This project was done in part by Aaron Jack's tutorial, I expanded upon it by adding the New York Times and Google News. A link can be seen below to teh exact tutorial:
https://www.youtube.com/watch?v=1UMHhJEaVTQ
