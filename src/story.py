import util

def run():
    protaganist_name = util.name()
    wiz_name = util.name()
    town_name = util.town()

    print(util.expand(
        util.town_intro(),
        pc_name = protaganist_name,
        wiz_name = wiz_name,
        armor_name = util.name()
    ))