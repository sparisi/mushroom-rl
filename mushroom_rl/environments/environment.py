import numpy as np

from mushroom_rl.core import Serializable


class MDPInfo(Serializable):
    """
    This class is used to store the information of the environment.

    """
    def __init__(self, observation_space, action_space, gamma, horizon):
        """
        Constructor.

        Args:
             observation_space ([Box, Discrete]): the state space;
             action_space ([Box, Discrete]): the action space;
             gamma (float): the discount factor;
             horizon (int): the horizon.

        """
        self.observation_space = observation_space
        self.action_space = action_space
        self.gamma = gamma
        self.horizon = horizon

        self._add_save_attr(
            observation_space='mushroom',
            action_space='mushroom',
            gamma='primitive',
            horizon='primitive'
        )

    @property
    def size(self):
        """
        Returns:
            The sum of the number of discrete states and discrete actions. Only
            works for discrete spaces.

        """
        return self.observation_space.size + self.action_space.size

    @property
    def shape(self):
        """
        Returns:
            The concatenation of the shape tuple of the state and action
            spaces.

        """
        return self.observation_space.shape + self.action_space.shape


class Environment(object):
    """
    Basic interface used by any mushroom environment.

    """

    @classmethod
    def register(cls):
        """
        Register an environment in the environment list.

        """
        env_name = cls.__name__

        if env_name not in Environment._registered_envs:
            Environment._registered_envs[env_name] = cls

    @staticmethod
    def list_registered():
        """
        List registered environments.

        Returns:
             The list of the registered environments.

        """
        return list(Environment._registered_envs.keys())

    @staticmethod
    def create(env_name, *args, **kwargs):
        """
        Construct an environment given an environment name and parameters.

        Args:
            env_name (str): Name of the environment,
            *args: positional arguments to be provided to the environment constructor
            **kwargs: keyword arguments to be provided to the environment constructor.

        Returns:
            An instance of the constructed environment.

        """
        env = Environment._registered_envs[env_name]

        return env(*args, **kwargs)

    @staticmethod
    def generate(env_name, *args, **kwargs):
        """
        Generate an environment given an environment name and parameters. Differently from
        the create method, it creates the environment calling the generate method, not the init.
        The generate method has simpler interface than the constructor, making easier to generate
        standard verison of the environment.

        Args:
            env_name (str): Name of the environment,
            *args: positional arguments to be provided to the environment generator;
            **kwargs: keyword arguments to be provided to the environment generator.

        Returns:
            An instance of the constructed environment.

        """
        env = Environment._registered_envs[env_name]

        assert hasattr(env, 'generate')

        return env.generate(*args, **kwargs)

    def __init__(self, mdp_info):
        """
        Constructor.

        Args:
             mdp_info (MDPInfo): an object containing the info of the
                environment.

        """
        self._mdp_info = mdp_info

    def seed(self, seed):
        """
        Set the seed of the environment.

        Args:
            seed (float): the value of the seed.

        """
        if hasattr(self, 'env'):
            self.env.seed(seed)
        else:
            raise NotImplementedError

    def reset(self, state=None):
        """
        Reset the current state.

        Args:
            state (np.ndarray, None): the state to set to the current state.

        Returns:
            The current state.

        """
        raise NotImplementedError

    def step(self, action):
        """
        Move the agent from its current state according to the action.

        Args:
            action (np.ndarray): the action to execute.

        Returns:
            The state reached by the agent executing ``action`` in its current
            state, the reward obtained in the transition and a flag to signal
            if the next state is absorbing. Also an additional dictionary is
            returned (possibly empty).

        """
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def stop(self):
        """
        Method used to stop an mdp. Useful when dealing with real world
        environments, simulators, or when using openai-gym rendering

        """
        pass

    @property
    def info(self):
        """
        Returns:
             An object containing the info of the environment.

        """
        return self._mdp_info

    @staticmethod
    def _bound(x, min_value, max_value):
        """
        Method used to bound state and action variables.

        Args:
            x: the variable to bound;
            min_value: the minimum value;
            max_value: the maximum value;

        Returns:
            The bounded variable.

        """
        return np.maximum(min_value, np.minimum(x, max_value))

    _registered_envs = dict()
