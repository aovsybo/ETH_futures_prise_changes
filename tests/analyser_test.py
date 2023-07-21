from unittest import TestCase, main

from utils import get_futures_change, has_changes_for_hour


class AnalyserTest(TestCase):
    def test_frequency_percent_float(self):
        f_prev = 120.1
        f_current = 112.4
        self.assertEqual(get_futures_change(f_prev, f_current), 6.4)

    def test_frequency_percent_huge_value(self):
        f_prev = 100000
        f_current = 100115
        self.assertEqual(get_futures_change(f_prev, f_current), -0.1)

    def test_frequency_percent_small_value(self):
        f_prev = 10.0
        f_current = 9.9
        self.assertEqual(get_futures_change(f_prev, f_current), 1)

    def test_changes_for_hour_equal(self):
        futures_history = [0.3, 0.3, 0.3, 0.1]
        self.assertTrue(has_changes_for_hour(futures_history)["status"])

    def test_changes_for_hour_less(self):
        futures_history = [0.3, 0.3, 0.3]
        self.assertFalse(has_changes_for_hour(futures_history)["status"])

    def test_changes_for_hour_more(self):
        futures_history = [0.3, 0.3, 0.3, 0.3]
        self.assertTrue(has_changes_for_hour(futures_history)["status"])

    def test_changes_for_hour_negative_num(self):
        futures_history = [0.3, 0.3, 0.3, 0.3, -0.1]
        self.assertTrue(has_changes_for_hour(futures_history)["status"])


if __name__ == '__main__':
    main()
