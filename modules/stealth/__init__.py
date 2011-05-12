import ConfigParser
import StringIO
import models
import logging


def importData(user, string):
    config = ConfigParser.RawConfigParser()
    config.readfp(StringIO.StringIO(string))
    charName = config.get('Stats','name')
    logging.debug(charName)

    char = models.Char.get_or_insert(str(user.key())+charName, owner=user)
    charStats = models.CharStats.get_or_insert(char.key().name(), char=char)

    statOptions = config.options('Stats')
    for option in statOptions:
        value = config.get('Stats',option)
        setattr(charStats, option, value)

    charStats.put()
    char.name = charStats.name
    char.put()

    skills= char.skills.fetch(1000)
    skillNames= config.options('Skills')
    for skillOpt in skillNames:
        skillVal = config.get('Skills', skillOpt)
        skillVal = float(skillVal.replace(',','.'))
        skillIncrease = float(config.get('SkillsIncrease',skillOpt).replace(',','.'))
        skillFound = False
        for skill in skills:
            if skill.name == skillOpt:
                skillFound = True
                changed = False
                if skill.current != skillVal:
                    changed = True
                skill.current = skillVal
                skill.increased = skillIncrease
                if changed:
                    skill.put()

        if not skillFound:
            skill = models.Skill(char=char,name=skillOpt,current=skillVal,increased=skillIncrease)
            skill.put();

    if 'Journal' not in config.sections():
        return

    journal = models.CharJournal.get_or_insert(char.key().name(), char=char)
    lineNums = config.options('Journal')
    for ln in lineNums:
        journal.lines.append(config.get('Journal',ln))

    if len(lineNums) > 0:
        while len(journal.lines) > 150:
            journal.lines.pop()
        journal.put()





    