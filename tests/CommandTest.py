import unittest
import tempfile
from PyOpenWorm.command import POW
import os
from os.path import exists, abspath
import shutil
import json


class CommandTest(unittest.TestCase):

    def setUp(self):
        self.testdir = tempfile.mkdtemp(prefix=__name__)
        self.startdir = os.getcwd()
        os.chdir(self.testdir)
        self.cut = POW()

    def tearDown(self):
        os.chdir(self.startdir)
        shutil.rmtree(self.testdir)

    def test_init_default_creates_store(self):
        self.cut.init()
        self.assertTrue(exists('worm.db'), msg='worm.db is created')

    def test_init_default_creates_config(self):
        self.cut.init()
        self.assertTrue(exists('default.conf'), msg='default.conf is created')

    def test_init_default_store_name_is_absolute(self):
        self.cut.init()
        with open('default.conf', 'r') as f:
            conf = json.load(f)
            self.assertTrue(conf['rdf.store_conf'].startswith('/'), msg="DB Store is absolute")

    def test_init_default_store_config_file_exists_no_change(self):
        with open('default.conf', 'w') as f:
            f.write('{}')

        self.cut.init()
        with open('default.conf', 'r') as f:
            self.assertEqual('{}', f.read())

    def test_init_default_store_config_file_exists_update_store_conf(self):
        with open('default.conf', 'w') as f:
            f.write('{}')

        self.cut.init(update_existing_config=True)
        with open('default.conf', 'r') as f:
            conf = json.load(f)
            self.assertEqual(conf['rdf.store_conf'], abspath('worm.db'), msg='path is updated')
