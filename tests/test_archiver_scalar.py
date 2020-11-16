import bact_archiver_bessyii
from bact_archiver import convert_datetime_to_timestamp
import unittest
import datetime


class CArchiverTest(unittest.TestCase):
    '''Access to scalar and vector / waveform data
    '''

    def setUp(self):
        self.archiver = bact_archiver_bessyii.FASTZC

        now = datetime.datetime.now()
        t0 = now
        t1 = now + datetime.timedelta(seconds=30 * 60)

        self.start_stamp = convert_datetime_to_timestamp(t0)
        self.end_stamp = convert_datetime_to_timestamp(t1)

        print(t0, t1, self.start_stamp, self.end_stamp)
        self.expect_n_lines = 110

    def test00_ReadingBeamCurrent(self):
        '''Reading TOPUPCC:rdCur as reliable input'''
        data = self.archiver.getData('TOPUPCC:rdCur', t0=self.start_stamp,
                                     t1=self.end_stamp)
        print(data)


if __name__ == '__main__':
    unittest.main()
