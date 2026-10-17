
import unittest

import pandas as pd

from app_logic import normalize_feature, calculate_scores


class TestNormalizeFeature(unittest.TestCase):

    def test_higher_values_get_higher_scores(self):
        values = pd.Series([10, 20, 30])

        scores = normalize_feature(values, "quantity")

        self.assertAlmostEqual(scores.iloc[0], 1.0)
        self.assertAlmostEqual(scores.iloc[1], 3.0)
        self.assertAlmostEqual(scores.iloc[2], 5.0)

    def test_lower_values_get_higher_scores_when_lower_is_better(self):
        values = pd.Series([1, 2, 3])

        scores = normalize_feature(values, "lower_better")

        self.assertAlmostEqual(scores.iloc[0], 5.0)
        self.assertAlmostEqual(scores.iloc[1], 3.0)
        self.assertAlmostEqual(scores.iloc[2], 1.0)

    def test_missing_values_remain_missing(self):
        values = pd.Series([10, None, 30])

        scores = normalize_feature(values, "quantity")

        self.assertTrue(pd.isna(scores.iloc[1]))

    def test_identical_values_receive_neutral_scores(self):
        values = pd.Series([8, 8, 8])

        scores = normalize_feature(values, "quantity")

        self.assertEqual(scores.tolist(), [3.0, 3.0, 3.0])


class TestCalculateScores(unittest.TestCase):

    def test_weighted_score_uses_feature_priorities(self):
        data = pd.DataFrame({
            "performance": [10, 30],
            "battery": [30, 10],
        })

        features = {
            "Performance": {
                "column": "performance",
                "type": "quantity",
            },
            "Battery": {
                "column": "battery",
                "type": "quantity",
            },
        }

        weights = {
            "performance": 5,
            "battery": 1,
        }

        result = calculate_scores(data, features, weights)

        self.assertGreater(
            result.loc[1, "match_score"],
            result.loc[0, "match_score"],
        )

    def test_all_missing_features_produce_no_score(self):
        data = pd.DataFrame({
            "performance": [None, None],
        })

        features = {
            "Performance": {
                "column": "performance",
                "type": "quantity",
            },
        }

        result = calculate_scores(
            data,
            features,
            {"performance": 3},
        )

        self.assertTrue(result["match_score"].isna().all())


if __name__ == "__main__":
    unittest.main()
