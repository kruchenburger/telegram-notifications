import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode


def set_action_output(output_name: str, output_value: str):
    """
    Writes a GitHub Action output variable to the GITHUB_OUTPUT file.

    Args:
        output_name (str): The name of the output variable.
        output_value (str): The value of the output variable.
    """
    github_otput_file = os.path.abspath(os.environ["GITHUB_OUTPUT"])
    with open(github_otput_file, "a", encoding="UTF-8") as f:
        f.write(f"{output_name}={output_value}")


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """
    Sends a notification that the bot is ready.

    Args:
        update (Update): The PTB update object.
        _ (ContextTypes.DEFAULT_TYPE): Context information (unused).
    """
    await update.message.reply_text(
        "The bot is set up and ready to send notifications!"
    )


async def notify(context: ContextTypes.DEFAULT_TYPE, chat_id: str,
                 message: str):
    """
    Sends a message to a specified chat or channel.

    Args:
        context (ContextTypes.DEFAULT_TYPE): Context information for the bot.
        chat_id (str): The ID of the chat where the message will be sent.
        message (str): The message text to be sent.
    """
    await context.bot.send_message(chat_id=chat_id, text=message,
                                   parse_mode=ParseMode.HTML)


async def main():
    """
    Main entry point of the application.
    """

    github_url = os.getenv("GITHUB_SERVER_URL")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    workflow_name = os.getenv("GITHUB_WORKFLOW")
    ref = os.getenv("GITHUB_REF_NAME")
    commit = os.getenv("GITHUB_SHA")
    run_id = os.getenv("GITHUB_RUN_ID")

    token = os.getenv("INPUT_TOKEN")
    chat_id = os.getenv("INPUT_CHAT_ID")
    status = os.getenv("INPUT_STATUS")

    if token is None:
        raise KeyError("Telegram token is required")
    if chat_id is None:
        raise KeyError("Telegram chat_id is required")
    if status is None:
        raise KeyError("Github status is required")

    repo_url = f"{github_url}/{repo_name}"
    ref_url = f"{repo_url}/tree/{ref}"
    commit_url = f"{repo_url}/commit/{commit}"
    workflow_url = f"{repo_url}/actions/runs/{run_id}"

    status_map = {
        'success': '🟢',
        'failure': '🔴',
        'cancelled': '⚪️'
    }

    status_icon = status_map[status.lower()]

    message = (
        f'<b>Repository:</b> <a href="{repo_url}">{repo_name}</a>\n'
        f'<b>Workflow:</b> <a href="{workflow_url}">{workflow_name}</a>\n'
        f'<b>Branch:</b> <a href="{ref_url}">{ref}</a>\n'
        f'<b>Commit:</b> <a href="{commit_url}">{commit:.7}</a>\n'
        f'<b>Status:</b> {status} {status_icon}'
    )

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler('start', start))
    try:
        await notify(application, chat_id, message)
        set_action_output('status', "Successfully delivered")
    except Exception as e:
        set_action_output('status', "Notification has not been delivered")
        logging.exception(e)
        raise e


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
