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
    'sushi': ['sushi'],
    'fancy': ['fancy'],
    'sleep': ['sleep', 'zzz', 'tired'],
    'bake': ['bake', 'baker', 'baking', 'cooking', 'cook', 'baker cat'],
    'sit': ['sit', 'neutral'],
    'lying_down': ['lazy'],
    'writing': ['writing'],
    'nap': ['nap', 'zzz', 'tired'],
    'book': ['book', 'reading', 'read'],
    'piano': ['piano', 'music'],
    'wat': ['wat', 'huh', 'surprised', 'surprise'],
    'excited': ['excited', ':D', 'yay', 'happy'],
    'pizza': ['pizza'],
    'fast_food': ['drink', 'burger'],
    'dj': ['dj', 'music'],
    'aww': ['aww', 'cute'],
    'workout': ['workout', 'gym', 'ddr'],
    'uhh': ['uhh', '...', u'\u2026'],  # slack condenses ...
    'wave': ['wave', 'hi', 'hello', 'hey'],
    'birthday': ['birthday', 'cake', 'happy birthday'],
    'wink': ['wink', ';)', ';D'],
    'unicorn': ['unicorn'],
    'ramen': ['ramen', 'noodles'],
    'cool': ['cool', 'B)'],
    'box': ['box', 'dropbox'],
    'giggle': ['hehe', 'haha', 'giggle', 'lol'],
    'tantrum': ['tantrum', 'angry', 'D:<'],
    'cry': ['cry', 'sad', ':('],
    'yarn': ['yarn', 'knitting'],
    'donut': ['donut'],
    'popcorn': ['popcorn'],
    'grumpy': ['grumpy', '):<', 'angry'],
    'blush': ['blush', 'embarassed', 'blushing'],
    'annoyed': ['annoyed', 'grumpy'],
    'vroom': ['vroom', 'bike', 'travel'],
    'bread': ['bake', 'baker', 'bread'],
    'coffee': ['drink', 'coffee', 'tea', 'hot chocolate'],
    'dough': ['stir', 'cook', 'cooking'],
    'groceries': ['groceries', 'shopping'],
    'helicopter': ['helicopter', 'fly', 'flying', 'plane'],
    'milk': ['cheers', 'congrats', 'milk'],
    'salad': ['salad'],
    'sandwich': ['sandwich', 'lunchbox'],
    'cupcake': ['cupcake'],
    'cookie': ['cookie'],
    'rice': ['rice'],
    'confused': ['confused', 'uhh', 'sweatdrop'],
    'cough': ['cough', 'sick'],
    'kiss': ['kiss'],
}

# give all the food pusheens some shared keywords
for food_pusheen in ['sushi', 'pizza', 'fast_food', 'ramen', 'donut', 'popcorn', 'bread', 'coffee',
                     'coffee', 'salad', 'sandwich', 'cupcake', 'cookie', 'rice']:
    pusheens[food_pusheen] += ['food', 'eat', 'eating', 'yum', 'hungry']


# map to words that should trigger the usagyuuun
usagyuuuns = {
    'beer': ['beer', 'drink', 'drinking', 'drunk', 'soju'],
    'boring': ['boring', 'bored'],
    'carrot_roll': ['carrot', 'roll', 'rolling'],
    'clap': ['clap', 'wave', 'hi', 'hello'],
    'confetti': ['congrats', 'congratulations', 'confetti', 'nice'],
    'cry': ['cry', 'sad', 'crying', ':('],
    'cry_joy': ['happy tears'],
    'dab': ['dab', 'dance', 'excited'],
    'dead_kinda': ['dead', 'rip', 'ghost'],
    'devil': ['devil', 'excited'],
    'devil_dance': ['devil', 'hahaha', 'ha ha ha', 'laugh'],
    'disco_carrot': ['disco carrot', 'carrot', 'tada'],
    'dying': ['dead', 'rip'],
    'exclaim': ['!', 'surprised', 'surprise'],
    'fairy': ['fairy'],
    'funky_dance': ['dance', 'funky dance', 'weird dance'],
    'head_slam': ['head slam', 'headdesk', 'head desk', 'argh'],
    'heart_circle': ['heart', 'love', 'heart circle'],
    'heart_get': ['get heart', 'heart', 'love'],
    'heart_give': ['give heart', 'heart', 'love'],
    'hearts': ['heart', 'hearts', 'wave hearts', 'love'],
    'jumping_jack': ['jumping jack', 'starjump', 'excited'],
    'lets_go': ['lets go', "let's go", 'car'],
    'long_rabbit': ['long', 'excited'],
    'maracas': ['maracas', 'cheer'],
    'muscle_man': ['muscle man', 'flexing', 'flex', 'gym', 'ddr'],
    'no': ['no', 'noo', 'nooo', 'noooo', 'nooooo', 'noooooo', 'nooooooo'],
    'omw': ['omw', 'on my way'],
    'peek': ['peek'],
    'pom_pom': ['pompom', 'pom pom', 'cheer'],
    'punish': ['punish'],
    'pushups': ['pushups', 'pushup', 'gym', 'ddr'],
    'question': ['?', '??', '???', 'question'],
    'rub_rub': ['hug', 'love', 'heart'],
    'salute': ['salute'],
    'shake_rabbit': ['shake'],
    'sing_song': ['sing', 'singing', 'music', 'karaoke'],
    'slap_ground': ['yes'],
    'sonic_speed': ['fast', 'omw', 'on my way'],
    'spin': ['spin'],
    'squirm': ['squirm'],
    'sweat': ['sweat', 'uh oh'],
    'throw_up': ['congrats', 'congratulations', 'nice', 'throw up'],
    'typing': ['typing', 'laptop'],
    'uh_oh': ['uh oh'],
    'up_lock': ['up lock', 'uplock'],
    'what': ['what', 'what?'],
    'zzzzzz': ['zzz', 'zzzz', 'zzzzz', 'zzzzzz', 'sleep'],
}

# helper to construct the map the other way
def reverse_map(sticker_to_words):
    word_to_stickers = defaultdict(list)
    for image, words in sticker_to_words.iteritems():
        for word in words:
            word_to_stickers[word].append(image)
    return word_to_stickers

stickers_to_words_by_set = {
    'pusheen': pusheens,
    'usagyuuun': usagyuuuns,
}

words_to_stickers_by_set = {
    set_name: reverse_map(stickers) for set_name, stickers in stickers_to_words_by_set.iteritems()
}

class PusheenHandler(webapp2.RequestHandler):
    def get(self):
        text = self.request.get("text").lower()
        size_mod = '_small'  # return small pusheens by default
        sticker_mod = 'pusheen'  # return pusheens by default (lol)

        if '--big' in text:
            text = text.replace('--big', '').strip()
            size_mod = ''  # remove size mod

        if '--usagyuuun' in text:
            text = text.replace('--usagyuuun', '').strip()
            sticker_mod = 'usagyuuun'

        sticker_set = words_to_stickers_by_set[sticker_mod]
        sticker_names = stickers_to_words_by_set[sticker_mod]

        if text and text in sticker_set:
            images = sticker_set[text]
            image_name = images[random.randint(0, len(images) - 1)]
        else:
            image_name = sticker_names.keys()[random.randint(0, len(sticker_names) - 1)]

        # construct response
        self.response.content_type = 'application/json'
        resp = {
            'response_type': 'in_channel',
            'attachments': [{
                'text': 'Meow!' if sticker_mod == 'pusheen' else '',
                'image_url': 'http://pusheen-slash-command.appspot.com/img/' + sticker_mod + '/' + image_name + size_mod + '.gif',
            }]
        }
        self.response.out.write(json.dumps(resp))

app = webapp2.WSGIApplication([
    ('/get', PusheenHandler),
    ('/', MainHandler)
],
debug=True)
