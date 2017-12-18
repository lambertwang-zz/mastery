import random
import json

def leave_town():
    return (
        random.choice([
            'With his newfound information, <!pc_name> departs from <!town_name>. ',
            'Sheathing his <!pc_weapon>, <!pc_name> leaves <!town_name> on a journey to find the <!monster_name>. '
        ]) +
        '\n\n' +
        '<journey_ahead>' +
        '<journey_ahead>' +
        '<journey_ahead>' +
        '<journey_ahead>' +
        '<journey_ahead>'
    )

def journey_ahead():
    return (
        random.choice([
            'As <!pc_name> walked along the path out of <!town_name>, he turned to his <direction> and saw something <positive_trait>.\n\n' +
            '<passing_landform>',
            'Continuing along the path, <!pc_name> crossed paths with another traveler.\n\n' +
            '<friendly_encounter>',
            'The ever <positive_trait> <!pc_name> continued his long and tiring journey to find the <!monster_name>.\n\n' +
            'Not once did <pc_name> regret his choice to not become a <occupation>.'
        ]) + '\n\n'
    )

def passing_landform():
    return (
        random.choice([
            'The <landform>s of <town> towered over the nearby <landform>s.',
            'Contrasting against the nearby <landform>s, the great <town> <landform>s provided a refreshing view.',
            'Some distant <landform>s stood out against the horizon.',
            '<pc_name:sentence> could barely make out some <landform>s in the distance.'
        ]) +
        random.choice([
            'It reminded <pc_name> of the town of <town> he had visited long ago.',
            'Maybe they might make for a <positive_trait> adventure for when <!pc_name>\'s current journey is over.'
        ])
    )

def friendly_encounter():
    return (
        '<pc_name:sentence> met a wandering <occupation> making his way toward <!town_name>. ' +
        'The stranger said to <!pc_name>' +
        '\n\n' +
        random.choice([
            '"You must be on your way to kill the <!monster_name>. I wish you the best of luck!"',
            '"Take care crossing the <town> <landform>s! They are especially dangerous this time of year."',
            '"I knew a <positive_trait> hero like you. He met his end far too early. I hope that you are better prepared for your future."',
            '"The <!monster_name> killed my brother. I would be heading back to end that <negative_trait> thing if only it hadn\'t taken my eye the first time I tried."'
        ])
    )
