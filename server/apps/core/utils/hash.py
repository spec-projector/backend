# -*- coding: utf-8 -*-

import hashlib
import random
from datetime import datetime
from typing import Optional


def generate_md5(source: Optional[str] = None) -> str:
    """Generated md5 hash."""
    if not source:
        source = '{0}-{1}'.format(datetime.now(), random.random())  # noqa: S311

    return hashlib.md5(source.encode()).hexdigest()  # noqa: S303
