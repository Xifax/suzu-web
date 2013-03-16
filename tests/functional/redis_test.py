# -*- coding: utf-8 -*-

from src.db.storage import Storage
import redis

class TestRedis:
    """Test Redis"""

    def test_can_process_kradfile(self):
        """Test that we can process kradfile"""
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        red = Storage(r)
        assert ['一', '言', '口', '五'] == red.get_radikals(u'語')

