from poker_stepz import MasterGame
import torch
import numpy as np 
from færdig_AI_model import q_net
import matplotlib.pyplot as plt
#from ddqn import DDQN


env = MasterGame()
wins = 0
losses = 0
tie = 0
done = False
actions = np.array([-1,0,1])
bet_fold_action = np.array([-1,1])
bet_check_action = np.array([0,1])

master_list = []

#model = DDQN(105, 3)

# Play episode    
def state_to_input(state):
    state = torch.tensor(state, dtype=torch.float)
    return (state)

for s in range(12):
    #model.load_state_dict(torch.load(f'q-nets-ddqn/q_net-{18}.pt'))
    q_net.load_state_dict(torch.load(f'q-nets-dqn/q_net-{s}.pt'))
    cumulative_reward = 0
    wins = 0
    losses = 0
    games_wanted = 100
    games_count = 0
    while games_wanted > games_count:

        done = False 
        env_observation = env.reset()  
        observation = state_to_input(env_observation)
        #print(observation)
        with torch.no_grad():   
            while (not done):

                # Choose action and step environment
                if observation[-1] == 0:
                    #action = np.argmax(model.forward(observation).detach().numpy())
                    action = np.argmax(q_net(observation).detach().numpy())
                    if actions[action] not in bet_check_action:
                        #min_action = np.argmin(model.forward(observation).detach().numpy())
                        min_action = np.argmin(q_net(observation).detach().numpy())
                        
                    
                        for i in range(3):
                            if i != action and i != min_action:
                                middle_action = i
                        action = middle_action
                else:
                    #ction = np.argmax(q_net(observation).detach().numpy())
                    #action = np.argmax(model.forward(observation).detach().numpy())
                    if actions[action] not in bet_fold_action:
                        #min_action = np.argmin(model.forward(observation).detach().numpy())
                        min_action = np.argmin(q_net(observation).detach().numpy())
                        #print(f'Max action: {action}, min action: {min_action}')
                    
                        for i in range(3):
                            if i != action and i != min_action:
                                middle_action = i
                        action = middle_action
                        #print(f'i: {i}, action: {actions[i]}')


                next_observation, reward, done = env.step(actions[action])
                observation = state_to_input(next_observation)


                cumulative_reward += reward
                if cumulative_reward >= 25:
                    wins += 1
                    games_count += 1
                    cumulative_reward = 0
                elif cumulative_reward <= -25:
                    losses += 1
                    games_count += 1
                    cumulative_reward = 0


    print(f'{s}: losses: {losses}, wins: {wins}, win rate: {wins/(losses+wins)}, cumulative reward: {cumulative_reward}')

    """# creating the dataset
    data = {'Wins':wins, 'Losses':losses}
    courses = list(data.keys())
    values = list(data.values())
    
    fig = plt.figure(figsize = (10, 5))
    
    # creating the bar plot
    plt.bar(courses, values, color ='maroon', 
            width = 0.4)
    

    plt.ylabel("Number of Wins or Losses")
    plt.title(f"Wins or Losses out of {games_wanted} games")
    #plt.show()
    plt.savefig(f'Barplot-{s}')"""

    '''#master_list.append((wins,losses))

classes = ('Q_net 1', 'Q_net 2', 'Q_net 3', 'Q_net 4', 'Q_net 5', 'Q_net 6')
data = {'Wins': (master_list[0][0], master_list[1][0], master_list[2][0], master_list[3][0], master_list[4][0], master_list[5][0]),
        'Losses': (master_list[0][1], master_list[1][1], master_list[2][1], master_list[3][1], master_list[4][1], master_list[5][1])}
x = np.arange(len(classes))
width = 0.25
multiplier = 0
fig, ax = plt.subplots(layout = 'constrained')
for attribute, games in data.items():
    offset = width*multiplier
    rects = ax.bar(x + offset, games, width, label = attribute)
    ax.bar_label(rects, padding =3)
    multiplier += 1
ax.set_ylabel('Wins and losses')
ax.set_title('DDQN')
ax.set_xticks(x + width, classes)
ax.legend(loc='upper left', ncols=3)
ax.set_ylim(0, 1750)

plt.show()'''
