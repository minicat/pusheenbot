# pusheenbot

Pusheenbot is a [Slack /slash command](https://api.slack.com/slash-commands) that allows you to post animated Pusheen stickers to Slack. (And usagyuuuns!)

This repo contains two components of Pusheenbot:
* **pusheen-slash-command** - simple [Google app engine](https://cloud.google.com/appengine/) webserver for the slash command
* **pusheen-stickers** - script to generate Pusheen .gifs from .pngs


## TODOs
* Simple sentiment analysis for unrecognised words
* Include more food stickers
* Include other Pusheens (from webcomic, LINE, etc)
* De-dupe Pusheen images in /img (to prevent breakage of prior usages, the pusheen images exist both in /img and /img/pusheen)
* Split out usagyuuuns into a separate slash command endpoint