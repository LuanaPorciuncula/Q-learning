import numpy as np
import random
import copy


def main():
    global actions
    global positions

    # UP, DOWN, LEFT, RIGHT
    actions = ["U", "D", "L", "R"]
    q_table = np.zeros((11,4))

    # taxa de aprendizagem
    alpha = 0.5
    # fator de desconto
    gamma = 0.8

    # Estado inicial: (1,1)
    # Estados finais: (4,3) - win; (4,2) - lose
    positions = [(1,1), (1,2), (1,3), (2,1), (2,3), (3,1), (3,2), (3,3), (4,1), (4,2), (4,3)]

    r_1 = -0.4
    r_2 = -0.04
    rewards_1 = {}
    rewards_2 = {}

    set_rewards(rewards_1, r_1)
    set_rewards(rewards_2, r_2)

    
    

def set_rewards(rewards, r):
    for pos in positions:
        rewards.update({pos : r})
    rewards[(4,3)] = 1.0
    rewards[(4,2)] = -1.0
    rewards[(4,1)] = 0.2


def choose_random_action():
    choice = random.choice(range(4))
    return actions[choice]


def move(curr_state, action):
    next_state = curr_state
    actual_action = get_actual_action(action)

    if actual_action == "U":
        # Se pode subir, sobe. Senão, fica
        next_y = min(curr_state[1]+1,3)
        next_state = (curr_state[0], next_y)
    elif actual_action == "D":
        # Se pode descer, desce. Senão, fica
        next_y = max(curr_state[1]-1,1)
        next_state = (curr_state[0], next_y)
    elif actual_action == "L":
        # Se pode ir p esquerda, vai. Senão, fica
        next_x = max(curr_state[0]-1,1)
        next_state = (next_x, curr_state[1])
    elif actual_action == "R":
        # Se pode ir p direita, vai. Senão, fica
        next_x = min(curr_state[0]+1,4)
        next_state = (next_x, curr_state[1])

    if next_state == (2,2):
        # Se moveu pra (2,2) volta pro lugar
        next_state==curr_state

    return next_state


def get_actual_action(action):
    # 0.8 chance actual action == action
    # 0.1 chance actual action == ir para esquerda de action
    # 0.1 chance actual action == ir para direita de action
    action_roulette = []
    if action == "U":
        action_roulette = ["U"]*8 + ["L"] + ["R"]
    elif action == "D":
        action_roulette = ["D"]*8 + ["R"] + ["L"]
    elif action == "L":
        action_roulette = ["L"]*8 + ["D"] + ["U"]
    elif action == "R":
        action_roulette = ["R"]*8 + ["U"] + ["D"]
    
    return random.choice(action_roulette)

if __name__ == "__main__":
    main()