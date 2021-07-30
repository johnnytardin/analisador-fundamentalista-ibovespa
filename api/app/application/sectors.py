import logging

from app.application import db

logger = logging.getLogger(__name__)


def get_sectors_names():
    sectors = db.sectors()
    return sectors
