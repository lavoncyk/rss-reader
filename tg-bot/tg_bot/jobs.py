"""
Module with bot background jobs.
"""

import telegram.ext

from tg_bot.integrations import clients


def fetch_feeds(context: telegram.ext.CallbackContext) -> None:
    """
    Fetch feeds updates.

    Args:
        context (telegram.ext.CallbackContext): A tg bot context object.
    """
    posts_client = clients.PostsClient()
    posts = posts_client.fetch_posts()

    job = context.job
    for post in posts:
        context.bot.send_message(job.context, post["title"])
