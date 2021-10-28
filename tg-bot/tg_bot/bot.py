"""
Module with TG bot configuring logic.
"""

import telegram
import telegram.ext as tg_ext

import commands
import jobs
import settings


def _add_command_handlers(bot: telegram.ext.Updater) -> None:
    """Add command handlers for bot.

    Args:
        bot (telegram.ext.Updater): A bot instance.
    """
    disp = bot.dispatcher
    disp.add_handler(tg_ext.CommandHandler("help", commands.help))
    disp.add_handler(tg_ext.CommandHandler("addfeed", commands.add_feed))
    disp.add_handler(tg_ext.CommandHandler("delfeed", commands.del_feed))


def _add_jobs(bot: telegram.ext.Updater) -> None:
    """Add jobs for bot.

    Args:
        bot (telegram.ext.Updater): A bot instance.
    """
    job_queue = bot.job_queue
    job_queue.run_repeating(
        jobs.fetch_feeds,
        interval=float(settings.FETCH_UPDATES_INTERVAL),
    )


def main() -> None:
    """
    Configure and start telegram bot.
    """
    updater = tg_ext.Updater(settings.TG_BOT_TOKEN)

    _add_command_handlers(updater)
    _add_jobs(updater)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
