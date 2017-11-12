import random
import re
import json

from combat import *
from pdb import set_trace

def load_words(path):
    with open(path, 'r') as f:
        for line in f:
            clean_line = line.strip()
            if clean_line and not clean_line[0] == "#":
                yield clean_line

class MarkovGenerator:
    def __init__(self, words, length):
        self.length = length
        self.transitions = {}

        for word in words:
            key = (None,) * length
            for char in word:
                self.addTransition(key, char)
                key = key[1:] + (char,)
            self.addTransition(key, None)

    def addTransition(self, key, char):
        if key not in self.transitions:
            self.transitions[key] = []
        self.transitions[key].append(char)

    def generate(self):
        result = []
        key = (None,) * self.length

        while key in self.transitions:
            next_char = random.choice(self.transitions[key])
            if next_char is None:
                break
            result.append(next_char)
            key = key[1:] + (next_char,)
        
        return ''.join(result)

town_generator = MarkovGenerator(load_words('../data/towns.txt'), 2)
name_generator = MarkovGenerator(load_words('../data/names_male.txt'), 3)
occupation_list = list(load_words('../data/occupations.txt'))
color_list = list(load_words('../data/colors.txt'))

with open('../monsters.json', 'r') as monster_file:
    monsters_list = json.load(monster_file)

def expand(sentence, **kwargs):
    # set_trace()
    while True:
        matches = list(re.finditer('<([!a-zA-Z0-9:_]*?)>', sentence))
        if not matches:
            return sentence 
        for match in reversed(matches):
            parts = match.group(1).split(':')
            
            if parts[0][0] == '!':
                replacement = kwargs[parts[0][1:]]
            else:
                replacement = globals()[parts[0]]()
            
            if len(parts) >= 2:
                replacement = globals()[parts[1]](replacement)

            sentence = sentence[:match.start(0)] + replacement + sentence[match.end(0):]

def title(words):
    return ' '.join((word[0].upper() + word[1:]) for word in words.split(' '))

def sentence(words):
    return words[0].upper() + words[1:]

def book_title():
    return '# <!pc_name>\'s Journey to Defeat the Evil Wizard <!wiz_name> _(and his many battles along the way)_\n\n'

def chapter_title():
    return '## <a name="chapter<!chapter_number>"></a> Chapter <!chapter_number>: <!town_name> and the <!monster_name:title>\n\n'

def town():
    return town_generator.generate()

def name():
    return name_generator.generate()

def occupation():
    return random.choice(occupation_list)

def color():
    return random.choice(color_list)

def positive_trait():
    return random.choice([
        'bold',
        'courageous',
        'daring',
        'epic',
        'fearless',
        'gallant',
        'grand',
        'gutsy',
        'noble',
        'valiant',
        'classic',
        'elevated',
        'bigger than life',
        'dauntless',
        'doughty',
        'exaggerated',
        'fire-eating',
        'grandiose',
        'gritty',
        'gutty',
        'high-flown',
        'impavid',
        'inflated',
        'intrepid',
        'lion-hearted',
        'mythological',
        'stand tall',
        'stouthearted',
        'unafraid',
        'valorous',
        'undaunted'
    ])

def negative_trait():
    return random.choice([
        'hideous',
        'smelly',
        'terrible',
        'menacing',
        'awful',
        'ruinous',
        'evil',
        'abhorrent',
        'abominable',
        'appalling',
        'awful',
        'cruel',
        'disgusting',
        'dreadful',
        'eerie',
        'frightful',
        'ghastly',
        'grim',
        'grisly',
        'gruesome',
        'heinous',
        'hideous',
        'horrendous',
        'horrid',
        'lousy',
        'nasty',
        'scandalous',
        'scary',
        'shameful',
        'shocking',
        'terrible',
        'terrifying',
        'beastly',
        'detestable',
        'disagreeable',
        'execrable',
        'fairy',
        'fearful',
        'loathsome',
        'lurid',
        'mean',
        'obnoxious',
        'offensive',
        'repellent',
        'repulsive',
        'revolting',
        'sickie',
        'ungodly',
        'unholy',
        'unkind'
    ])

def pc_name():
    return random.choice([
        '<!pc_name>',
        'the <positive_trait> <!pc_name>',
        '<!pc_name> the <positive_trait>'
        'our hero',
        'the adventurer',
        'he',
        'he',
        'he',
        'he'
    ])

def activity():
    return random.choice([
        'sat by the side of the road',
        'rushed by quickly, ignoring him',
        'gazed at him from an open window',
        'talked excitedly with what appeared to be a <occupation>',
        'slowly carried supplies',
        'slept in an alleyway',
        'eyed him suspiciously',
        'scuttled out of his way',
        'stood by a market stall, negotiating with the <occupation>',
        'hawked fine imported goods from <town>',
        'bit into an apple',
        'finished an apple and tossed the core aside',
        'ran from person to person, asking if they had seen <name>',
        'loaded a market stall with wares',
        'threw punches'
    ])

def town_people_sentence():
    return random.choice([
        'A <occupation> <activity>.',
        'While the <occupation> <activity>, a <occupation> <activity>.',
        'Two <occupation>s <activity>.',
        'The <occupation> <activity> with a <occupation>.',
        'Nearby, a <occupation> <activity>.'
    ])

def character_attribute():
    return random.choice([
        'unusual weapons',
        'foreboding cloak',
        'impressive armor',
        'strong forearms',
        'well-made boots',
        'determined look',
        'dangerous demeanor'
    ])

def number():
    return str(random.randint(2, 10))

def building():
    return random.choice([
        'tavern',
        'inn',
        'barn',
        'church',
        'monastery',
        'cattle barn',
        'stables',
        'warehouse'
    ])

def direction():
    return random.choice([
        'left',
        'right'
    ])

def in_town_directions_end():
    return random.choice([
        'It\'s just to the <direction>.',
        'There\'s a small door.',
        'Look for the large hanging sign that reads \"<!armor_name> Fine Supplies\".'
    ])

def in_town_directions():
    return random.choice([
        'down the street to the <building> and <direction>. You\'ll see a <building>. It\'s <in_town_directions>',
        'past the <building>. <in_town_directions_end>',
        'into the market and towards the <building>. Eventually you need to walk <in_town_directions>',
        'just a bit further down the street. <in_town_directions_end>'
    ])

def town_intro():
    return (
        '<!pc_name> followed a dirt path into the village of <!town_name>. <town_people_sentence> <town_people_sentence> '
        '<!pc_name> continued down the path. <town_people_sentence>\n\n'
        'Eventually, <!pc_name> arrived at the town square, where he found a <occupation>. ' +
        random.choice([
            'The man, eying his <character_attribute>, beckoned him forward.\n\n'
            '"Not many people around here like you." he said gruffly. "What makes you think you can step foot in these parts?"\n\n',
            '<!pc_name> approached him, hoping for some advice.\n\n'
        ]) +
        random.choice([
            '"My name is <!pc_name>, and it is my quest to defeat the evil wizard <!wiz_name>." <!pc_name> announced.\n\n',
            '"The evil wizard <!wiz_name> has terrorized these lands for far too long. I <!pc_name> have come to destroy him!" <!pc_name> exclaimed.\n\n',
            '"Do you remember the glory days before the evil wizard <!wiz_name> took over?" <!pc_name> asked. '
            '"I seek to destroy him and restore this kingdom\'s rightful rule!"\n\n'
        ]) +
        '<town_people_sentence> ' +
        random.choice([
            'The man eyed him thoughtfully',
            'He still looked suspicious',
            'The man sat in silence for a while',
            'The man quietly reminised about the past'
        ]) +
        random.choice([
            ', then finally responded.\n\n',
            ', but eventually responded.\n\n',
            'He finally responded.\n\n'
        ]) +
        random.choice([
            '"We have waited for your arrival for many years, <!pc_name>. Is there any way I can be of help?"\n\n',
            '"Our village of <town> will gladly help you on your quest. What do you need?"\n\n'
        ]) +
        '"My weapons were badly damaged on the way here. Could you point me to your armory to get some new supplies?"\n\n' +
        random.choice([
            '"<!armor_name> is the best in town. His shop is <in_town_directions> ',
            '"The armory is <in_town_directions> You\'ll find <!armor_name>, the best weapons expert we\'ve got. ',
            '"<!armor_name> is <in_town_directions> Tell him I sent you. '
        ]) +
        random.choice([
            'And here, take a few gold pieces to buy the best." He reached into his pocket and pulled out <number> small coins. '
            '"I want that <!wiz_name> gone as much as anybody."\n\n',
            'Be careful out there. You\'re not the first to try this adventure. Men stronger than you have vanished or worse."\n\n',
            'I\'d show you myself, but I have urgent matters to attend to here in the square."\n\n'
        ]) +
        '<!pc_name> hurried towards the armory. <town_people_sentence> <town_people_sentence> '
        'Turning the corner, he saw the armory in front of him. He pushed the door open and walked inside.\n\n'
    )

def monster_name():
    return random.choice([monster['name'].strip() for monster in monsters_list])

def monster_description(name):
    matches = [monster for monster in monsters_list if monster['name'].strip() == name]
    if matches and matches[0]['description']:
        return matches[0]['description']
    else:
        return ['The monster ' + name + ' is terrifying for sure, but I honestly don\'t know much about that beast.']

def armory_intro():
    return (
        random.choice([
            '<!armor_name> looked up from his work behind a counter at <!pc_name>.\n\n',
            'There was no one there. <!pc_name> cleared his throat and a man ran out from a backroom.\n\n'
        ]) +
        '"I\'m <!pc_name>, a brave adventurer seeking to destroy <!wiz_name>. What dangers lurk nearby?" he asked.\n\n' +
        random.choice([
            '<!armor_name> grabbed a dusty book from the shelf and flipped through it. Pictures of <monster_name>s and <monster_name>s flew by. '
            'Eventually he settled on a page and started to explain.\n\n',
            '<!armor_name> lifted up his tunic and pointed to a scar. "You see this?" he asked. "Only one monster can do this kind of damage. The <!monster_name>."\n\n',
            '"Brave you say? You may have fought the <monster_name>, or perhaps even the <monster_name>, but that\'s nothing compared to the <!monster_name> we\'ve got."\n\n'
        ])
    )

def armory_explanation():
    return random.choice([
        '"<!description>" <!armor_name> explained.\n\n',
        'The armorer sighed and continued. "<!description>"\n\n',
        '<!armor_name> returned to the book of monsters on the desk and pointed at the terrifying illustration. "<!description>"\n\n'
    ])

def armory_more():
    return random.choice([
        '<!pc_name> looked surprised. "Incredible! Is there anything else I should know?"\n\n',
        '"But my weapons may be too weak. Are there any other ways to defeat the <!monster_name>?" <!pc_name> asked.\n\n',
        '<!pc_name> slipped the man <number> coins. "I get the feeling you\'ve been here for a while. Surely you know more than that."\n\n',
        '"I could handle that. Tell me again, what makes the <!monster_name> so bad?" <!pc_name> responded.\n\n'
    ])

def armory_no_more():
    return random.choice([
        '"That\'s all I can tell you."\n\n',
        '"Anything else you need to know can be found it the book. Take your time." He took the book of monsters and handed it to <!pc_name>.\n\n',
        '"Look I\'ve got other things to attend to. Do you need weapons or not?" His frusturation was visible.\n\n'
    ])