"""
Singleton dependencies for resource management.
Prevents creating multiple heavy resources on every API request.
"""
from typing import Optional

# Global singletons - Services
_auth_service = None
_profile_service = None
_common_service = None


def get_auth_service():
    """Get singleton AuthService instance"""
    global _auth_service
    if _auth_service is None:
        from app.services.Auth import AuthService
        _auth_service = AuthService()
    return _auth_service


def get_profile_service():
    """Get singleton ProfileService instance"""
    global _profile_service
    if _profile_service is None:
        from app.services.Profile import ProfileService
        _profile_service = ProfileService()
    return _profile_service


def get_common_service():
    """Get singleton CommonService instance"""
    global _common_service
    if _common_service is None:
        from app.services.Common import CommonService
        _common_service = CommonService()
    return _common_service


def cleanup_resources():
    """
    Cleanup all singleton resources. Call this on application shutdown.
    """
    global _auth_service, _profile_service, _common_service
    
    # Reset all services
    _auth_service = None
    _profile_service = None
    _common_service = None