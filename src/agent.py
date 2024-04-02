import tensorflow as tf

class Agent:

    def __init__(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(units=1, activation='relu', input_shape=[2]),
            tf.keras.layers.Dense(units=1)
        ])
        self.model.summary()

    def runPolicy(self, state):
        return [state[0] < state[1] / 2]