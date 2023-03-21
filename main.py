# All print functions have been used to keep track of the program
import snscrape.modules.twitter as sntwitter
import pandas as pd

def get_column_as_list(file_path, column_index):
    """Reads data from a file and returns the specified column as a list."""
    df = pd.read_csv(file_path)
    column = df.iloc[:, column_index-1].tolist()
    return column

def extract_tweet_id(url):
    """Extracts the tweet ID from a tweet URL."""
    try:
        return url.split("/")[-1].split("?")[0]
    except:
        return 404
    
def strip(text):
    """ Remove extra lines and comas to write to csv file without errors """
    text = text.replace('\n', ' ')
    text = text.replace(',', ' ')
    return(text)

def influencer_data(tweet_id):
    """ Returning order: Profile Link, Tweet Url, Tweet Likes, Tweet Content """
    try:
        response = sntwitter.TwitterTweetScraper(tweet_id).get_items()
        for tweet in response:
            pf_url = tweet.user.url
            tweet_url = tweet.url
            like_count = tweet.likeCount
            tweet_text = strip(tweet.rawContent)
            return [pf_url, tweet_url, like_count, tweet_text]
    except:
        return ["Tweet Deleted", "Tweet Deleted", "Tweet Deleted", "Tweet Deleted"]
    


def tweet_data(tweet_id, current_link):
    """ Returning Order: Date, Influencer Profile Url, Promoter Profile Url, Influencer Tweet Url, Promoter Tweet Url, Influencer Likes, Promoter Likes, Influencer Tweet, Promoter Tweet  """
    try:
        response = sntwitter.TwitterTweetScraper(tweet_id).get_items()
        for tweet in response:
            # promoter's data:
            promoter_tweet_text = strip(tweet.rawContent)
            promoter_tweet_likes = tweet.likeCount
            promoter_tweet_link = tweet.url
            promoter_profile_url = tweet.user.url
            promoter_tweet_date = tweet.date

            influencer_tweet_id = tweet.inReplyToTweetId #will be used to fetch the influencer tweet and it's likes
            temp = influencer_data(influencer_tweet_id)

            # Influencer tweet data
            influencer_profile_url = temp[0]
            influencer_tweet_url = temp[1]
            influencer_tweet_likes = temp[2]
            influencer_tweet_text = temp[3]

            return [promoter_tweet_date, influencer_profile_url, promoter_profile_url, influencer_tweet_url, promoter_tweet_link, influencer_tweet_likes, promoter_tweet_likes, influencer_tweet_text, promoter_tweet_text]
    except:
        return ["Tweet Deleted", "Tweet Deleted", "Tweet Deleted", "Tweet Deleted", f"{current_link}", "Tweet Deleted", "Tweet Deleted", "Tweet Deleted", "Tweet Deleted"]

def write(list, link_list):
    """ Writes the obtained data to output.csv """
    file_ref = open('output.csv', 'w', encoding='utf-8')
    file_ref.write('timestamp,influencer_profile,promoter_profile,influencer_tweet_url,promotion_tweet_url,influencer_tweet_likes,promoter_tweet_likes,influencer_tweet_text,promoter_tweet_text\n')
    index = 0
    for items in list:
        index += 1
        print(f'Lines written: {index}')
        try:
            for item in items:
                file_ref.write(f'{str(item[0])},{item[1]},{item[2]},{item[3]},{item[4]},{item[5]},{item[6]},{item[7]},{item[8]}\n')
        except:
            file_ref.write(f'Tweet Deleted,Tweet Deleted,Tweet Deleted,Tweet Deleted,{link_list[index]},Tweet Deleted,Tweet Deleted,Tweet Deleted,Tweet Deleted\n')



links = get_column_as_list('./input.csv', 5) # Reading column number  of input.csv
resulting_data = [] # Data scrapped will be stored here
counter = 0 # To keep track of program
for link in links:
    counter+=1
    data = tweet_data(extract_tweet_id(link), link) # Scrapping tweet data
    resulting_data.append([data])
    print(f"Urls Fetched: {counter}")
    print(link)
write(resulting_data, links)