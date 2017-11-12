import random
import re

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

def expand(sentence, **kwargs):
    while True:
        matches = list(re.finditer('<(.*?)>', sentence))
        if not matches:
            return sentence 
        for match in reversed(matches):
            key = match.group(1)
            if key[0] == '!':
                replacement = kwargs[key[1:]]
            else:
                replacement = globals()[key]()
            sentence = sentence[:match.start(0)] + replacement + sentence[match.end(0):]

def town():
    return town_generator.generate()

def name():
    return name_generator.generate()

def occupation():
    return random.choice(occupation_list)

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
        'right',
        'slightly left',
        'slightly right'
    ])

def in_town_directions_end():
    return random.choice([
        'It\'s just to the <direction>.',
        'There\'s a small door.',
        'Look for the large hanging sign that reads \"<!armor_name> Fine Supplies\".'
    ])

def in_town_directions():
    return random.choice([
        'down the street to the <building> and turn <direction>. You\'ll see a <building>. Go <in_town_directions>',
        'past the <building>. Continue <in_town_directions>',
        'into the market and walk towards the <building>. Eventually you need to walk <in_town_directions>',
        'just a bit further down the street. <in_town_directions_end>'
    ])

def town_intro():
    return (
        '<!pc_name> followed a dirt path into the village. <town_people_sentence> <town_people_sentence> '
        '<!pc_name> continued down the path. <town_people_sentence>\n'
        'Eventually, <!pc_name> arrived at the town square, where he found a <occupation>. ' +
        random.choice([
            'The man, eying his <character_attribute>, beckoned him forward.\n'
            '"Not many people around here like you." he said gruffly. "What makes you think you can step foot in these parts?"\n',
            '<!pc_name> approached him, hoping for some advice.\n'
        ]) +
        random.choice([
            '"My name is <!pc_name>, and it is my quest to defeat the evil wizard <!wiz_name>." <!pc_name> announced.\n',
            '"The evil wizard <!wiz_name> has terrorized these lands for far too long. I <!pc_name> have come to destroy him!" <!pc_name> exclaimed.\n',
            '"Do you remember the glory days before the evil wizard <!wiz_name> took over?" <!pc_name> asked. '
            '"I seek to destroy him and restore this kingdom\'s rightful rule!"\n'
        ]) +
        '<town_people_sentence> ' +
        random.choice([
            'The man eyed him thoughtfully',
            'He still looked suspicious',
            'The man sat in silence for a while',
            'The man quietly reminised about the past'
        ]) +
        random.choice([
            ', then finally responded.\n',
            ', but eventually responded.\n',
            'He finally responded.\n'
        ]) +
        random.choice([
            '"We have waited for your arrival for many years, <!pc_name>. Is there any way I can be of help?"\n',
            '"Our village of <town> will gladly help you on your quest. What do you need?"\n'
        ]) +
        '"My weapons were badly damaged on the way here. Could you point me to your armory to get some new supplies?"\n' +
        random.choice([
            '"<!armor_name> is the best in town. His shop is <in_town_directions> ',
            '"Go <in_town_directions> You\'ll find <!armor_name>, the best weapons expert we\'ve got. ',
            '"<!armor_name> is <in_town_directions>. Tell him I sent you. '
        ]) +
        random.choice([
            'And here, take a few gold pieces to buy the best." He reached into his pocket and pulled out <number> small coins. '
            'I want that <!wiz_name> gone as much as anybody."\n',
            'Be careful out there. You\'re not the first to try this adventure. Men stronger than you have vanished or worse."\n',
            'I\'d show you myself, but I have urgent matters to attend to here in the square."\n'
        ]) +
        '<!pc_name> hurried towards the armory. <town_people_sentence> <town_people_sentence> '
        'Turning the corner, he saw the armory in front of him.'
    )
