from utils import IOptimizer

from .newton_method import NewtonMethod
from .steepest_descent import SteepestDescent

optimizers: dict[str, IOptimizer] = {
    "Steepest Descent method": SteepestDescent(),
    "Newton method": NewtonMethod()
}