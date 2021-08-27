import numpy as np
import random
import copy


def main():
    global actions
    global positions
    global alpha
    global gamma
    global curr_rewards

    # UP, DOWN, LEFT, RIGHT
    actions = ["U", "D", "L", "R"]
    q_table = np.zeros((11,4))
    q_table[8] = np.array([0.2]*4)
    q_table[9] = np.array([-1.0]*4)
    q_table[10] = np.array([1.0]*4)

    # taxa de aprendizagem
    alpha = 0.5
    # fator de desconto
    gamma = 0.8

    # Estado inicial: (1,1)
    # Estados finais: (4,3) - win; (4,2) - lose e (4,1) - also win
    positions = [(1,1), (1,2), (1,3), (2,1), (2,3), (3,1), (3,2), (3,3), (4,1), (4,2), (4,3)]

    r1 = -0.4
    r2 = -0.04
    rewards_1 = {}
    rewards_2 = {}

    set_rewards(rewards_1, r1)
    set_rewards(rewards_2, r2)

    n_explorations = 10000

    # exploração pra r = -0.4
    curr_rewards = rewards_1
    explored_q_r1 = explore(n_explorations, copy.deepcopy(q_table))
    policies = make_policy(explored_q_r1)
    print("Politicas para r = -0.4:")
    print_policy(policies)
    print()

    # exploração pra r = -0.04
    curr_rewards = rewards_2
    explored_q_r2 = explore(n_explorations, copy.deepcopy(q_table))
    policies = make_policy(explored_q_r2)
    print("Politicas para r = -0.04:")
    print_policy(policies)
    print()
    

def set_rewards(rewards, r):
    for pos in positions:
        rewards.update({pos : r})
    rewards[(4,3)] = 1.0
    rewards[(4,2)] = -1.0
    rewards[(4,1)] = 0.2


def explore(n_explorations, q_table):
    # Começar explorações
    for _ in range(n_explorations):
        #print("Exploração: ", i)
        # Começar do estado inicial
        curr_state = positions[0]
        non_terminal_state = True

        while (non_terminal_state):
            # Escolher ação
            action = choose_random_action()
            # Pegar o estado resultante com base na ação escolhida
            next_state = move(curr_state, action)

            #print(curr_state, action, next_state)
            update_q_table(q_table,curr_state,action,next_state)

            # Tornar proximo estado, estado atual
            curr_state = next_state
            # Se for (4,2) ou (4,3) chegou a um estado terminal
            if curr_state in [positions[8], positions[9], positions[10]]:
                non_terminal_state = False
                
    print("Tabela Q após explorações")
    print(q_table)
    return q_table


def print_policy(policies):
    policies = np.transpose(policies)
    policies = np.flip(policies, axis=0)
    for line in policies:
        print(line)


def make_policy(explored_q):
    policy = [[" "," ",""],[" "," "," "],[" "," "," "],[" "," "," "]]
    for pos in positions:
        best_action = get_policy_4_state(explored_q, pos)
        policy[pos[0]-1][pos[1]-1] = best_action

    policy[3][2] = "+1"
    policy[3][1] = "-1"
    policy[3][0] = "0.2"
    return policy

    
def get_policy_4_state(explored_q, state):
    state_index = positions.index(state)
    best_action_index = np.argmax(explored_q[state_index])
    return actions[best_action_index]


def choose_random_action():
    choice = random.choice(range(4))
    return actions[choice]


def move(curr_state, action):
    next_state = copy.deepcopy(curr_state)
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
        next_state=curr_state

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
    
    random.shuffle(action_roulette)
    return random.choice(action_roulette)


def update_q_table(q_table, curr_state, action, next_state):
    # Obtendo indices para acessar a tabela Q
    curr_state_index = positions.index(curr_state)
    next_state_index = positions.index(next_state)
    action_index = actions.index(action)

    # Estimativa de Q(s,a) pela Equação de Belman
    estimate = curr_rewards[curr_state] + gamma * max(q_table[next_state_index])
    
    # Equação de atualização
    q_table[curr_state_index][action_index] += alpha*(estimate - q_table[curr_state_index][action_index])


if __name__ == "__main__":
    main()