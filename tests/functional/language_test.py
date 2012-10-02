# -*- coding: utf-8 -*-

from src.language import Language


class TestLanguage:
    """Detect language API test cases."""

    def test_can_detect_language(self):
        """Test that we can correctly detect language code"""
        assert 'ru' in Language().detect(u'Водка-балалайка!')
