import gym
import random
import numpy as np
import time
from collections import deque
import pickle
from collections import defaultdict


EPISODES =  20000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999


def default_Q_value():
    return 0

if __name__ == "__main__":

    random.seed(1)
    np.random.seed(1)
    env = gym.envs.make("FrozenLake-v1")
    env.seed(1)
    env.action_space.np_random.seed(1)

    # Update the Q_table for the iteration
    Q_table = defaultdict(default_Q_value) # starts with a pessimistic estimate of zero reward for each state.
    episode_reward_record = deque(maxlen=100)

    for i in range(EPISODES):
        episode_reward = 0
        done = False
        obs = env.reset()

        ##########################################################
        # Q LEARNING ALGORITHM

        while not done:
            # Epsilon-greedy policy
            if random.uniform(0, 1) < EPSILON:
                action = env.action_space.sample() # Exploratory paths
            else:
                # Exploitative action based on Q-table
                action = np.argmax([Q_table[(obs, a)] for a in range(env.action_space.n)])
            
            # Perfrom the action
            new_obs, reward, done, _ = env.step(action)

            # Q-learning update
            old_value = Q_table[(obs, action)]
            future_max = np.max([Q_table[(new_obs, a)] for a in range(env.action_space.n)])

            # Update rule for Q-learning 
            if not done:
                Q_table[(obs, action)] = (1 - LEARNING_RATE) * old_value + LEARNING_RATE * (reward + DISCOUNT_FACTOR * future_max)
            else:
                Q_table[(obs, action)] = (1 - LEARNING_RATE) * old_value + LEARNING_RATE * reward
            
            obs = new_obs
            episode_reward += reward

        # Decrement EPSILON
        EPSILON *= EPSILON_DECAY

        ##########################################################

        # record the reward for this episode
        episode_reward_record.append(episode_reward) 
     
        if i % 100 == 0 and i > 0:
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record))/100))
            print("EPSILON: " + str(EPSILON) )
    
    model_file = open('Q_TABLE.pkl' ,'wb')
    pickle.dump([Q_table,EPSILON],model_file)
    model_file.close()
