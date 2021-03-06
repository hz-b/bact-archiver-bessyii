import bact_archiver_bessyii

import unittest
import logging

logger = logging.getLogger('bact')
# logger.setLevel(logging.DEBUG)


class ArchiverMethods(unittest.TestCase):
    '''Check that non data retrieving methods work
    '''
    def setUp(self):
        self.archiver = bact_archiver_bessyii.BESSY

    def test00_MatchingPVS(self):
        '''Use topup engine to test matching pvs

        Should be at least a hundred or so
        Test gave 221
        '''
        pvs = self.archiver.getMatchingPVs('TOPUPCC*')
        n_pvs = len(pvs)
        self.assertGreater(n_pvs, 100)
        self.assertEqual(n_pvs, 231)

    def test01_AllPVs(self):
        '''Epics archiver returns 500 PV

        Todo:
           Check if that is an archiver limit
        '''
        pvs = self.archiver.getAllPVs()
        n_pvs = len(pvs)
        self.assertGreater(n_pvs, 450)
        self.assertEqual(n_pvs, 500)

    def test02_TypeInfo(self):
        '''Use topup read current to check type info
        '''
        meta_data = self.archiver.getTypeInfo('TOPUPCC:rdCur')
        print(meta_data)


if __name__ == "__main__":
    unittest.main()
