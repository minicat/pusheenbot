#!/usr/bin/env python

from collections import defaultdict
import json
import random
import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('meow!')

# map to words that should trigger the pusheen
pusheens = {
    'heart': ['heart', 'love', '<3'],
    'shock': ['shock', ':O', 'surprise'],
    'laptop': ['laptop', 'typing', 'work'],
    'sushi': ['sushi', 'food', 'eat', 'yum', 'hungry'],
    'fancy': ['fancy'],
    'sleep': ['sleep', 'zzz', 'tired'],
    'bake': ['bake', 'baker', 'cooking', 'cook'],
    'sit': ['sit', 'neutral'],
    'lying_down': ['lazy'],
    'writing': ['writing'],
    'nap': ['nap', 'zzz', 'tired'],
    'book': ['book', 'reading', 'read'],
    'piano': ['piano', 'music'],
    'wat': ['wat', 'huh', 'surprised', 'surprise'],
    'excited': ['excited', ':D', 'yay', 'happy'],
    'pizza': ['pizza', 'food', 'eat', 'hungry'],
    'fast_food': ['food', 'eat', 'drink', 'hungry'],
    'dj': ['dj', 'music'],
    'aww': ['aww', 'cute'],
    'workout': ['workout', 'gym', 'ddr'],
    'uhh': ['uhh', '...', u'\u2026'],  # slack condenses ...
    'wave': ['wave', 'hi', 'hello', 'hey'],
    'birthday': ['birthday', 'cake', 'happy birthday'],
    'wink': ['wink', ';)', ';D'],
    'unicorn': ['unicorn'],
    'ramen': ['ramen', 'food', 'eat', 'noodles', 'yum', 'hungry'],
    'cool': ['cool', 'B)'],
    'box': ['box', 'dropbox'],
    'giggle': ['hehe', 'haha', 'giggle', 'lol'],
    'tantrum': ['tantrum', 'angry', 'D:<'],
    'cry': ['cry', 'sad', ':('],
    'yarn': ['yarn', 'knitting'],
    'donut': ['donut', 'food', 'eat'],
    'popcorn': ['popcorn'],
    'grumpy': ['grumpy', '):<', 'angry'],
    'blush': ['blush', 'embarassed', 'blushing'],
    'annoyed': ['annoyed', 'grumpy'],
    'vroom': ['vroom', 'bike', 'travel']
}

# construct the map the other way
text_to_pusheens = defaultdict(list)
for image, words in pusheens.iteritems():
    for word in words:
        text_to_pusheens[word].append(image)


class PusheenHandler(webapp2.RequestHandler):
    def get(self):
        text = self.request.get("text").lower()

        if text and text in text_to_pusheens:
            images = text_to_pusheens[text]
            image_name = images[random.randint(0, len(images) - 1)]
        else:
            image_name = pusheens.keys()[random.randint(0, len(pusheens) - 1)]

        # construct response
        self.response.content_type = 'application/json'
        resp = {
            'response_type': 'in_channel',
            'attachments': [{
                'text': 'Meow!',
                'image_url': 'http://pusheen-slash-command.appspot.com/img/' + image_name + '.gif',
            }]
        }
        self.response.out.write(json.dumps(resp))

app = webapp2.WSGIApplication([
    ('/get', PusheenHandler),
    ('/', MainHandler)
],
debug=True)
