from winreg import QueryValue
import tweepy
import configparser
import pandas

#read configs
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authentication

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()

columns = ['Time', 'User', 'Tweet']
data = []

print("**************************************")


# function to display data of each tweet
def printtweetdata(n, ith_tweet):
        print()
        print(f"Tweet {n}:")
        print(f"Date:{ith_tweet[0]}")
        print(f"Username:{ith_tweet[1]}")
        print(f"Description:{ith_tweet[2]}")
        print(f"Location:{ith_tweet[3]}")
        print(f"Following Count:{ith_tweet[4]}")
        print(f"Follower Count:{ith_tweet[5]}")
        print(f"Total Tweets:{ith_tweet[6]}")
        print(f"Retweet Count:{ith_tweet[7]}")
        print(f"Tweet Text:{ith_tweet[8]}")
        print(f"Hashtags Used:{ith_tweet[9]}")
 
 
# function to perform data extraction
def scrape(words, date_since, numtweet):
 
        # Creating DataFrame using pandas
        db = pandas.DataFrame(columns=['date',
                                   'username',
                                   'description',
                                   'location',
                                   'following',
                                   'followers',
                                   'totaltweets',
                                   'retweetcount',
                                   'text',
                                   'hashtags'])
 
        # We are using .Cursor() to search
        # through twitter for the required tweets.
        # The number of tweets can be
        # restricted using .items(number of tweets)
        tweets = tweepy.Cursor(api.search_tweets,
                               words, lang="en",
                               since_id=date_since,
                               tweet_mode='extended').items(numtweet)
 
 
        # .Cursor() returns an iterable object. Each item in
        # the iterator has various attributes
        # that you can access to
        # get information about each tweet
        list_tweets = [tweet for tweet in tweets]
 
        # Counter to maintain Tweet Count
        i = 1
 
        # iterate over each tweet in the
        # list for extracting information about each tweet
        for tweet in list_tweets:
                date = tweet.user.date
                username = tweet.user.screen_name
                description = tweet.user.description
                location = tweet.user.location
                following = tweet.user.friends_count
                followers = tweet.user.followers_count
                totaltweets = tweet.user.statuses_count
                retweetcount = tweet.retweet_count
                hashtags = tweet.entities['hashtags']
 
                # Retweets can be distinguished by
                # a retweeted_status attribute,
                # in case it is an invalid reference,
                # except block will be executed
                try:
                        text = tweet.retweeted_status.full_text
                except AttributeError:
                        text = tweet.full_text
                hashtext = list()
                for j in range(0, len(hashtags)):
                        hashtext.append(hashtags[j]['text'])
 
                # appending all the
                # extracted information in the DataFrame
                ith_tweet = [date, username, description,
                             location, following,
                             followers, totaltweets,
                             retweetcount, text, hashtext]
                db.loc[len(db)] = ith_tweet
 
                # Function call to print tweet data on screen
                printtweetdata(i, ith_tweet)
                i = i+1
        filename = 'TweetDatasetNew.csv'


 
        # save thedatabase as a CSV file.
        db.to_csv(filename)

        # Enter Hashtag and initial date
print("Enter Twitter HashTag to search for")
words = input()
print("Enter Date since The Tweets are required in yyyy-mm--dd")
date_since = input()
 
        # number of tweets you want to extract in one run
numtweet = 1000
scrape(words, date_since, numtweet)
print('Scraping has completed!')



#print(public_tweets[0].user.screen_name )

#for tweet in public_tweets:
#    data.append([tweet.created_at, tweet.user.screen_name, tweet.text])

#df = pandas.DataFrame(data, columns=columns)

#df.to_csv('tweetsdemo.csv')
#print(public_tweets[0].text)
