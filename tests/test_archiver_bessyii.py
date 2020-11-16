import logging
import bact_archiver_bessyii
import unittest


class BESSYIIArchivers(unittest.TestCase):

    def test001LoadDefault(self):
        '''Default archiver found
        '''
        bact_archiver_bessyii.default

    def test002LoadArchivers(self):
        '''All archivers found
        '''
        archivers = bact_archiver_bessyii.archivers
        keys = list(archivers.keys())
        self.assertEqual(len(keys), 5)


if __name__ == '__main__':
    unittest.main()
