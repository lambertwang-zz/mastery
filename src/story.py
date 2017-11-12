import util
import combat

TARGET_WORD_COUNT = 50000

def chapter(args):
    args.update({
        'armor_name': util.name(),
        'town_name': util.town(),
        'monster_name': util.monster_name(),
        'pc_weapon': 'sword'
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
    result += util.expand(combat.combat_intro(args['monster_name']), **args)
    result += util.expand(combat.combat(), **args)
    return result

chapter_number = 1
def book():
    args = {
        'pc_name': util.name(),
        'wiz_name': util.name(),
    }

    result = util.expand(util.book_title(), **args)
    word_count = len(result.split(' '))

    global chapter_number
    global TARGET_WORD_COUNT
    while word_count < TARGET_WORD_COUNT:
        args['chapter_number'] = str(chapter_number)
        chapter_text = chapter(args)
        word_count += len(chapter_text.split(' '))
        result += chapter_text
        chapter_number += 1

    return result

def toc():
    result = ''
    for i in range(1, chapter_number + 1):
        result += '[Chapter ' + str(i) + '](#chapter' + str(i) + ')\n\n'

    return result


book_text = book()

print(toc())
print(book_text)