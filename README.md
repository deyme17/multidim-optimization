# multidim-optimization

A Python application for finding the minimum of multivariable functions. This project implements classical gradient-based optimization algorithms for multidimensional problems, supporting both first-order (steepest descent) and second-order (Newton) methods, with precise one-dimensional line search.

## 📋 Features

This application implements the following numerical methods:

1. **Steepest Descent (Gradient Descent)**
   - Direction of search: negative gradient `-∇f(x)`
   - Step size determined via accurate one-dimensional search along the direction

2. **Newton's Method**
   - Uses second-order information (Hessian matrix) for quadratic convergence near the minimum
   - Direction: `-H⁻¹∇f(x)`

3. **Line Search (for Steepest Descent)**
   - **Fibonacci Search**: Efficient derivative-free method for finding optimal step size λ in one-dimensional subproblem

4. **Graphical User Interface**
   - User-friendly input of arbitrary multivariable functions (e.g., `(1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2` — Rosenbrock function)
   - Selection of optimization method and parameters (precision ε, max iterations)
   - Display of results: minimum point, function value, number of iterations
   - Visualization of convergence (distance to optimal point vs. iteration)

## 📂 Project Structure

```text
multidim-optimization/
├── README.md                    # Project documentation
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── core/
│   ├── __init__.py
│   ├── line_searchers/
│   │   ├── __init__.py
│   │   └── fibonacci_method.py  # Fibonacci search for line search
│   ├── newton_method.py         # Newton's method implementation
│   └── steepest_descent.py      # Steepest descent with line search
├── gui/
│   ├── __init__.py
│   ├── app_window.py            # Main window
│   ├── input_widget.py          # Input configuration panel
│   └── result_widget.py         # Results display and plot
└── utils/
    ├── __init__.py
    ├── constants.py             # Constants, enums, colors, default values
    ├── containers.py            # Dataclasses: OptimizationProblem, OptimizationResult
    └── ...                      # Interfaces, UI helpers, styling
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- Required libraries (listed in `requirements.txt`): PyQt6, NumPy, Matplotlib

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/deyme17/multidim-optimization.git
   cd multidim-optimization
   ```

2. **Install dependencies:**
    ```bash
    install -r requirements.txt
    ```

## Usage
**Run the main script to launch the GUI application**
    ```bash 
    main.py
    ```
## 🧠 Theory & Methods

### 1. Steepest Descent
**Purpose:** First-order method using only gradient information.  

**How it works:**
- At each iteration, move in the direction of steepest decrease: `p_k = -∇f(x_k)`
- Find optimal step size λ by minimizing the one-dimensional function `φ(λ) = f(x_k + λ · p_k)`
- Uses Fibonacci search for accurate and efficient line search

### 2. Newton's Method
**Purpose:** Second-order method with quadratic convergence near the minimum.  

**How it works:**
- Uses Taylor expansion up to second order
- Search direction: `p_k = -H⁻¹(x_k) ∇f(x_k)`, where H is the Hessian matrix
- Performs full step (λ = 1) assuming local quadratic approximation is good

### 3. Fibonacci Line Search
**Purpose:** Find optimal step size in one-dimensional subproblem without derivatives.  

**How it works:**
- Uses Fibonacci sequence to systematically narrow the uncertainty interval
- Guarantees maximal reduction of interval for a fixed number of function evaluations
- Highly efficient for unimodal functions (which is typical along the search direction)

## 🎯 Example Usage

- Default function: Rosenbrock — `(1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2`
- Default starting point: `x₀ = [-1.2, 1.0]`
- Try both methods and compare convergence speed and number of iterations!