"""Logging configuration for the test framework."""

import sys
import os
from pathlib import Path
from loguru import logger
from config.settings import config


def setup_logger() -> None:
    """Setup logger configuration."""
    
    # Remove default logger
    logger.remove()
    
    # Ensure logs directory exists
    log_dir = Path(config.log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Console logging with colors
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=config.log_level,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # File logging with rotation
    logger.add(
        config.log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True
    )
    
    # Add test results logging
    logger.add(
        "logs/test_results_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO",
        rotation="1 day",
        retention="7 days",
        filter=lambda record: "TEST_RESULT" in record["message"]
    )
    
    logger.info("Logger initialized successfully")


# Test result logging helpers
def log_test_start(test_name: str) -> None:
    """Log test start."""
    logger.info(f"TEST_RESULT | STARTED | {test_name}")


def log_test_pass(test_name: str, duration: float = 0) -> None:
    """Log test pass."""
    logger.info(f"TEST_RESULT | PASSED | {test_name} | Duration: {duration:.2f}s")


def log_test_fail(test_name: str, error: str, duration: float = 0) -> None:
    """Log test failure."""
    logger.error(f"TEST_RESULT | FAILED | {test_name} | Duration: {duration:.2f}s | Error: {error}")


def log_test_skip(test_name: str, reason: str) -> None:
    """Log test skip."""
    logger.warning(f"TEST_RESULT | SKIPPED | {test_name} | Reason: {reason}")