import logging
import sys

def setup_logging():
    # Enterprise standard logging configuration
    logger = logging.getLogger("jsl_app")
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate handlers
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console Handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # Future placeholders for File Handlers:
        # app_logger = FileHandler('logs/app.log')
        # error_logger = FileHandler('logs/error.log')
        # audit_logger = FileHandler('logs/audit.log')
        # perf_logger = FileHandler('logs/performance.log')
        
    return logger

logger = setup_logging()
