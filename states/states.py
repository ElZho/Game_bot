from aiogram.fsm.state import State, StatesGroup


# create class inheited from StatesGroup, for FSM group of states
class FSMInGame(StatesGroup):
    # states users during the game 
    # waiting of user's move state
    wait_move = State()        
    # wating of users response to the bot's move 
    wait_answer = State()         
