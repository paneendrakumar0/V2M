import logging
import coloredlogs

def setup_logger(name: str = "v2m_pipeline", log_level: int = logging.INFO) -> logging.Logger:
    """
    Sets up an industrial-grade logger for the V2M pipeline.
    
    Args:
        name (str): Name of the logger.
        log_level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Avoid duplicate handlers if setup_logger is called multiple times
    if not logger.handlers:
        coloredlogs.install(
            level=log_level,
            logger=logger,
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
    return logger
