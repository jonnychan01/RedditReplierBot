import praw
import re
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv('.env')
encryptedPassword = os.getenv("password")
secretClient = os.gentenv("secret")

reddit = praw.Reddit(
    client_id="Rdw80RjbjaDhuar33Z00QQ",
    client_secret= secretClient,
    username="MikeBrownBot_",
    password= encryptedPassword,
    user_agent="script:reply_bot:v1.0 (by u/MikeBrownBot_)"
)

subreddit_name = "Kings"

reply_text = "After possession"

keywords = ["mike brown", "possession"]

replied_to = set()

def log_exception(e, context):
    logging.error(f"Error in {context}: {e}")

def reply_to_comments():
    subreddit = reddit.subreddit(subreddit_name)
    logging.info(f"Monitoring comments in subreddit: r/{subreddit_name}")

    for comment in subreddit.stream.comments(skip_existing=True):
        try:
            if comment.author and comment.author.name == reddit.user.me().name:
                continue

            if comment.id not in replied_to and any(re.search(rf"\b{keyword}\b", comment.body, re.IGNORECASE) for keyword in keywords):
                logging.info(f"Replying to comment ID: {comment.id} by {comment.author}")
                comment.reply(reply_text)
                replied_to.add(comment.id)
                time.sleep(2) 
        except Exception as e:
            log_exception(e, "reply_to_comments")

def reply_to_posts():
    subreddit = reddit.subreddit(subreddit_name)
    logging.info(f"Monitoring posts in subreddit: r/{subreddit_name}")

    for submission in subreddit.stream.submissions(skip_existing=True):
        try:
            if submission.id not in replied_to and any(re.search(rf"\b{keyword}\b", submission.title + " " + submission.selftext, re.IGNORECASE) for keyword in keywords):
                logging.info(f"Replying to post ID: {submission.id} by {submission.author}")
                submission.reply(reply_text)
                replied_to.add(submission.id)
                time.sleep(2) 
        except Exception as e:
            log_exception(e, "reply_to_posts")

if __name__ == "__main__":
    try:
        logging.info(f"Authenticated as: {reddit.user.me()}")
    except Exception as e:
        log_exception(e, "authentication")
        exit(1)

    from threading import Thread

    Thread(target=reply_to_comments).start()
    Thread(target=reply_to_posts).start()
