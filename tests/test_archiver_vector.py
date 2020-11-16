import bact_archiver_bessyii
# from bact_archiver.archiver2 import archiver
# from bact_archiver.carchiver import archiver
from bact_archiver import convert_datetime_to_timestamp

import numpy as np
import unittest
import datetime
import logging

logger = logging.getLogger('bact')
# logger.setLevel(logging.DEBUG)


class CArchiverTest(unittest.TestCase):
    '''Access to scalar and vector / waveform data
    '''

    def setUp(self):
        self.archiver = bact_archiver_bessyii.FASTZC

        # Data is accessed from fast archiver
        # This data is gone after 2 or weeks. needs to be fixed that these
        # timestamps are automatically chosen appropriately

        now = datetime.datetime.now()
        t0 = now
        t1 = now + datetime.timedelta(seconds=3 * 60)

        print(t0, t1)
        self.start_stamp = convert_datetime_to_timestamp(t0)
        self.end_stamp = convert_datetime_to_timestamp(t1)

        # self.start_stamp = '2020-03-19T18:31:02.000000Z'
        # self.end_stamp = '2020-03-19T18:34:41.000000Z'

        self.expect_n_lines = 110

    def test00_ScalarData(self):
        '''Test reading scalar data

        Here exemplifed using the count variable of the BPM IOC
        '''

        df = self.archiver.getData('MDIZ2T5G:count', t0=self.start_stamp,
                                   t1=self.end_stamp)
        df = np.array(df)
        # print(df)
        l = df.shape[0]
        self.assertEqual(l, self.expect_n_lines)

    def test02_VectorData_BPM(self):
        '''Test reading vector/waveform data using bpm data
        '''
        df = self.archiver.getData('MDIZ2T5G:bdata', t0=self.start_stamp,
                                   t1=self.end_stamp)
        l0 = df.shape[0]
        self.assertEqual(l0,  self.expect_n_lines)

    def test03_VectorData_Tune(self):
        '''Test reading vector/waveform data using tune data
        '''
        df = self.archiver.getData('TUNEZR:wxH', t0=self.start_stamp,
                                   t1=self.end_stamp)
        l0 = df.shape[0]
        self.assertEqual(l0,  self.expect_n_lines)


if __name__ == "__main__":
    unittest.main()
