from .kiosk import create_app

server = create_app()

__all__ = ("server",)
