from typing import Callable, Optional, List
from dataclasses import dataclass
import numpy as np

@dataclass
class OptimizationProblem:
    obj_func: Callable[[np.ndarray], float]
    grad_func: Callable[[np.ndarray], np.ndarray]
    hess_func: Callable[[np.ndarray], np.ndarray]
    
    epsilon: float
    method_name: str
    x_0: np.ndarray 
    max_iter: int = 1000

@dataclass
class OptimizationResult:
    x_min: Optional[np.ndarray]
    value: Optional[float]
    iterations: Optional[int]
    final_epsilon: Optional[float]
    trajectory: List[np.ndarray]
    status: str = 'optimal'