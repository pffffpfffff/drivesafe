from ReplayBuffer import *
from DQNagent import *
from main import *




def get_experience(env, agent, RPbuffer):
    for car in env.cars:
        state =car.state
        action = agent.choose_action(state)
        reward, state_, = car.feedback, car.info()
        RPbuffer.store(state,action,reward,state_)
        state = state_
    
def train_model(max_episode=200):
    agent  = DQNagent()
    RPbuffer = ReplayBuffer(10)
    env = game()
    for i in range(100):
        get_experience(env,agent,RPbuffer)
    for episode in range(max_episode):
        get_experience(env,agent,RPbuffer)
        experience_batch = RPbuffer.sample()
        loss = agent.train(experience_batch)
        print(loss)

train_model()
