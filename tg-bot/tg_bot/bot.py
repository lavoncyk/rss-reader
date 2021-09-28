

import telegram
import telegram.ext

import jobs
import settings


def main() -> None:
    """
    Configure and start telegram bot.
    """
    updater = telegram.ext.Updater(settings.TG_BOT_TOKEN)

    job_queue = updater.job_queue
    job_queue.run_repeating(
        jobs.fetch_feeds,
        interval=float(settings.FETCH_UPDATES_INTERVAL),
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
