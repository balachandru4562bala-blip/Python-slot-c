"""
Package attendance_pkg initialization.
Exposes core functions at the package level.
"""
from .reader import read_attendance
from .stats import calculate_stats, find_consecutive_absentees
from .report import generate_report

__all__ = ["read_attendance", "calculate_stats", "find_consecutive_absentees", "generate_report"]
