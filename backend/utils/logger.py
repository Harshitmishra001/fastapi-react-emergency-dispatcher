import logging
import json
from datetime import datetime, timezone

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage()
        }
        if hasattr(record, "user_id"):
            log_record["user_id"] = record.user_id
        if hasattr(record, "report_id"):
            log_record["report_id"] = record.report_id
        if hasattr(record, "need_id"):
            log_record["need_id"] = record.need_id
        if hasattr(record, "action"):
            log_record["action"] = record.action
            
        return json.dumps(log_record)

def get_audit_logger(name: str = "disaster_audit"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # File handler for audit logs
        fh = logging.FileHandler("audit.log")
        fh.setFormatter(JSONFormatter())
        logger.addHandler(fh)
        
        # Console handler for dev
        ch = logging.StreamHandler()
        ch.setFormatter(JSONFormatter())
        logger.addHandler(ch)
        
    return logger
