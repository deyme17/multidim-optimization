from utils import (
    IOptimizer, ILineSearch, 
    OptimizationProblem, OptimizationResult
)


class SteepestDescent(IOptimizer):
    """
    Steepest descent optimization method.
    """
    def optimize(self, problem: OptimizationProblem, line_searcher: ILineSearch) -> OptimizationResult:
        """
        Finds a local minimum of a multivariate objective function.
        Args:
            problem (OptimizationProblem):
                Optimization problem definition containing the objective function, 
                its gradient, initial point, precision and stopping criteria.
            line_searcher (ILineSearch):
                Line search strategy used to compute the step size lambda.
        Returns:
            OptimizationResult:
                Result of the optimization process, including the approximated minimizer, 
                function value and convergence information.
        """
        ... # TODO
        return OptimizationResult(

        )