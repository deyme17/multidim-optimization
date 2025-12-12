from abc import ABC, abstractmethod
from typing import Callable
from .containers import OptimizationProblem, OptimizationResult

class IOptimizer(ABC):
    """Interface for Multidimensional Optimization."""
    @abstractmethod
    def optimize(self, problem: OptimizationProblem) -> OptimizationResult:
        """
        Finds the minimum function.
        Args:
            problem (OptimizationProblem): An object containing the function, gradient, Hessian
            and initial parameters.
        Returns:
            OptimizationResult: A result with the found vector x_min and other statistics.
        """
        pass

class ILineSearch(ABC):
    """
    Interface for one-dimensional line search methods.
    """
    @abstractmethod
    def search(self, phi: Callable[[float], float],
        interval: tuple[float, float], epsilon: float) -> float:
        """
        Finds an approximate minimizer of a scalar function on a given interval.
        Args:
            phi (Callable[[float], float]): One-dimensional objective function φ(λ).
            interval (tuple[float, float]): Initial uncertainty interval (a, b) for λ.
            epsilon (float): Desired precision of the line search.
        Returns:
            float: Approximate value of λ that minimizes φ(λ).
        """
        pass