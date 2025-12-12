from utils import (
    IOptimizer, SolutionStatus,
    OptimizationProblem, OptimizationResult
)
import numpy as np


class NewtonMethod(IOptimizer):
    """
    Newton optimization method.
    Uses second-order Taylor approximation to find local minimum.
    """
    def optimize(self, problem: OptimizationProblem) -> OptimizationResult:
        """
        Finds a local minimum of a multivariate objective function.
        Args:
            problem (OptimizationProblem):
                Optimization problem definition containing the objective function, 
                its gradient and hessian, initial point, precision and stopping criteria.
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
        hess_func = problem.hess_func
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
            try:
                hess = hess_func(x)
                # update x
                delta_x = np.linalg.solve(hess, -grad) # -H^(-1) * grad_F
                x = x + delta_x
                grad = grad_func(x)
                grad_norm = np.linalg.norm(grad)

                iter_count += 1
                trajectory.append(x.copy())
                
            except Exception as e:
                print(f"[ERROR] {e}")
                return OptimizationResult(
                    x_min=x,
                    value=obj_func(x),
                    iterations=iter_count,
                    final_epsilon=np.linalg.norm(grad),
                    trajectory=trajectory,
                    status=SolutionStatus.ERROR.value
                )
        return OptimizationResult(
            x_min=x,
            value=obj_func(x),
            iterations=iter_count,
            final_epsilon=np.linalg.norm(grad_func(x)),
            trajectory=trajectory,
            status=SolutionStatus.OPTIMAL.value
        )