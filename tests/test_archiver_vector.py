import bact_archiver_bessyii

import unittest
import datetime
import logging

logger = logging.getLogger('bact')
# logger.setLevel(logging.DEBUG)


class CArchiverTest(unittest.TestCase):
    '''Access to scalar and vector / waveform data
    '''

    def setUp(self):
        self.archiver = bact_archiver_bessyii.FASTZC_proxy
        self.archiver_bessyii = bact_archiver_bessyii.FASTZC_proxy

        # Data is accessed from fast archiver
        # This data is gone after 2 or weeks. needs to be fixed that these
        # timestamps are automatically chosen appropriately

        t0 = datetime.datetime.now()
        # Archiver needs some time to publish data
        t0 -= datetime.timedelta(seconds=12 * 60 * 60)

        self.interval_seconds = 30 * 60
        t1 = t0 + datetime.timedelta(seconds=self.interval_seconds)

        self.start_stamp = t0
        self.end_stamp = t1

        self.expect_n_lines = self.interval_seconds / 2.0

    def checkNumberOfLines(self, nlines, expected_n_lines):
        self.assertGreater(nlines,  expected_n_lines * 0.9)
        self.assertLess(nlines, expected_n_lines * 1.1)

    @unittest.skip
    def test00_ScalarData(self):
        '''Test reading scalar data: bpm data count

        Here exemplifed using the count variable of the BPM IOC

        Todo:
           Why do I get only one datum?
        '''

        df = self.archiver.getData('MDIZ2T5G:count', t0=self.start_stamp,
                                   t1=self.end_stamp)
        self.checkNumberOfLines(df.shape[0], self.expect_n_lines)

    def test03_VectorData_BPM_SizeGuess(self):
        '''Check if guessing size matches
        '''
        res = self.archiver.guessSize('MDIZ2T5G:bdata', t0=self.start_stamp,
                                      t1=self.end_stamp)
        nlines, _ = res
        self.checkNumberOfLines(nlines, self.expect_n_lines)

    def test04_VectorData_BPM(self):
        '''Test reading vector/waveform data using bpm data
        '''
        df = self.archiver.getData('MDIZ2T5G:bdata', t0=self.start_stamp,
                                   t1=self.end_stamp)
        nlines, n_elements_vector = df.shape
        # Should be 2048
        self.assertEqual(n_elements_vector,  2048)
        self.checkNumberOfLines(nlines, self.expect_n_lines)

    @unittest.skip
    def test05_VectorData_Tune(self):
        '''Test reading vector/waveform data using tune data

        Get only one ....
        '''
        df = self.archiver.getData('TUNEZR:wxH', t0=self.start_stamp,
                                   t1=self.end_stamp)
        self.checkNumberOfLines(df.shape[0], self.expect_n_lines)


if __name__ == "__main__":
    unittest.main()
