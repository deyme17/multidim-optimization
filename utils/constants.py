from enum import Enum

class SolutionStatus(Enum):
    OPTIMAL = 'optimal'
    NOT_CONVERGED = 'not_converged'
    MAX_ITERATIONS = 'max_iterations'
    ERROR = 'error'
    UNKNOWN = 'unknown'

class StatusColor(Enum):
    OPTIMAL = '#4CAF50'
    NOT_CONVERGED = '#FF9800'
    MAX_ITERATIONS = "#D34D00"
    ERROR = "#ff1100"
    UNKNOWN = '#aaaaaa'
    
    @staticmethod
    def get_color(status: str) -> str:
        color_map = {
            SolutionStatus.OPTIMAL.value: StatusColor.OPTIMAL.value,
            SolutionStatus.NOT_CONVERGED.value: StatusColor.NOT_CONVERGED.value,
            SolutionStatus.MAX_ITERATIONS.value: StatusColor.MAX_ITERATIONS.value,
            SolutionStatus.ERROR.value: StatusColor.ERROR.value,
            SolutionStatus.UNKNOWN.value: StatusColor.UNKNOWN.value,
        }
        return color_map.get(status, StatusColor.UNKNOWN.value)

class StatusMessages:
    LABELS = {
        SolutionStatus.OPTIMAL.value: "Optimal Solution Found",
        SolutionStatus.NOT_CONVERGED.value: "Not Converged",
        SolutionStatus.MAX_ITERATIONS.value: "Maximum Iterations Reached",
        SolutionStatus.ERROR.value: "Error Occurred",
        SolutionStatus.UNKNOWN.value: "Unknown Status",
    }
    
    @staticmethod
    def get_message(status: str) -> str:
        """Get message for given status"""
        return StatusMessages.LABELS.get(status, "Unknown Status")
    
# app
class AppConstants:
    WINDOW_TITLE = "Multidimensional Optimization"
    WINDOW_SIZE = (1000, 800)
    TITLE_FONT_SIZE = 16
    BUTTON_HEIGHT = 40
    BUTTON_FONT_SIZE = 12
    LAYOUT_SPACING = 15
    LAYOUT_MARGINS = 15

# input widget
class InputWidgetConstants:
    DEFAULT_FUNC = "(1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2"  # rosenbrock function
    DEFAULT_X0_STR = "-1.2, 1.0"
    DEFAULT_EPS = 1e-6
    DEFAULT_MAX_ITER = 1000

# result widget
class ResultWidgetConstants:
    FONT_FAMILY = "Segoe UI"
    HEADER_SIZE = 12
    VALUE_SIZE = 16
    COORD_SIZE = 14

# plot
class PlotColors:
    TRAJECTORY = '#0078D7'
    START_POINT = '#FF9800'
    END_POINT = '#4CAF50'
    CONTOUR_LINES = '#888888'
    BACKGROUND = "#0A0A0A60"