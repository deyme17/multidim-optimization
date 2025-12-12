from utils import (
    IOptimizer, ILineSearch, SolutionStatus,
    OptimizationProblem, OptimizationResult
)
import numpy as np


class SteepestDescent(IOptimizer):
    """
    Steepest descent optimization method.
    """
    def __init__(self, line_searcher: ILineSearch) -> None:
        """
        Initialize SteepestDescent.
        Args:
            line_searcher (ILineSearch):
                Line search strategy used to compute the step size lambda.
        """
        self.line_searcher = line_searcher

    def optimize(self, problem: OptimizationProblem) -> OptimizationResult:
        """
        Finds a local minimum of a multivariate objective function.
        Args:
            problem (OptimizationProblem):
                Optimization problem definition containing the objective function, 
                its gradient, initial point, precision and stopping criteria.
        Returns:
            OptimizationResult:
                Result of the optimization process, including the approximated minimizer, 
                function value and convergence information.
        """
        if problem is None:
            return OptimizationResult(
                status=SolutionStatus.ERROR.value
        )
        obj_func = problem.obj_func
        grad_func = problem.grad_func
        eps = problem.epsilon
        max_iter = problem.max_iter

        x = problem.x_0.copy()
        grad = grad_func(x)
        grad_norm = np.linalg.norm(grad)

        trajectory = [x.copy()]
        iter_count = 0

        while grad_norm > eps:
            if iter_count > max_iter:
                return OptimizationResult(
                    x_min=x,
                    value=obj_func(x),
                    iterations=iter_count,
                    final_epsilon=np.linalg.norm(grad_func(x)),
                    trajectory=trajectory,
                    status=SolutionStatus.MAX_ITERATIONS.value
                )
            # find optimal lambda
            def phi(lmbda: float) -> float:
                return obj_func(x - lmbda * grad)
            
            lmbda = self.line_searcher.search(
                phi=phi,
                interval=(0.0, 1.0),
                epsilon=eps
            )
            # update x
            x = x - lmbda * grad
            grad = grad_func(x)
            grad_norm = np.linalg.norm(grad)

            trajectory.append(x.copy())
            iter_count += 1

        return OptimizationResult(
            x_min=x,
            value=obj_func(x),
            iterations=iter_count,
            final_epsilon=np.linalg.norm(grad_func(x)),
            trajectory=trajectory,
            status=SolutionStatus.OPTIMAL.value
        )