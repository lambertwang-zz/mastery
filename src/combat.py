import random
import json

monster = None

def find_monster(name):
    matches = [monster for monster in monsters_list if monster['name'].strip() == name]
    return matches[0]

def combat_intro(name = None):
    if name == None:
        return (
            '<!pc_name> sees no hostile entities. '
        )
    global monster
    monster = find_monster(name)

    return (
        '<!pc_name> saw a <negative_trait> <!monster_name> in the distance! ' + 
        random.choice([
            '<pc_name:sentence> readied his sword. ',
            'Our hero fixed his gaze on the <negative_trait> sight. '
        ]) +
        '<!pc_name> hurried towards the enemy, ready to strike it down with all his might! '
        '\n\n'
    )

def combat():
    if monster['hitpoints'] <= 0:
        return '<pc_attack><monster_dead>'
    return (
        random.choice([
            '<monster_attack><pc_attack>',
            '<pc_attack><monster_attack><pc_attack>',
            '<pc_attack><monster_stunned><pc_attack>',
            '<monster_attack><pc_stunned><monster_attack>',
            '<monster_passing><pc_attack>',
            '<monster_passing><monster_attack>',
            '<pc_passing><monster_attack>',
            '<pc_passing><pc_attack>',
            '<pc_passing><monster_passing>',
            '<pc_attack><monster_stunned><pc_passing>',
            '<monster_attack><pc_stunned><monster_passing>'
        ]) + 
        '\n\n<combat>'
    )

def pc_attack():
    hit = False
    if random.random() < 0.40:
        hit = True

    return (
        '<!pc_name> lunged toward the <!monster_name>, his <!pc_weapon> ready to strike! ' +
        ('<pc_hit>' if hit else '<pc_miss>')
    )

def monster_attack():
    global monster
    hit = False
    if random.random() < 0.25:
        hit = True

    try:
        weapon = monster['melee']
        return (
            'The <!monster_name> struck with its ' + weapon['name'] + '! ' +
            ('<monster_hit>' if hit else '<monster_miss>')
        )
    except:
        pass
    try:
        weapon = monster['ranged']
        return (
            '<!monster_name> fired a shot with its ' + weapon['name'] + '! ' +
            ('<monster_hit>' if hit else '<monster_miss>')
        )
    except:
        pass
    return (
        '<!monster_name> lunged toward <!pc_name>! ' +
        ('<monster_hit>' if hit else '<monster_miss>')
    )

def pc_stunned():
    return (
        random.choice([
            '<pc_name:sentence> leaned on his <!pc_weapon> to catch a moment\'s respite. ' +
            '<pc_name:sentence> was worn out by the combat. ',
            'The exhilarating combat made the hours seem like seconds. ',
            '<pc_name> stumbles to his knee, gasping for breath. '
        ])
    )

def pc_passing():
    return (
        random.choice([
            '<pc_name:sentence> sneaked around to <!monster_name>\'s blind spot. ',
            '<pc_name:sentence> pulls a <color> potion from his pack and drinks it. He is reinvigorated. '
        ])
    )

def pc_hit():
    damage = random.randint(0, 20)
    monster['hitpoints'] -= damage
    return (
        ('<monster_struck_soft>' if damage < 5 else ('<monster_struck_med>' if damage < 16 else '<monster_struck_hard>'))
    )

def pc_miss():
    return (
        'The slippery <!monster_name> evaded <!pc_name>\'s hit. '
    )

def monster_stunned():
    return random.choice([
            'The monster was stunned by the attack. '
    ])

def monster_passing():
    return (
        random.choice([
            'The <!monster_name> leans low, ready to strike with its might. '
        ])
    )

def monster_struck_soft():
    return (
        random.choice([
            'The <!monster_name> took a glancing blow. ',
            'Although <pc_name>\'s hit landed, <!monster_name> is mostly unphased'
        ])
    )

def monster_struck_med():
    return random.choice([
        'The <!monster_name> was struck by the blow! ',
        'A sharp crack was heard as the strike left its mark. ',
        'That blow seemed like it could break some bones. ',
        'The attack from <pc_name> surely left a impression. '
    ])

def monster_struck_hard():
    return random.choice([
        'The <!monster_name> was staggered by the immense force. ',
        '<pc_name:sentence> landed a massive hit on <!monster_name>! ',
        'The shattering blow from <pc_name> rumbled through the ground. '
    ])

def monster_hit():
    return random.choice([
        '<!pc_name> reeled back in pain. ',
        '<pc_name:sentence> stunbles backward, gasping for breath. ',
        '<pc_name:sentence> winces from the pain but continues fighting. '
    ])

def monster_miss():
    return random.choice([
        'The <negative_trait> <!monster_name> failed to land its hit. ',
        '<pc_name:sentence> jumps out of the way. ',
        '<pc_name:sentence> blocks the strike with his <!pc_weapon>. ',
        'The fierce blow from the monster narrowly misses <pc_name>. '
    ])

def monster_dead():
    return random.choice([
        '<pc_name:sentence> was victorious! The <!monster_name> menaced for no longer! \n\n',
        '<!pc_name> says\n\n"That didn\'t seem so hard, I don\'t know what <!armor_name> was talking about."\n\n'
    ])

with open('../monsters.json', 'r') as monster_file:
    monsters_list = json.load(monster_file)
