from utils import IOptimizer

from .newton_method import NewtonMethod
from .steepest_descent import SteepestDescent

from .line_searchers import FibonacciMethod

optimizers: dict[str, IOptimizer] = {
    "Steepest Descent method": SteepestDescent(FibonacciMethod()),
    "Newton method": NewtonMethod()
}