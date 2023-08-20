from mycroft import MycroftSkill, intent_file_handler


class FormulaOne(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('one.formula.intent')
    def handle_one_formula(self, message):
        self.speak_dialog('one.formula')


def create_skill():
    return FormulaOne()

