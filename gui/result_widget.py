import numpy as np
from typing import Callable
from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QFrame, QGridLayout, QSizePolicy, QHBoxLayout
)
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from utils import (OptimizationResult, ResultWidgetConstants, 
                   UIHelper, PlotColors, StatusMessages, StatusColor, SolutionStatus)


class ResultSection(QGroupBox):
    """Widget for displaying multidimensional optimization results and convergence plot"""
    def __init__(self) -> None:
        super().__init__("Optimization Results")
        self._init_ui()
    
    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        self.status_label = UIHelper.create_label("Ready",
            style="font-weight: bold; font-size: 14px; padding: 5px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.result_card = QFrame()
        self.result_card.setStyleSheet("background-color: #2b2b2b; border-radius: 8px; border: 1px solid #3d3d3d;")
        card_layout = QVBoxLayout(self.result_card)
        
        value_style = f"color: #4CAF50; font-size: {ResultWidgetConstants.VALUE_SIZE}px; font-weight: bold; font-family: {ResultWidgetConstants.FONT_FAMILY};"
        header_style = f"font-size: {ResultWidgetConstants.HEADER_SIZE}px; font-family: {ResultWidgetConstants.FONT_FAMILY};"
        coord_style = f"color: #0078D7; font-size: {ResultWidgetConstants.COORD_SIZE}px; font-family: {ResultWidgetConstants.FONT_FAMILY};"
        
        # min point
        card_layout.addWidget(UIHelper.create_label("Minimum Point (x*):", style=header_style))
        self.lbl_xmin_val = UIHelper.create_label("-", style=coord_style)
        self.lbl_xmin_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_xmin_val.setWordWrap(True)
        card_layout.addWidget(self.lbl_xmin_val)
        
        # min value
        card_layout.addWidget(UIHelper.create_label("Function Value f(x*):", style=header_style))
        self.lbl_fmin_val = UIHelper.create_label("-", style=value_style.replace("bold", "normal"))
        self.lbl_fmin_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.lbl_fmin_val)
        
        layout.addWidget(self.result_card)

        # Details
        details_layout = QGridLayout()
        self.lbl_iters = UIHelper.create_label("Iterations: -")
        self.lbl_final_eps = UIHelper.create_label("Precision: -")
        details_layout.addWidget(self.lbl_iters, 0, 0)
        details_layout.addWidget(self.lbl_final_eps, 0, 1)
        layout.addLayout(details_layout)

        # graph
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.figure.patch.set_facecolor(PlotColors.BACKGROUND) 
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.canvas)

    def _format_vector(self, vec: np.ndarray) -> str:
        """Format vector for display"""
        if len(vec) <= 5:
            return "[" + ", ".join([f"{x:.5f}" for x in vec]) + "]"
        else:
            first_three = ", ".join([f"{x:.5f}" for x in vec[:3]])
            return f"[{first_three}, ..., {vec[-1]:.5f}]"

    def display_results(self, opt_result: OptimizationResult) -> None:
        """Display text results and plot convergence graph"""
        status = opt_result.status or SolutionStatus.UNKNOWN.value
        status_text = StatusMessages.get_message(status)
        status_color = StatusColor.get_color(status)
        self.status_label.setText(status_text)
        self.status_label.setStyleSheet(
            f"font-weight: bold; font-size: 14px; padding: 5px; "
            f"background-color: {status_color}; border-radius: 4px; color: white;"
        )
        # update values
        if status == SolutionStatus.OPTIMAL.value:
            self.lbl_xmin_val.setText(self._format_vector(opt_result.x_min))
            self.lbl_fmin_val.setText(f"{opt_result.value:.5f}")
        else:
            self.lbl_xmin_val.setText("N/A")
            self.lbl_fmin_val.setText("N/A")
            
        self.lbl_iters.setText(f"Iterations: {opt_result.iterations}")
        self.lbl_final_eps.setText(f"Precision: {opt_result.final_epsilon:.5f}")
        self.result_card.show()

        if status == SolutionStatus.OPTIMAL.value and opt_result.trajectory is not None and len(opt_result.trajectory) > 1:
            self.plot_convergence(opt_result)

    def plot_convergence(self, opt_res: OptimizationResult) -> None:
        """Draw convergence plot showing distance to optimal point"""
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)

            # calculate distances from each point to the final point
            optimal_point = opt_res.x_min
            distances = []
            for point in opt_res.trajectory:
                dist = np.linalg.norm(point - optimal_point)
                distances.append(dist)
            
            iterations = list(range(len(distances)))
            
            # plot
            ax.plot(iterations, distances, 
                   color=PlotColors.TRAJECTORY, 
                   linewidth=2, 
                   marker='o', 
                   markersize=4,
                   label='Distance to optimum')
            
            # mark start and end
            ax.plot(0, distances[0], 'o', 
                   color=PlotColors.START_POINT, 
                   markersize=8, 
                   zorder=5, 
                   label='Start')
            ax.plot(len(distances)-1, distances[-1], 'o', 
                   color=PlotColors.END_POINT, 
                   markersize=8, 
                   zorder=5, 
                   label='End')

            ax.set_xlabel('Iteration', fontsize=10)
            ax.set_ylabel('Distance to optimal point', fontsize=10)
            ax.set_title("Convergence Plot", fontsize=12, fontweight='bold')
            ax.grid(True, linestyle=':', alpha=0.6)
            ax.legend(fontsize='small')
            
            self.figure.patch.set_facecolor("#FFFFFF")
            self.canvas.draw()
        except Exception as e:
            self.figure.patch.set_facecolor(PlotColors.BACKGROUND)
            raise Exception(f"Plot error: {str(e)}")

    def clear(self) -> None:
        """Clear all results"""
        self.status_label.setText("Ready")
        self.status_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        self.figure.patch.set_facecolor(PlotColors.BACKGROUND)
        self.lbl_xmin_val.setText("-")
        self.lbl_fmin_val.setText("-")
        self.lbl_iters.setText("Iterations: -")
        self.lbl_final_eps.setText("Precision: -")
        self.figure.clear()
        self.canvas.draw()