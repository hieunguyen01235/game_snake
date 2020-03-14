from snake_env import SnakeEnv
import numpy as np
import time
env = SnakeEnv()
env.reset()
env.render()
array_action =[1,-1,2,-2]
for each_game in range(10):
    print("-------------------------------Game: ", each_game)
    reward = 0
    for step_index in range(10000):
        action =array_action[np.random.randint(4)]
        state, rew, done, _ = env.step(action)
        print("Action:", action)
        print("State", state)
        print("Reward: ", rew)
        print("Done: ", done)
        env.render()
        time.sleep(100.0 / 1000.0)
        if done:
            # time.sleep(10000.0 / 1000.0)
            break
    if reward ==1:
        break
    env.reset()
