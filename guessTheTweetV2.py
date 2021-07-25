# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 01:54:00 2020

@author: Intiser Rajoan

Description: Welcome! This is a modified version of the game of guessing tweet authors.
Here, the user gets to choose any two twitter handlers/usernames to play the game.
Again, all *possible* (max 3200) tweets from kanye west and elon musk is scraped. 
The user is then showed a random tweets and asked to guess whose tweet it is.
The user can choose how many rounds to play the game.
At the end, the user's game stats are displayed.
"""
import tweepy, random, os, time
from dotenv import load_dotenv

def main ():
    # load environment variables for api keys
    load_dotenv()

    # authorization
    api = authorization()

    
    # introduction
    print("Welcome to the game of Guess The Tweet V2!\n")
    print("The rules are simple:")
    print("\t1. You give me two twitter usernames")
    print("\t2. I give you a tweet.")
    print("\t3. You guess the author of the tweet from your two given usernames\n\n")

    # get two usernames
    (user1, user2) = getTwitterUsernames()

    # scrape tweets
    print(f"Please wait. Getting tweets of {user1} and {user2}...")
    user1TweetObjects = scrape_tweet_objects(api, user1)
    user2TweetObjects = scrape_tweet_objects(api, user2)
    
    # filter the tweets
    user1FilteredTweetObjects = filter_tweet_objects(user1TweetObjects, user1)
    user2FilteredTweetObjects = filter_tweet_objects(user2TweetObjects, user2)

    # get tweet texts
    user1Tweets = get_tweet_texts(user1FilteredTweetObjects)
    user2Tweets = get_tweet_texts(user2FilteredTweetObjects)

    # display scraping stats -- uncomment if you want to view the stats 
    # print("Done! Here are the scraping stats -")
    # display_scraping_stats(user1, user1TweetObjects, user1FilteredTweetObjects)
    # display_scraping_stats(user2, user2TweetObjects, user2FilteredTweetObjects)

    # play the game
    print("\nDone. Let's start!")
    playGuessTheTweet(user1, user2, user1Tweets, user2Tweets)

# take two usernames from user
def getTwitterUsernames():
    user1 = input("\nType a twitter username: ")
    user2 = input("Type another Twitter username: ")
    
    return (user1, user2)

# play game
def playGuessTheTweet(user1, user2, user1Tweets, user2Tweets):
    """ Input: two lists containing the texts of tweets of two users. 
    Plays the game and displays the results. Returns nothing"""
    allTweets = user1Tweets + user2Tweets  # combine the two lists of tweets
    correctPoints = 0
    gameRounds = int(input("How many rounds do you want to play? - "))
    print("You ready?")
    time.sleep(1)
    for x in range(gameRounds):
        print("\nRound", x+1)
        print("Can you guess who tweeted this?")
        # print a random tweet and take user's guess
        randomTweet = random.choice(allTweets)
        print(randomTweet)
        userGuess = int(input(f"Type 1 or 2:\n(1) {user1}\t(2) {user2}\n"))
        # check and display correctness of the guess 
        if ((randomTweet in user1Tweets) and (userGuess == 1)) or \
             ((randomTweet in user2Tweets) and (userGuess == 2)):
            print("Correct!")
            correctPoints += 1
        else:
            print("Incorrect.")
        print("\n---------------------------------")
        time.sleep(1)

    # display game stats
    print("Game over.\n[Your game stats]")
    print("Number of rounds: ", gameRounds)
    print("Correctly guessed: ", correctPoints)
    print("\n---------------------------------")
    print("Thank you for playing :)\n")
    
#authorization
def authorization():
    """Completes the authorization using the api keys"""
    auth = tweepy.OAuthHandler(consumer_key = os.getenv("TWITTER_API_KEY"), \
        consumer_secret = os.getenv("TWITTER_API_SECRET"))
    auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), \
        os.getenv("TWITTER_ACCESS_SECRET"))
    return tweepy.API(auth)

# scrape tweet objects
def scrape_tweet_objects(api, user):
    """Input: the api and a string of the username. 
    Scrapes all available (max 3200) tweets from the specified username. 
    Returns a list of all the tweet objects""" 

    # scrape the latest 200 tweets
    tweetObjectTemp = api.user_timeline(id=user, 
                                        count=200, 
                                        tweet_mode='extended', 
                                        include_rts=True)
    tweetObjectsAll = []
    tweetObjectsAll.extend(tweetObjectTemp)
    lastId = tweetObjectsAll[-1].id
    # gets the id of the last scraped tweet and in the next iteration of the loop,
    # grabs 200 more tweets up to that id
    while len(tweetObjectsAll):
        tweetObjectTemp = api.user_timeline(id=user, 
                                            count=200, 
                                            tweet_mode='extended', 
                                            include_rts=True, 
                                            max_id=lastId-1)
        # break loop if no more tweets
        if len(tweetObjectTemp) == 0:
            break
        lastId = tweetObjectTemp[-1].id
        tweetObjectsAll.extend(tweetObjectTemp)
    
    #return 3200 if more than 3200
    if len(tweetObjectsAll) > 3200:
        return tweetObjectsAll[:3200]

    return tweetObjectsAll   

#filter tweet objects
def filter_tweet_objects(tweetObjects, username):
    """Input: a list of all the scraped tweet objects and a string of the username. 
    Applies filters to return a new list of tweet objects, 
    excluding the ones which contain retweets, urls, user mentions or media."""
    return [t for t in tweetObjects if (t.entities.get('user_mentions') == [] and       #filter for user mentions
                                        t.entities.get('urls') == [] and                #filter of urls
                                        t.entities.get('media') == None and             #filters for pictures and videos
                                        t._json.get('retweeted_status') == None and     #filter for retweets
                                        (t.in_reply_to_screen_name == None or 
                                        t.in_reply_to_screen_name == username))]        #filter for replies

# get only the texts from tweets
def get_tweet_texts (tweetObjects):
    """Input: a list of the filtered tweet objects.
    Returns a list containing only the texts of all tweet objects."""
    return [t.full_text for t in tweetObjects]

# displays scraping stats
def display_scraping_stats(user ,tweetObj, filteredObj):
    """Input: string of username, and two lists of unfiltered and filtered tweet objects. 
    Displays the scraping statistics of the username"""
    print("Here are the scraping stats - ")
    print(f"{user} Tweet Stats")
    print("----------------------------")
    print(f"Scraped Tweets: {len(tweetObj)}")
    print(f"Filtered Tweets: {len(filteredObj)}\n")


if __name__ == "__main__":
    main()



    
    


