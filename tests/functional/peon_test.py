# -*- coding: utf-8 -*-

from src.db.mongo import connectMongo
from src.run.peon import Peon
from src.db.models import (
        Key,
        Fact
)


class TestPeon:
    """Test Peon"""

    def test_can_process_unprocess_items(self):
        """Test that we can process unprocessed items"""
        #db = connectMongo()
        #Peon(db).process('kanji')
        #kanji = Peon(db).random()
        #print kanji.fact.gloss.readings['default']
        #facts = Fact.objects(key=kanji)
        #for usage in kanji.fact.usages:
            #print usage.gloss.readings['default']
