# -*- coding: utf-8 -*-

from src.db.storage import Storage
import redis

class TestRedis:
    """Test Redis"""

    def test_can_process_kradfile(self):
        """Test that we can process kradfile"""
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        red = Storage(r)
        assert [u'一', u'言', u'口', u'五'] == red.get_radikals(u'語')

