from random import random
from typing import Callable, Optional, Union, List
from easyAI.clsstools.Verifiers import verify_type, verify_components_type, verify_len
from easyAI.core.objects import Neuron, Model, Layer
from easyAI.core.activations import activation_map


class Perceptron(Neuron):
    "Class representing a Perceptron (Unitary Layer Neural DL Model)"

    def __init__(self, entries: int) -> None:
        """
        Builds an instance give X training data, y training data and entries.

        Args:
            - entries (int): The number of inputs of the model.
        """
        super().__init__()

        # Compatibility with int expressed in float
        if isinstance(entries, float):
            if int(entries) == entries:
                entries = int(entries)

        del self._inputnodes
        del self._inputs
        del self._z

        # Model params
        self._n: int = verify_type(entries, int) # Number of entries
        self._lr: float = 0.1
        self._weights: List[float] = [random() for _ in range(self._n)]
        self._activation: Callable = activation_map["step"]

    def __call__(self, X: List[Union[int, float]]) -> float:
        return self.predict(X)

    @property
    def id(self) -> int:
        """The id property."""
        return self._identifier

    @property
    def b(self) -> float:
        """The bias property."""
        return self._bias

    @b.setter
    def b(self, value) -> None:
        self._bias = verify_type(value, (int, float))

    @property
    def w(self) -> List[float]:
        """The w property."""
        return self._weights

    @w.setter
    def w(self, value) -> None:
        self._w = float(verify_type(value, (int, float)))

    @property
    def learning_rate(self) -> float:
        """The learning_rate property."""
        return self._lr

    @learning_rate.setter
    def learning_rate(self, value) -> None:
        self._lr = float(verify_type(value, (int, float)))

    def fit(
        self,
        X: List[Union[int, float]],
        y: List[Union[int, float]],
        verbose: Optional[bool] = False,
    ) -> List[Union[int, float]]:
        """
        Trains the model following the Perceptron Learning Rule.

        Returns:
            - list: The history loss.
        """

        # Verify type of X and y, and verbose option
        X = verify_components_type(verify_type(X, (list)), (int, float))

        y = verify_components_type(verify_type(y, list), (int, float))

        verify_type(verbose, bool)

        # Verifing data sizes compatibility
        if len(X) % self._n != 0:
            print("[!] Warning, X size and y size doesn't correspond.")

        if len(X) < self._n:
            return []

        # Training
        history: list = []

        for epoch in range(len(y)):
            # Narrowing down y for X
            eX = X[epoch * self._n : (epoch + 1) * self._n]
            ey = y[epoch]

            z = self.__call__(eX)

            # Updating parameters
            if z != ey:
                for i in range(len(self._weights)):
                    self._weights[i] += self._lr * (ey - z) * eX[i]
                self._bias += self._lr * (ey - z)

            # Calculate loss MSE for the current epoch
            epoch_loss = sum(
                (y[i] - self.__call__(X[i * self._n : (i + 1) * self._n])) ** 2
                for i in range(len(y))
            ) / len(y)
            history.append(epoch_loss)

            if verbose:
                print(
                    f"Epoch {epoch}:\n\tModel output: {z}\n\tExpected output: {ey}\n\tLoss: {epoch_loss}"
                )

        return history

    def predict(self, X: List[Union[int, float]]) -> float:
        """Returns a prediction given X as inputs."""
        verify_len(X, self._n)  # The input must be the same shape as n.
        verify_components_type(X, (int, float))  # Input data must be numeric.

        return self.activation(
            sum([x * w for x, w in zip(X, self._weights)]) + self._bias
        )



class MLP(Model):

    def __init__(self, structure: List[Layer]) -> None:
        super().__init__(structure)