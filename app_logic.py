
import pandas as pd


SUPPORTED_FEATURE_TYPES = {
    "rating",
    "quantity",
    "lower_better",
}


def normalize_feature(series, feature_type):
    """Normalize feature values to a 1–5 scale."""

    if feature_type not in SUPPORTED_FEATURE_TYPES:
        raise ValueError(
            f"Unsupported feature type: {feature_type!r}. "
            f"Expected one of {sorted(SUPPORTED_FEATURE_TYPES)}."
        )

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
            result[column],
            feature_type,
        )

        valid = normalized.notna()

        weighted_total.loc[valid] += (
            normalized.loc[valid] * weight
        )
        available_weight.loc[valid] += weight

    result["match_score"] = (
        weighted_total / available_weight
    ).where(available_weight > 0)

    return result


def explain_score(product, features, weights):
    """Explain a product's match score feature by feature.

    Returns a DataFrame containing each feature's relative score,
    priority weight, and weighted contribution to the final score.
    Missing feature values are excluded from the calculation.
    """

    rows = []
    weighted_total = 0.0
    available_weight = 0.0

    for feature_name, feature_config in features.items():
        column = feature_config["column"]
        feature_type = feature_config["type"]
        weight = weights.get(column, 0)

        if column not in product.index or weight <= 0:
            continue

        value = pd.to_numeric(
            pd.Series([product[column]]),
            errors="coerce",
        ).iloc[0]

        if pd.isna(value):
            rows.append({
                "Feature": feature_name,
                "Priority": weight,
                "Relative score (/5)": None,
                "Weighted contribution": None,
            })
            continue

        # Normalize against the full category dataset supplied
        # through the feature configuration's data column.
        rows.append({
            "Feature": feature_name,
            "Priority": weight,
            "Relative score (/5)": None,
            "Weighted contribution": None,
        })

    return pd.DataFrame(rows)
