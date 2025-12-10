from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget, QMessageBox
)
from PyQt6.QtGui import QFont
from typing import Dict
from utils.interfaces import IOptimizer

from utils import AppConstants, StyleSheet
from . import InputSection, ResultSection


class MultidimOptApp(QMainWindow):
    """Main application window for multidimensional optimization app"""
    def __init__(self, input_section: InputSection, results_section: ResultSection,
                 optimizers: Dict[str, IOptimizer]) -> None:
        super().__init__()
        self.input_section = input_section
        self.results_section = results_section
        self.optimizers = optimizers
        
        self._setup_window()
        self.init_ui()

    def _setup_window(self) -> None:
        """Setup window properties using AppConstants"""
        self.setWindowTitle(AppConstants.WINDOW_TITLE)
        self.setMinimumSize(*AppConstants.WINDOW_SIZE)
        self.setStyleSheet(StyleSheet.DARK_STYLE)
        
    def init_ui(self) -> None:
        """Initialize the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(AppConstants.LAYOUT_SPACING)
        main_layout.setContentsMargins(
            AppConstants.LAYOUT_MARGINS,
            AppConstants.LAYOUT_MARGINS,
            AppConstants.LAYOUT_MARGINS,
            AppConstants.LAYOUT_MARGINS
        )
        # title
        title = self._create_title()
        main_layout.addWidget(title)
        
        # tabs
        self.tabs = QTabWidget()
        
        # input section
        input_tab = QWidget()
        input_layout = QVBoxLayout(input_tab)
        input_layout.addWidget(self.input_section)
        input_layout.addStretch()
        self.tabs.addTab(input_tab, "Configuration")
        
        # result section
        results_tab = QWidget()
        results_layout = QVBoxLayout(results_tab)
        results_layout.addWidget(self.results_section)
        self.tabs.addTab(results_tab, "Results")
        
        main_layout.addWidget(self.tabs)
        
        # buttons
        buttons_layout = self._create_buttons_layout()
        main_layout.addLayout(buttons_layout)
    
    def _create_title(self) -> QLabel:
        """Create title label using AppConstants"""
        title = QLabel(AppConstants.WINDOW_TITLE)
        title_font = QFont()
        title_font.setPointSize(AppConstants.TITLE_FONT_SIZE)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #ffffff; margin-bottom: 5px;")
        return title
    
    def _create_buttons_layout(self) -> QHBoxLayout:
        """Create button layout using AppConstants"""
        layout = QHBoxLayout()
        layout.setSpacing(AppConstants.LAYOUT_SPACING)
        
        # clear
        self.btn_clear = self._create_button(
            "Clear Result", 
            AppConstants.BUTTON_HEIGHT, 
            AppConstants.BUTTON_FONT_SIZE
        )
        self.btn_clear.clicked.connect(self.on_clear)
        
        # optimize
        self.btn_optimize = self._create_button(
            "Find Optimum", 
            AppConstants.BUTTON_HEIGHT, 
            AppConstants.BUTTON_FONT_SIZE
        )
        self.btn_optimize.setStyleSheet("background-color: #0078D7; color: white; border-radius: 4px;")
        self.btn_optimize.clicked.connect(self.on_optimize)
        
        layout.addStretch()
        layout.addWidget(self.btn_clear)
        layout.addWidget(self.btn_optimize)
        return layout
    
    @staticmethod
    def _create_button(text: str, height: int, font_size: int) -> QPushButton:
        """Create styled button"""
        button = QPushButton(text)
        button.setMinimumHeight(height)
        button.setMinimumWidth(100)
        font = QFont()
        font.setPointSize(font_size)
        font.setBold(True)
        button.setFont(font)
        return button

    def on_optimize(self) -> None:
        """Handle optimize button click: Execute optimization -> Plot"""
        try:
            problem, success, error_msg = self.input_section.get_data()
            if not success:
                self._show_error(error_msg)
                return

            # optimization
            optimizer = self.optimizers.get(problem.method_name)
            if not optimizer:
                raise ValueError(f"Optimizer '{problem.method_name}' not found")
            
            opt_result = optimizer.optimize(problem)

            # display result
            self.results_section.display_results(opt_result)
            self.tabs.setCurrentIndex(1)

        except Exception as e:
            self._show_error(str(e))

    def on_clear(self) -> None:
        """Handle clear button click"""
        self.results_section.clear()
        self.tabs.setCurrentIndex(0)

    def _show_error(self, message: str) -> None:
        """Display error message dialog"""
        QMessageBox.warning(self, "Calculation Error", message)