# -*- coding: utf-8 -*-

from src.mecab import MeCab


class TestMeCab:
    """Detect language API test cases."""

    def test_can_sentence_reading_in_hiragana(self):
        """Test that we can get correct sentence reading"""
        assert (
            MeCab().reading(u'来週からテストが始まる。') ==
            u'らいしゅうからてすとがはじまる。'
        )

    def test_can_sentence_reading_in_katakana(self):
        """Test that we can get correct sentence reading without conversion"""
        assert (
            MeCab().reading(u'来週からテストが始まる。') ==
            u'ライシュウカラテストガハジマル。'
        )
