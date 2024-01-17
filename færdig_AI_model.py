import torch
import numpy as np
import matplotlib.pyplot as plt

from poker_stepz import MasterGame

input_dimension = 105
hidden_dimension = 512
output_dimension = 3

q_net = torch.nn.Sequential(
        torch.nn.Linear(input_dimension, hidden_dimension),
        torch.nn.ReLU(),
        torch.nn.Linear(hidden_dimension, hidden_dimension),
        torch.nn.ReLU(),
        torch.nn.Linear(hidden_dimension, hidden_dimension),
        torch.nn.ReLU(),
        torch.nn.Linear(hidden_dimension, output_dimension)
        )


n_games = 100_000
epsilon = 1
epsilon_min = 0.01
epsilon_reduction_factor = 0.01**(1/100_000)
gamma = 0.99
batch_size = 256
buffer_size = 50_000
learning_rate = 0.0001
steps_per_gradient_update = 10
max_episode_step = 128

optimizer = torch.optim.Adam(q_net.parameters(), lr=learning_rate)
loss_function = torch.nn.MSELoss()

def reset_weights(layer):
    if isinstance(layer, torch.nn.Linear):
        print('hey')
        torch.nn.init.xavier_uniform_(layer.weight)
        torch.nn.init.constant_(layer.bias, 0)



if __name__=='__main__':

    for s in range(10,12):
        q_net = torch.nn.Sequential(
                torch.nn.Linear(input_dimension, hidden_dimension),
                torch.nn.ReLU(),
                torch.nn.Linear(hidden_dimension, hidden_dimension),
                torch.nn.ReLU(),
                torch.nn.Linear(hidden_dimension, hidden_dimension),
                torch.nn.ReLU(),
                torch.nn.Linear(hidden_dimension, output_dimension)
        )

        epsilon = 1
        def state_to_input(state):
            state = torch.tensor(state, dtype=torch.float)
            return (state)

        env = MasterGame()
        
        q_net.apply(reset_weights)


        actions = np.array([-1,0,1])

        bet_fold_action = np.array([-1,1])
        bet_check_action = np.array([0,1])




        obs_buffer = torch.zeros((buffer_size, input_dimension))
        obs_next_buffer = torch.zeros((buffer_size, input_dimension))
        action_buffer = torch.zeros(buffer_size).long()
        reward_buffer = torch.zeros(buffer_size)
        done_buffer = torch.zeros(buffer_size)

        optimizer = torch.optim.Adam(q_net.parameters(), lr=learning_rate)
        loss_function = torch.nn.MSELoss()


        scores = []
        losses = []
        episode_steps = []
        step_count = 0
        step_count_list = []
        print_interval = 100
        games_played = 0
        cumulative_reward = 0
        cumulative_reward_list = []

    # Training loop
    
  
        games_played = 0
        games_played_list = []
        cumulative_reward = 0
        cumulative_reward_list = []
        for i in range(n_games):
            # Reset game
            
            score = 0
            episode_step = 0
            episode_loss = 0
            episode_gradient_step = 0
            done = False
            env_observation = env.reset()
            observation = state_to_input(env_observation)

            # Reduce exploration rate
            epsilon = (epsilon-epsilon_min)*epsilon_reduction_factor + epsilon_min
            
            # Episode loop
            while (not done):   
                #print(f'epsilon: {epsilon}')    
                # Choose action and step environment
                if np.random.rand() < epsilon:
                    # Random action
                    if observation[-1] == 0:
                        action = np.random.choice(bet_check_action)
                        action += 1
                        #print(f'Bet check action {actions[action]}')
                    else:
                        action = np.random.choice(bet_fold_action)
                        action += 1
                        #print(f'Bet fold action {actions[action]}')

                else:
                    # Action according to policy
                    if observation[-1] == 0:
                        action = np.argmax(q_net(observation).detach().numpy())
                        if actions[action] not in bet_check_action:
                            min_action = np.argmin(q_net(observation).detach().numpy())
                        
                            for i in range(3):
                                if i != action and i != min_action:
                                    middle_action = i
                            action = middle_action
                    else:
                        action = np.argmax(q_net(observation).detach().numpy())
                        if actions[action] not in bet_fold_action:
                            min_action = np.argmin(q_net(observation).detach().numpy())
                            #print(f'Max action: {action}, min action: {min_action}')
                        
                            for i in range(3):
                                if i != action and i != min_action:
                                    middle_action = i
                            action = middle_action
                            #print(f'i: {i}, action: {actions[i]}')



                #print(f'Games played: {games_played}')
                #print(f'Action: {actions[action]}')
                #print(f'Observation: {observation}')
                
                env_observation_next, reward, done = env.step(actions[action])
                #print(f'Reward: {reward}')
                observation_next = state_to_input(env_observation_next)        
                score += reward

                # Store to buffers
                buffer_index = step_count % buffer_size
                obs_buffer[buffer_index] = observation
                obs_next_buffer[buffer_index] = observation_next
                action_buffer[buffer_index] = action
                reward_buffer[buffer_index] = reward
                done_buffer[buffer_index] = done

                # Update to next observation
                observation = observation_next

                # Learn using minibatch from buffer (every )
                if step_count > batch_size and step_count % steps_per_gradient_update == 0:
                    # Choose a minibatch
                    batch_idx = np.random.choice(np.minimum(
                        buffer_size, step_count), size=batch_size, replace=False)

                    # Compute loss function
                    out = q_net(obs_buffer[batch_idx])
                    val = out[np.arange(batch_size), action_buffer[batch_idx]]   # Explain this indexing
                    with torch.no_grad():
                        out_next = q_net(obs_next_buffer[batch_idx])
                        target = reward_buffer[batch_idx] + \
                            gamma*torch.max(out_next, dim=1).values * \
                            (1-done_buffer[batch_idx])
                    loss = loss_function(val, target)

                    # Step the optimizer
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                    episode_gradient_step += 1
                    episode_loss += loss.item()


                # Update step counteres
                episode_step += 1
                
                step_count += 1
                step_count_list.append(step_count)

            if games_played % 1000 == 0:
                print(f'Games played: {games_played}')
            cumulative_reward += reward
            cumulative_reward_list.append(cumulative_reward)

            games_played += 1
            games_played_list.append(games_played)
            
        
        torch.save(q_net.state_dict(),f'q-nets-dqn/q_net-{s}.pt')

        plt.plot(games_played_list, cumulative_reward_list)
        plt.title(f'Neurons: {hidden_dimension}, BS: {batch_size}, Games: {n_games}')
        plt.xlabel('Games Played')
        plt.ylabel('Cumulative Reward')
        plt.grid(True)
        plt.savefig(f'plots-dqn/cumulative-reward-{s}')


