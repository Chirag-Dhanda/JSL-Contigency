import logging
import logging.handlers
import sys
import os
from shared.context import get_request_id, get_user_id, get_department, get_correlation_id
from config.manager import get_config

# 1. Add custom TRACE level (Level 5)
TRACE_LEVEL_NUM = 5
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")
def trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        self._log(TRACE_LEVEL_NUM, message, args, **kws)
logging.Logger.trace = trace

# 2. Context-aware Formatter
class ContextFormatter(logging.Formatter):
    def format(self, record):
        # Inject context variables
        record.request_id = get_request_id() or "-"
        record.user_id = get_user_id() or "-"
        record.department = get_department() or "-"
        record.correlation_id = get_correlation_id() or "-"
        return super().format(record)

# 3. Setup core logging framework
def setup_logging():
    config = get_config()
    
    # Base configuration
    log_format = "%(asctime)s | %(levelname)-8s | [%(name)s] | ReqID:%(request_id)s | User:%(user_id)s | %(message)s"
    formatter = ContextFormatter(log_format)
    
    log_level = config.logging.log_level.upper()
    level_num = logging.getLevelName(log_level)
    if not isinstance(level_num, int):
        level_num = logging.INFO
        
    root_logger = logging.getLogger()
    root_logger.setLevel(level_num)
    
    # Prevent duplicate handlers
    if not root_logger.handlers:
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        # Ensure logs directory exists
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        # Application Rolling File Handler (10MB max, keep 5 backups)
        app_file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, "application.log"), maxBytes=10485760, backupCount=5
        )
        app_file_handler.setFormatter(formatter)
        root_logger.addHandler(app_file_handler)
        
        # Error File Handler (Only WARNING and above)
        error_file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, "error.log"), maxBytes=10485760, backupCount=5
        )
        error_file_handler.setLevel(logging.WARNING)
        error_file_handler.setFormatter(formatter)
        root_logger.addHandler(error_file_handler)

setup_logging()

# 4. Logger Factory
def get_logger(category: str) -> logging.Logger:
    """
    Factory to retrieve dedicated loggers for different categories.
    E.g. get_logger('Auth'), get_logger('SAP'), get_logger('Database')
    """
    return logging.getLogger(category)
