import unittest
import pandas as pd
import sys
import csv_combiner
from csv_combiner import headers_equal, handle_cli_args, combine_csvs

class CSVCombinerTest(unittest.TestCase):

    def test_headers_equal(self):
        df1 = pd.read_csv("fixtures/accessories.csv")
        df2 = pd.read_csv("fixtures/clothing.csv")
        df3 = pd.read_csv("fixtures/household_cleaners.csv")

        # All of the provided fixtures csv's have the same number of columns
        # and the same header values. Thus, headers_equal should return True
        self.assertEqual(True, headers_equal(df1, df2))
        self.assertEqual(True, headers_equal(df1, df3))
        self.assertEqual(True, headers_equal(df2, df3))

        # Now, we add a column to df3, this means that it should no longer be True
        df3["newcol"] = "foo"
        self.assertEqual(False, headers_equal(df1, df3))
        self.assertEqual(False, headers_equal(df2, df3))

        # If I add the same column to df2 as well, now df3 and df2 should be equal
        df2["newcol"] = "foo"
        self.assertEqual(True, headers_equal(df2, df3))

        # If I add a different column to df1, df1 has the same number of columns
        # as df2 and df3, but not the same header contents. Thus, it should
        # return False
        df1["nouveaucol"] = "bar"
        self.assertEqual(False, headers_equal(df1, df2))
        self.assertEqual(False, headers_equal(df1, df3))

    def test_handle_cli_args(self):

        # should raise a systemexit error since we are only
        # passing one argument. we need at least 2
        args = ["accessories.csv"]

        self.assertRaises(SystemExit, handle_cli_args, args)

        # at least two arguments were passed, so there should
        # not be a sys exit. we test the values of the outputted
        # parser for validity here
        args = ["accessories.csv", "clothing.csv"]

        result = handle_cli_args(args)
        self.assertEqual(result.csv1, ["accessories.csv"])
        self.assertEqual(result.csv2, ["clothing.csv"])

        # similar to last test case, but with third arg as well.
        args = ["accessories.csv", "clothing.csv", "household_cleaners.csv"]

        result = handle_cli_args(args)
        self.assertEqual(result.csv1, ["accessories.csv"])
        self.assertEqual(result.csv2, ["clothing.csv", "household_cleaners.csv"])

    def test_combine_csvs(self):
        args = ["fixtures/accessories.csv", "fixtures/clothing.csv"]
        result = handle_cli_args(args)
        
        accessories_lines = 0
        with open("fixtures/accessories.csv") as f:
            for line in f:
                accessories_lines = accessories_lines + 1
        clothing_lines = 0
        with open("fixtures/clothing.csv") as f:
            for line in f:
                clothing_lines = clothing_lines +1


        # combined csv should have the length of accessories and clothing combined!
        combined = combine_csvs(result)
        self.assertEqual(len(combined), accessories_lines + clothing_lines - 2)
        combined = combined.drop("filename", axis = 1)
        accessories = pd.read_csv("fixtures/accessories.csv")

        # tests to see whether cells from accessories were correctly added to the combined csv
        self.assertTrue((combined.loc[0]["email_hash"] == accessories.loc[0]["email_hash"]))
        self.assertTrue((combined.loc[20]["email_hash"] == accessories.loc[20]["email_hash"]))
        self.assertTrue((combined.loc[80]["email_hash"] == accessories.loc[80]["email_hash"]))
        self.assertTrue((combined.loc[0]["category"] == accessories.loc[0]["category"]))
        self.assertTrue((combined.loc[20]["category"] == accessories.loc[20]["category"]))
        self.assertTrue((combined.loc[80]["category"] == accessories.loc[80]["category"]))
