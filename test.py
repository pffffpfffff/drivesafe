import tensorflow as tf
import numpy as np

state = np.array([int(x) for x in format(42301,'05')])
print(state)
state = tf.convert_to_tensor(state[None,:], dtype = tf.float32)
print(state)

for i in range(10):
    act = np.random.randint(0,4)
    print(act)
