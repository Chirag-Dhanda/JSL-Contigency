import logging
from typing import List, Dict

logger = logging.getLogger("AlertSystem")

class AlertSystem:
    """Generates system alerts for AI infrastructure failures."""
    
    def __init__(self):
        pass

    def generate_alerts(self, health_data: Dict) -> List[Dict[str, str]]:
        """Analyzes health data and flags issues."""
        alerts = []
        
        if health_data.get("storage_usage_percent", 0) > 85.0:
            alerts.append({"type": "Warning", "message": "Vector DB storage exceeding 85%."})
            
        for component, status in health_data.get("components", {}).items():
            if status != "Online":
                logger.error(f"Alert Generated: {component} is {status}")
                alerts.append({"type": "Critical", "message": f"{component} is {status}!"})
                
        return alerts
