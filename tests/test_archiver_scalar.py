import logging
import bact_archiver_bessyii
import unittest
import datetime

logger = logging.getLogger('bact-archiver-bessyii')


class CheckTimestamp:
    '''Check if timestamp is compatible with archiver expectations
    '''
    def checkTimestampText(self, txt):
        '''Check that the text maches the expected format
        '''
        tmp = txt.split('.')
        self.assertEqual(len(tmp), 2)
        timestamp, fractional = tmp
        self.assertEqual(fractional[-1], 'Z')

        fmt = '%Y-%m-%dT%H:%M:%S'

        d = datetime.datetime.strptime(timestamp, fmt)
        return d


class DateTimetoStringCompliance(unittest.TestCase, CheckTimestamp):
    '''
    '''

    def test00_SimpleDate(self):
        '''See if conversion matches expected format

        Should be similar to '2020-11-19T11:37:02.000000Z'
        '''
        from bact_archiver.archiver import convert_datetime_to_timestamp
        now = datetime.datetime.now()
        res = convert_datetime_to_timestamp(now)
        d2 = self.checkTimestampText(res)
        dt = now - d2
        self.assertLessEqual(abs(dt.seconds), 1.0)


class CArchiverTest(unittest.TestCase, CheckTimestamp):
    '''Access to scalar data
    '''

    def setUp(self):
        self.archiver = bact_archiver_bessyii.BESSY
        self.pvname = 'TOPUPCC:rdCur'

    def checkNumberOfLines(self, data, expected_n_lines):
        self.assertGreater(data.shape[0],  expected_n_lines * 0.9)
        self.assertLess(data.shape[0], expected_n_lines * 1.1)

    def test000_WithFixedStamps(self):
        '''Reading TOPUPCC:rdCur as reliable input

        Retrieving roughly 1 reading per second
        '''
        start_stamp = '2020-11-19T11:37:02.000000Z'
        end_stamp = '2020-11-19T11:39:02.000000Z'

        t0 = self.checkTimestampText(start_stamp)
        t1 = self.checkTimestampText(end_stamp)
        dt = t1 - t0

        expect_n_lines = dt.total_seconds() / 1.0

        fmt = "Sending request for variable %s time span: %s..%s"
        logger.debug(fmt, self.pvname, t0, t1)

        data = self.archiver.getData(self.pvname, t0=t0, t1=t1)
        self.checkNumberOfLines(data, expect_n_lines)

    def test000_AroundToday(self):
        """Make the tests around today
        """
        t0 = datetime.datetime.now()
        # Archiver needs some time to publish data
        t0 -= datetime.timedelta(seconds=2 * 60 * 60)
        self.interval_seconds = 30 * 60
        t1 = t0 + datetime.timedelta(seconds=self.interval_seconds)

        start_stamp = t0
        end_stamp = t1

        # One reading per second roughly
        expect_n_lines = self.interval_seconds / 1.0

        fmt = "Sending request for variable %s time span: %s..%s (types %s, %s)"
        logger.debug(fmt, self.pvname, t0, t1, type(t0), type(t1))
        data = self.archiver.getData(self.pvname, t0=t0, t1=t1)
        self.checkNumberOfLines(data, expect_n_lines)

        # see if data can also be read as datetime
        data = self.archiver.getData(self.pvname, t0=t0, t1=t1, time_format='datetime')
        print(data)

        
if __name__ == '__main__':
    unittest.main()
