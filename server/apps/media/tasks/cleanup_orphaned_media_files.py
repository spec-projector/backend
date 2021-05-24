from apps.core import injector
from apps.media.logic.interfaces import ICleanupMediaFilesService


def cleanup_orphaned_media_files_task():
    """Cleanup orphaned media files task."""
    cleanup_service = injector.get(ICleanupMediaFilesService)
    cleanup_service.cleanup_media_files()
