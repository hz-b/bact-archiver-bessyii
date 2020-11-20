import logging
# Please consider to rename the package or adjust this test to your
# package
import bact_archiver_local
import unittest


class BESSYIIArchivers(unittest.TestCase):

    def test001LoadDefault(self):
        '''Default archiver found
        '''
        bact_archiver_local.default

    def test002LoadArchivers(self):
        '''All archivers found
        '''
        archivers = bact_archiver_local.archivers
        keys = list(archivers.keys())
        self.assertEqual(len(keys), 2)


if __name__ == '__main__':
    unittest.main()
