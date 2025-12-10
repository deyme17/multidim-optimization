import math
import numpy as np
from typing import Tuple, List
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QLineEdit, QComboBox, QFormLayout
from PyQt6.QtCore import Qt
from utils import InputWidgetConstants, OptimizationProblem, UIHelper
import warnings


class InputSection(QGroupBox):
    """Widget for multidimensional function optimization input and configuration"""
    def __init__(self, opt_methods_names: List[str]) -> None:
        super().__init__("Optimization Configuration")
        self.opt_methods_names = opt_methods_names
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize the input section UI using Form Layout"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.setSpacing(10)

        # func
        self.func_input = QLineEdit()
        self.func_input.setPlaceholderText("e.g. (1-x[0])**2 + 100*(x[1]-x[0]**2)**2")
        self.func_input.setText(InputWidgetConstants.DEFAULT_FUNC)
        form_layout.addRow(UIHelper.create_label("Objective Function f(x):"), self.func_input)
        
        # optimization method selection
        self.opt_method_combo = QComboBox()
        self.opt_method_combo.addItems(self.opt_methods_names)
        form_layout.addRow(UIHelper.create_label("Optimization Method:"), self.opt_method_combo)
        main_layout.addLayout(form_layout)

        # params
        params_group = QGroupBox("Parameters")
        params_layout = QFormLayout(params_group)
        
        # x0
        self.x0_input = QLineEdit()
        self.x0_input.setPlaceholderText("e.g. -1.2, 1.0")
        self.x0_input.setText(InputWidgetConstants.DEFAULT_X0_STR)
        params_layout.addRow(UIHelper.create_label("Start Point (x₀):"),
                             self.x0_input)
        
        # eps
        self.eps_input = UIHelper.create_double_spinbox(
            0.000001, 1.0,
            InputWidgetConstants.DEFAULT_EPS,
            0.001, decimals=6)
        params_layout.addRow(UIHelper.create_label("Precision (ε):"), self.eps_input)
        
        # max_iter
        self.max_iter_input = UIHelper.create_spinbox(
            10, 100000,
            InputWidgetConstants.DEFAULT_MAX_ITER,
            max_width=120)
        params_layout.addRow(UIHelper.create_label("Max Iterations:"), self.max_iter_input)
        
        main_layout.addWidget(params_group)
        main_layout.addStretch()

    def _parse_vector(self, text: str) -> Tuple[np.ndarray, bool, str]:
        """Parse comma-separated vector from text"""
        try:
            values = [float(x.strip()) for x in text.split(',')]
            if len(values) == 0:
                return None, False, "Vector cannot be empty"
            return np.array(values), True, ""
        except ValueError:
            return None, False, "Invalid vector format. Use comma-separated numbers."

    def _create_numerical_gradient(self, func: callable, h: float = 1e-8) -> callable:
        """Create numerical gradient function"""
        def gradient(x: np.ndarray) -> np.ndarray:
            grad = np.zeros_like(x)
            for i in range(len(x)):
                x_plus = x.copy()
                x_plus[i] += h
                x_minus = x.copy()
                x_minus[i] -= h
                grad[i] = (func(x_plus) - func(x_minus)) / (2 * h)
            return grad
        return gradient

    def _create_numerical_hessian(self, func: callable, h: float = 1e-5) -> callable:
        """Create numerical Hessian function"""
        def hessian(x: np.ndarray) -> np.ndarray:
            n = len(x)
            H = np.zeros((n, n))
            for i in range(n):
                for j in range(n):
                    x_pp = x.copy()
                    x_pp[i] += h
                    x_pp[j] += h
                    
                    x_pm = x.copy()
                    x_pm[i] += h
                    x_pm[j] -= h
                    
                    x_mp = x.copy()
                    x_mp[i] -= h
                    x_mp[j] += h
                    
                    x_mm = x.copy()
                    x_mm[i] -= h
                    x_mm[j] -= h
                    
                    H[i, j] = (func(x_pp) - func(x_pm) - func(x_mp) + func(x_mm)) / (4 * h * h)
            return H
        return hessian

    def get_data(self) -> Tuple[OptimizationProblem, bool, str]:
        """Extract and validate input data."""
        try:
            # validation
            func_str = self.func_input.text().strip()
            if not func_str:
                return None, False, "Function cannot be empty."
            
            # parse x0
            x0, success, error = self._parse_vector(self.x0_input.text())
            if not success:
                return None, False, error
            
            # allow math funcs
            safe_dict = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
            safe_dict['np'] = np
            
            def objective_function(x: np.ndarray) -> float:
                try:
                    with warnings.catch_warnings():
                        warnings.filterwarnings('ignore', category=RuntimeWarning)
                        
                        safe_dict["x"] = x
                        val = eval(func_str, {"__builtins__": {}}, safe_dict)
                        
                        # invalid results?
                        if val is None or isinstance(val, complex):
                            return float("inf")
                        if math.isnan(val) or math.isinf(val):
                            return float("inf")
                        
                        return float(val)
                except (ValueError, ZeroDivisionError, OverflowError):
                    return float("inf")
                except Exception as e:
                    raise Exception(str(e))

            # create gradient and hessian
            grad_func = self._create_numerical_gradient(objective_function)
            hess_func = self._create_numerical_hessian(objective_function)

            problem = OptimizationProblem(
                obj_func=objective_function,
                grad_func=grad_func,
                hess_func=hess_func,
                epsilon=self.eps_input.value(),
                method_name=self.opt_method_combo.currentText(),
                x_0=x0,
                max_iter=self.max_iter_input.value()
            )
            return problem, True, ""
        except Exception as e:
            return None, False, f"Unexpected error: {str(e)}"