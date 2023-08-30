from aiogram.fsm.state import State, StatesGroup


class QuestionState(StatesGroup):
    ask_question = State()

class SuggestState(StatesGroup):
    give_suggest = State()