import util

def chapter(args):
    args.update({
        'armor_name': util.name(),
        'town_name': util.town(),
        'monster_name': util.monster_name()
    })

    result = ''

    result += util.expand(util.chapter_title(), **args)
    result += util.expand(util.town_intro(), **args)
    result += util.expand(util.armory_intro(), **args)

    descriptions = util.monster_description(args['monster_name'])
    for description in descriptions:
        args['description'] = description
        result += util.expand(util.armory_explanation(), **args)
        result += util.expand(util.armory_more(), **args)

    result += util.expand(util.armory_no_more(), **args)
    return result

def book():
    args = {
        'pc_name': util.name(),
        'wiz_name': util.name(),
    }

    result = util.expand(util.book_title(), **args)
    word_count = len(result.split(' '))

    chapter_number = 1
    while word_count < 50000:
        args['chapter_number'] = str(chapter_number)
        chapter_text = chapter(args)
        word_count += len(chapter_text.split(' '))
        result += chapter_text
        chapter_number += 1

    return result

print(book())