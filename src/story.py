import util

def chapter():
    args = {
        'pc_name': util.name(),
        'wiz_name': util.name(),
        'town_name': util.town(),
        'armor_name': util.name(),
        'monster_name': util.monster_name()
    }    
    result = ''

    result += util.expand(util.town_intro(), **args)
    result += util.expand(util.armory_intro(), **args)

    descriptions = util.monster_description(args['monster_name'])
    for description in descriptions:
        args['description'] = description
        result += util.expand(util.armory_explanation(), **args)
        result += util.expand(util.armory_more(), **args)

    result += util.expand(util.armory_no_more(), **args)
    return result

print(chapter())