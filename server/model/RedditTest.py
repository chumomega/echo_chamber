import praw
import os
from praw.models import MoreComments
from dotenv import load_dotenv


reddit = praw.Reddit("test") # praw.ini file has credetials
reddit.read_only = True
print(reddit.read_only)
    
def get_subreddit(reddit):
    subreddit = reddit.subreddit("redditdev")
    print(subreddit.display_name)
    return subreddit

test_get_sub = get_subreddit(reddit)

def get_hot_submission(subreddit):
    for submission in subreddit.hot(limit=10):
        print(submission.title)
    return

test_get_hot = get_hot_submission(test_get_sub)

url = "https://www.reddit.com/r/funny/comments/3g1jfi/buttons/"

def print_submission_comments(url):

    submission = reddit.submission(url=url)

    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        print(top_level_comment.body)

    submission.comments.replace_more(limit=10)
    for comment in submission.comments.list():
        print(comment.body)

test_comments = print_submission_comments(url)


