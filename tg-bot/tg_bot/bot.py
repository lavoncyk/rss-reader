

import telegram
import telegram.ext

import commands
import jobs
import settings


def main() -> None:
    """
    Configure and start telegram bot.
    """
    updater = telegram.ext.Updater(settings.TG_BOT_TOKEN)

    command_handlers = [
        telegram.ext.CommandHandler("help", commands.help),
        telegram.ext.CommandHandler("add-rss-feed", commands.add_rss_feed),
        telegram.ext.CommandHandler("del-rss-feed", commands.remove_rss_feed),
    ]
    dispatcher = updater.dispatcher
    for handler in command_handlers:
        dispatcher.add_handler(handler)

    job_queue = updater.job_queue
    job_queue.run_repeating(
        jobs.fetch_feeds,
        interval=float(settings.FETCH_UPDATES_INTERVAL),
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
