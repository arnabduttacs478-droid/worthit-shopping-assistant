
import pandas as pd


def normalize_feature(series, feature_type):
    """Normalize feature values to a 1–5 scale."""
    values = pd.to_numeric(series, errors="coerce")
    minimum = values.min()
    maximum = values.max()

    if pd.isna(minimum) or pd.isna(maximum):
        return pd.Series(float("nan"), index=series.index)

    if minimum == maximum:
        scores = pd.Series(3.0, index=series.index)
        return scores.where(values.notna())

    scores = 1 + 4 * (values - minimum) / (maximum - minimum)

    if feature_type == "lower_better":
        scores = 6 - scores

    return scores


def calculate_scores(products, features, weights):
    """Calculate weighted match scores using available features."""
    result = products.copy()

    weighted_total = pd.Series(0.0, index=result.index)
    available_weight = pd.Series(0.0, index=result.index)

    for feature_config in features.values():
        column = feature_config["column"]
        feature_type = feature_config["type"]
        weight = weights.get(column, 0)

        if column not in result.columns or weight <= 0:
            continue

        normalized = normalize_feature(
            result[column], feature_type
        )

        valid = normalized.notna()
        weighted_total.loc[valid] += normalized.loc[valid] * weight
        available_weight.loc[valid] += weight

    result["match_score"] = (
        weighted_total / available_weight
    ).where(available_weight > 0)

    return result
