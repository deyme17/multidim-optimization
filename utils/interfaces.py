from abc import ABC, abstractmethod
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