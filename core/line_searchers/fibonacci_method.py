from utils import (
    ILineSearch, OptimizationResult, SolutionStatus
)
from typing import Callable, Tuple, List


class FibonacciMethod(ILineSearch):
    """Implementation of fibonacci method for single-variable optimization"""
    def search(self, phi: Callable[[float], float],
        interval: tuple[float, float], epsilon: float) -> float:
        """
        Minimizes the function φ(λ) on a given interval using
        the Fibonacci search algorithm.
        Args:
            phi (Callable[[float], float]): One-dimensional objective function φ(λ).
            interval (tuple[float, float]): Initial uncertainty interval (a, b).
            epsilon (float): Required final interval length.
        Returns:
            float: Approximate minimizer λ of φ(λ).
        """
        a, b = interval
        L = b - a
        FIB, N = self._calculate_N_fibonacci(L, epsilon)

        iterations = 0

        x1 = b - FIB[N - 1] / FIB[N] * L
        x2 = a + FIB[N - 1] / FIB[N] * L
        f1 = phi(x1)
        f2 = phi(x2)

        while N > 3:
            if f1 < f2:
                b = x2
                x2 = x1
                f2 = f1
                L = b - a
                x1 = b - FIB[N - 2] / FIB[N - 1] * L
                f1 = phi(x1)
            else:
                a = x1
                x1 = x2
                f1 = f2
                L = b - a
                x2 = a + FIB[N - 2] / FIB[N - 1] * L
                f2 = phi(x2)

            N -= 1
            iterations += 1

        # N == 3
        x_min = (x1 + x2) / 2
        value = phi(x_min)

        return OptimizationResult(
            x_min=x_min,
            value=value,
            iterations=iterations,
            final_epsilon=b - a,
            status=SolutionStatus.OPTIMAL.value
        )
    
    def _calculate_N_fibonacci(self, L: float, epsilon: float = 0.001) -> Tuple[List[int], int]:
        """
        Calculate first N fibonacci numbers.
        Args:
            L (float): the length of the interval (a, b)
            epsilon (float): desired method pricision.
        Returns:
            Tuple: (List of the first N Fibonacci numbers,
                    Number of Fibonacci nambers)
        """
        fib = [1, 1]
        while fib[-1] < L / epsilon:
            fib.append(fib[-1] + fib[-2])
        N = len(fib) - 1
        return fib, N