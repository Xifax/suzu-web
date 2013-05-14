# -*- coding: utf-8 -*-

from src.db.storage import Storage
import redis

class TestRedis:
    """Test Redis"""

    def test_can_process_kradfile(self):
        """Test that we can process kradfile"""
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        red = Storage(r)
        assert [u'一', u'言', u'口', u'五'] == red.get_radicals(u'語')

    def test_can_reverse_search_kanji(self):
        """Test that we can reverse-find all kanji with specified radical"""
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        red = Storage(r)
        #red.prepare_reverse_index()
        assert set(['黑', '黕', '黔']).issubset(
            red.find_kanji_with_radical(u'黒')
        )
