# Telegram Notifier

## Usage

1. To get started, message [@BotFather](https://t.me/botfather) on Telegram to register your bot and receive its authentication token. See the official instruction here: [#creating-a-new-bot](https://core.telegram.org/bots/features#creating-a-new-bot)
2. You can get the chat_id you need using this bot [@username_to_id_bot](https://t.me/username_to_id_bot)
3. If you want to send notifications to a channel or group chat, you need to add your bot there

### Example workflow

```yaml
name: Example Workflow
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master

    - name: Log in to the Container registry
      uses: docker/login-action@65b78e6e13532edd9afa3aa52ac7964289d1a9c1
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata (tags, labels) for Docker
      id: meta
      uses: docker/metadata-action@9ec57ed1fcdbf14dcef7dfbe97b2010124a938b7
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}

    - name: Build and push Docker image
      id: push
      uses: docker/build-push-action@f2a1d5e99d037542a71f64918e516c093c6f3fc4
      with:
        file: Dockerfile
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}

    - name: Telegram Notification
      if: always()
      uses: kruchenburger/telegram-notifier@master # you can put here any branch or version
      with:
        status: ${{ job.status }} # this line is required and should not change.
        token: ${{ secrets.TG_TOKEN }}  # always keep the telegram api token secret, especially in a public repository
        chat_id: ${{ secrets.TG_CHAT_ID }} # user or chat ID or @channel_name
```

### Inputs

| Input     | Description                                                                                                         |
| --------- | ------------------------------------------------------------------------------------------------------------------- |
| `status`  | The current status of the job.                                                                                      |
| `token`   | Telegram api token for your notification bot.                                                                       |
| `chat_id` | User or chat ID or channel name to which notifications should be sent. @channel_name work only for public channels. |

### Outputs

| Output   | Description                                                                                                                                             |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `status` | Returns the status of the message delivery. `Successfully delivered` if action complited with success and `Notification has not been delivered` if not. |

## How to use in your Workflow

Just add this step in the end of your pipeline

```yaml
  - name: Telegram Notification
    if: always()
    uses: kruchenburger/telegram-notifier@master # you can put here any branch or version
    with:
      status: ${{ job.status }} # this line is required and should not change.
      token: ${{ secrets.TG_TOKEN }}  # always keep the telegram api token secret, especially in a public repository
      chat_id: ${{ secrets.TG_CHAT_ID }} # user or chat ID or @channel_name
```
