from datetime import datetime, timedelta
from app.models import User
from app import db

def can_register(ip_address, device_info):
    """Check if registration is allowed based on IP and device"""
    # two_days_ago = datetime.utcnow() - timedelta(days=2)
    
    # # Check IP address
    # ip_registration = User.query.filter(
    #     User.ip_address == ip_address,
    #     User.created_at > two_days_ago
    # ).first()
    
    # if ip_registration:
    #     return False
    
    # # Check device info
    # device_registration = User.query.filter(
    #     User.device_info == device_info,
    #     User.created_at > two_days_ago
    # ).first()
    
    # if device_registration:
    #     return False
    
    return True