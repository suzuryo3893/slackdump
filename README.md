# slackdump

Dump slack history using Slack Conversation API.
Only channels to which you belong are dumped.
Replies are also dumped.

# Requirements

* Python3
  * requests
  * lxml

# How

1. Obtain a legacy token of Slack API from [here](https://api.slack.com/custom-integrations/legacy-tokens).
2. Move to a convenient directory
3. `python /path/to/slackdump.py -t your_token channel_name1 channel_name2 ...`
   Set \* as channel_name for dump all channels you belong to.
   `users.json` and `channels.json` will be generated in the current directory.
4. `python /path/to/generate_html.py` for generating html
   `result.html` will be generated.

# LICENSE
MIT
