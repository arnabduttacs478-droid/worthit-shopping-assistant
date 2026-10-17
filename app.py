
import streamlit as st
import pandas as pd
import database
from app_logic import normalize_feature, calculate_scores

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="WorthIt? | Shopping Assistant",
    page_icon="🛍️",
    layout="wide",
)

st.title("WorthIt? 🛍️")
st.subheader("Spend smarter. Buy what actually fits your needs.")

st.write(
    "A personalized shopping assistant that helps you compare "
    "products based on your budget, intended use, and priorities."
)

st.warning(
    "DEMO MODE: All products, prices, and feature values are "
    "illustrative sample data, not verified market information."
)

# ==================================================
# 2. CATEGORY CONFIGURATION
# ==================================================

CATEGORIES = {
    "Earbuds": {
        "file": "data/earbuds.csv",
        "features": {
            "Microphone quality": {
                "column": "mic_quality",
                "type": "rating",
                "unit": "/5",
            },
            "Comfort": {
                "column": "comfort",
                "type": "rating",
                "unit": "/5",
            },
            "Bass": {
                "column": "bass",
                "type": "rating",
                "unit": "/5",
            },
            "Battery life": {
                "column": "battery_hours",
                "type": "quantity",
                "unit": " hours",
            },
        },
    },
    "Laptops": {
        "file": "data/laptops.csv",
        "features": {
            "Processor performance": {
                "column": "processor_score",
                "type": "rating",
                "unit": "/5",
            },
            "RAM capacity": {
                "column": "ram_gb",
                "type": "quantity",
                "unit": " GB",
            },
            "Battery life": {
                "column": "battery_hours",
                "type": "quantity",
                "unit": " hours",
            },
            "Portability": {
                "column": "weight_kg",
                "type": "lower_better",
                "unit": " kg",
            },
        },
    },
    "Smartphones": {
        "file": "data/smartphones.csv",
        "features": {
            "Camera quality": {
                "column": "camera_score",
                "type": "rating",
                "unit": "/5",
            },
            "Performance": {
                "column": "performance_score",
                "type": "rating",
                "unit": "/5",
            },
            "Battery capacity": {
                "column": "battery_mah",
                "type": "quantity",
                "unit": " mAh",
            },
            "Display quality": {
                "column": "display_score",
                "type": "rating",
                "unit": "/5",
            },
        },
    },
}


# ==================================================
# 3. DISPLAY HELPER
# ==================================================

def format_feature_value(value, feature_config):
    """Format a feature value for display."""

    if pd.isna(value):
        return "Not available"

    if feature_config["type"] == "rating":
        return f"{value:g}/5"

    return f"{value:g}{feature_config['unit']}"


# ==================================================
# 4. SELECT CATEGORY AND LOAD DATA
# ==================================================

st.header("1. Choose a Product Category")

category = st.selectbox(
    "What are you shopping for?",
    options=list(CATEGORIES.keys()),
)

config = CATEGORIES[category]
feature_configurations = config["features"]

try:
    products = pd.read_csv(config["file"])

except FileNotFoundError:
    st.error(
        f"Could not find `{config['file']}`. "
        "Check that the CSV exists inside your data folder."
    )
    st.stop()

except pd.errors.ParserError:
    st.error(
        f"The file `{config['file']}` could not be read. "
        "Check its CSV formatting."
    )
    st.stop()

except UnicodeDecodeError:
    st.error(
        f"The file `{config['file']}` has an unsupported text encoding."
    )
    st.stop()


required_columns = [
    "name",
    "price_inr",
    *[
        feature["column"]
        for feature in feature_configurations.values()
    ],
]

missing_columns = [
    column
    for column in required_columns
    if column not in products.columns
]

if missing_columns:
    st.error(
        "The selected dataset is missing required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()

if products.empty:
    st.error("There are no products in this category yet.")
    st.stop()


products["name"] = (
    products["name"]
    .fillna("")
    .astype(str)
    .str.strip()
)

products["price_inr"] = pd.to_numeric(
    products["price_inr"],
    errors="coerce",
)

for feature_config in feature_configurations.values():
    column = feature_config["column"]

    products[column] = pd.to_numeric(
        products[column],
        errors="coerce",
    )


products = products[
    (products["name"] != "")
    & products["price_inr"].notna()
    & (products["price_inr"] >= 0)
].copy()


if products["name"].duplicated().any():
    st.error(
        f"The {category.lower()} dataset contains duplicate product names. "
        "Give every product a unique name before continuing."
    )
    st.stop()

if products.empty:
    st.error("No valid product records were found in this dataset.")
    st.stop()

# Stable indices allow product-specific analysis after filtering.
products = products.reset_index(drop=True)


# ==================================================
# 5. PERSONAL PRIORITIES
# ==================================================

st.header("2. Set Your Priorities")

st.write(
    "Rate each feature from 1 to 5. A higher rating means "
    "that feature matters more to you."
)

weights = {}

left, right = st.columns(2)

for index, (feature_name, feature_config) in enumerate(
    feature_configurations.items()
):
    target_column = left if index % 2 == 0 else right
    column = feature_config["column"]

    with target_column:
        weights[column] = st.slider(
            feature_name,
            min_value=1,
            max_value=5,
            value=3,
            key=f"priority_{category}_{column}",
        )


scored_products = calculate_scores(
    products,
    feature_configurations,
    weights,
)


# ==================================================
# 6. BUDGET AND SEARCH FILTERS
# ==================================================

st.header("3. Find Products")

min_price = int(products["price_inr"].min())
max_price = int(products["price_inr"].max())

slider_min = (min_price // 1000) * 1000
slider_max = ((max_price + 999) // 1000) * 1000

if slider_min == slider_max:
    slider_max = slider_min + 1000

default_budget = min(
    max(1500, slider_min),
    slider_max,
)

budget_step = (
    500
    if slider_max - slider_min >= 500
    else 100
)

budget = st.slider(
    "Maximum budget (₹)",
    min_value=slider_min,
    max_value=slider_max,
    value=default_budget,
    step=budget_step,
    key=f"budget_{category}",
)

search_query = st.text_input(
    "Search products by name",
    placeholder="For example, Demo Laptop A",
    key=f"search_{category}",
)


filtered = scored_products[
    scored_products["price_inr"] <= budget
].copy()

if search_query.strip():
    filtered = filtered[
        filtered["name"].str.contains(
            search_query.strip(),
            case=False,
            na=False,
            regex=False,
        )
    ].copy()


unscored_count = int(
    filtered["match_score"].isna().sum()
)

if unscored_count:
    st.warning(
        f"{unscored_count} product(s) have no usable feature values "
        "and cannot be ranked. Check their dataset records."
    )

filtered = filtered[
    filtered["match_score"].notna()
].copy()


# ==================================================
# 7. HANDLE EMPTY RESULTS
# ==================================================

if filtered.empty:
    st.info(
        "No rankable products match your current budget and search. "
        "Try increasing your budget, changing your search, or checking "
        "the dataset for missing feature values."
    )

    st.header(f"Your {category} Shortlist")

    try:
        saved_names = database.get_shortlist(category)

    except Exception as error:
        st.error(f"Could not load your saved shortlist: {error}")
        st.stop()

    saved_products = scored_products[
        scored_products["name"].isin(saved_names)
    ].copy()

    if saved_products.empty:
        st.info(
            f"You have not saved any {category.lower()} yet."
        )

    else:
        st.dataframe(
            saved_products[
                ["name", "price_inr"]
            ].rename(
                columns={
                    "name": "Product",
                    "price_inr": "Price (₹)",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        if st.button(
            f"Clear {category} Shortlist",
            key=f"clear_shortlist_{category}",
        ):
            try:
                database.clear_shortlist(category)
                st.success(f"{category} shortlist cleared.")
                st.rerun()

            except Exception as error:
                st.error(
                    f"Could not clear the shortlist: {error}"
                )

    st.stop()


filtered = filtered.sort_values(
    by=["match_score", "price_inr"],
    ascending=[False, True],
).reset_index(drop=True)


# ==================================================
# 8. RANKED RESULTS
# ==================================================

st.header("4. Your Best Matches")

st.caption(
    "Scores use category-wide feature ranges and your selected "
    "priorities. Missing feature values are excluded from a product's "
    "score rather than treated as average performance. Rankings reflect "
    "illustrative data, not verified product quality."
)

display_columns = (
    ["name", "price_inr"]
    + [
        feature["column"]
        for feature in feature_configurations.values()
    ]
    + ["match_score"]
)

rename_columns = {
    "name": "Product",
    "price_inr": "Price (₹)",
    "match_score": "Match Score (/5)",
}

for feature_name, feature_config in feature_configurations.items():
    rename_columns[feature_config["column"]] = feature_name


results = filtered[display_columns].rename(
    columns=rename_columns
).copy()

results["Match Score (/5)"] = (
    results["Match Score (/5)"].round(2)
)

st.dataframe(
    results,
    use_container_width=True,
    hide_index=True,
)


# ==================================================
# 9. BEST MATCH
# ==================================================

best = filtered.iloc[0]

st.success(
    f"Best match in your current results: **{best['name']}** "
    f"with a score of {best['match_score']:.2f}/5."
)

st.subheader("Why This Product Matches You")

priority_features = [
    (feature_name, feature_config)
    for feature_name, feature_config in feature_configurations.items()
    if weights[feature_config["column"]] >= 4
]

if priority_features:
    for feature_name, feature_config in priority_features:
        column = feature_config["column"]
        value = best[column]

        st.write(
            f"- **{feature_name}:** "
            f"{format_feature_value(value, feature_config)}."
        )

else:
    st.write(
        "You gave similar importance to the available features, "
        "so the recommendation balances them."
    )


# ==================================================
# 10. PRICE AND VALUE ANALYSIS
# ==================================================

st.header("5. Price and Value Analysis")
st.subheader("Price vs. Match Score")

chart_data = filtered[
    ["name", "price_inr", "match_score"]
].rename(
    columns={
        "name": "Product",
        "price_inr": "Price (₹)",
        "match_score": "Match Score (/5)",
    }
).set_index("Product")

st.scatter_chart(
    chart_data,
    x="Price (₹)",
    y="Match Score (/5)",
)

st.caption(
    "A higher price does not guarantee a better match."
)

st.subheader("Budget Trade-offs")

lowest_price = filtered.sort_values(
    by=["price_inr", "match_score"],
    ascending=[True, False],
).iloc[0]

top_match = filtered.iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Lowest-priced option",
        f"₹{lowest_price['price_inr']:,.0f}",
    )
    st.write(f"**{lowest_price['name']}**")
    st.write(
        f"Match score: {lowest_price['match_score']:.2f}/5"
    )

with col2:
    st.metric(
        "Top personalized match",
        f"₹{top_match['price_inr']:,.0f}",
    )
    st.write(f"**{top_match['name']}**")
    st.write(
        f"Match score: {top_match['match_score']:.2f}/5"
    )

if lowest_price["name"] == top_match["name"]:
    st.info(
        "The lowest-priced option is also the top personalized match."
    )

else:
    difference = (
        top_match["match_score"]
        - lowest_price["match_score"]
    )

    st.write(
        f"The top match scores {difference:.2f} points higher "
        "than the lowest-priced option."
    )


# ==================================================
# 11. PRODUCT FIT ANALYSIS
# ==================================================

st.header("6. Product Fit Analysis")

selected_for_analysis = st.selectbox(
    "Choose a product to analyse",
    options=filtered["name"].tolist(),
    index=0,
    key=f"analysis_{category}",
)

product = filtered.loc[
    filtered["name"] == selected_for_analysis
].iloc[0]

# Find the product's stable index in the original dataset.
product_index = products.index[
    products["name"] == selected_for_analysis
][0]

analysis_rows = []
available_weight = 0.0
normalized_feature_values = {}

# Normalize against the complete category dataset.
# This keeps the analysis consistent with the main ranking.
for feature_name, feature_config in feature_configurations.items():
    column = feature_config["column"]
    weight = weights.get(column, 0)

    normalized_values = normalize_feature(
        products[column],
        feature_config["type"],
    )

    normalized_value = normalized_values.loc[product_index]

    normalized_feature_values[feature_name] = normalized_value

    if pd.notna(normalized_value) and weight > 0:
        available_weight += weight

# Build the feature explanation table.
for feature_name, feature_config in feature_configurations.items():
    column = feature_config["column"]
    weight = weights.get(column, 0)
    raw_value = product[column]

    normalized_value = normalized_feature_values[feature_name]

    contribution = None

    if (
        pd.notna(normalized_value)
        and weight > 0
        and available_weight > 0
    ):
        contribution = round(
            float(normalized_value)
            * weight
            / available_weight,
            2,
        )

    analysis_rows.append(
        {
            "Feature": feature_name,
            "Recorded value": format_feature_value(
                raw_value,
                feature_config,
            ),
            "Your priority": weight,
            "Relative score (/5)": (
                round(float(normalized_value), 2)
                if pd.notna(normalized_value)
                else None
            ),
            "Weighted contribution": contribution,
        }
    )


analysis = pd.DataFrame(analysis_rows)

st.write(
    f"**{selected_for_analysis}** — "
    f"₹{product['price_inr']:,.0f}"
)

st.dataframe(
    analysis,
    use_container_width=True,
    hide_index=True,
)

if available_weight > 0:
    st.caption(
        "Weighted contributions show each feature's contribution "
        "to the final match score. Missing feature values are "
        "excluded from the calculation. Values are rounded for display."
    )

else:
    st.warning(
        "A match score cannot be explained because no usable "
        "feature values have a positive priority."
    )


# Identify strongest and weakest relative features.
valid_analysis = analysis.dropna(
    subset=["Relative score (/5)"]
)

col1, col2 = st.columns(2)

if valid_analysis.empty:
    st.info(
        "No feature values are available for relative fit analysis."
    )

else:
    strongest = valid_analysis.loc[
        valid_analysis["Relative score (/5)"].idxmax()
    ]

    weakest = valid_analysis.loc[
        valid_analysis["Relative score (/5)"].idxmin()
    ]

    with col1:
        st.metric(
            "Strongest relative feature",
            strongest["Feature"],
            f"{strongest['Relative score (/5)']}/5",
        )

    with col2:
        st.metric(
            "Weakest relative feature",
            weakest["Feature"],
            f"{weakest['Relative score (/5)']}/5",
        )

st.caption(
    "Relative feature scores compare the selected product with "
    "the category's illustrative sample data. They are not "
    "independent measures of real-world product quality."
)


# ==================================================
# 12. PERSONALIZED BUYING VERDICT
# ==================================================

st.subheader("WorthIt? Verdict")

selected_price = float(product["price_inr"])
selected_score = float(product["match_score"])
average_score = float(filtered["match_score"].mean())

if selected_score >= average_score + 0.5:
    fit_label = "Strong match"
    fit_reason = (
        "This product scores notably above the average match score "
        "among the products currently shown."
    )

elif selected_score >= average_score:
    fit_label = "Reasonable match"
    fit_reason = (
        "This product scores at or above the average match score "
        "among the products currently shown."
    )

else:
    fit_label = "Consider alternatives"
    fit_reason = (
        "Other products in the current results may align better "
        "with your selected priorities."
    )

st.markdown(f"### {fit_label}")
st.write(fit_reason)
st.write(f"**Price:** ₹{selected_price:,.0f}")
st.write(f"**Match score:** {selected_score:.2f}/5")
st.write(
    f"**Budget remaining:** ₹{budget - selected_price:,.0f}"
)

# Explain a meaningful feature trade-off.
if not valid_analysis.empty:
    strongest_name = strongest["Feature"]
    weakest_name = weakest["Feature"]

    if strongest_name == weakest_name:
        st.write(
            f"**Feature insight:** {strongest_name} is the "
            "available feature with the highest relative score."
        )

    else:
        st.write(
            f"**Strength:** {strongest_name} has the highest "
            "relative score for this product."
        )
        st.write(
            f"**Trade-off:** {weakest_name} has the lowest "
            "relative score among its available features."
        )

st.caption(
    "This verdict is based on the current shortlist, selected priorities, "
    "and illustrative dataset. It is not a guarantee of product quality."
)


# ==================================================
# 13. PRODUCT COMPARISON
# ==================================================

st.header("7. Compare Products")

product_names = filtered["name"].tolist()

selected_products = st.multiselect(
    "Select up to three products to compare",
    options=product_names,
    default=product_names[:2],
    max_selections=3,
    key=f"compare_{category}",
)

if len(selected_products) >= 2:
    comparison = filtered[
        filtered["name"].isin(selected_products)
    ][display_columns].rename(
        columns=rename_columns
    ).copy()

    comparison["Match Score (/5)"] = (
        comparison["Match Score (/5)"].round(2)
    )

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True,
    )

else:
    st.info("Select at least two products to compare.")


# ==================================================
# 14. DATABASE-BACKED SHORTLIST
# ==================================================

st.header(f"8. Your {category} Shortlist")

st.write(
    "Add products from the current results to this category's "
    "saved shortlist. Each category has its own persistent list."
)

try:
    saved_names = database.get_shortlist(category)

except Exception as error:
    st.error(f"Could not load your saved shortlist: {error}")
    st.stop()


products_to_add = st.multiselect(
    "Choose products to save",
    options=product_names,
    default=[
        name for name in saved_names
        if name in product_names
    ],
    key=f"add_to_shortlist_{category}",
)

if st.button(
    f"Save {category} Shortlist",
    key=f"save_shortlist_{category}",
):
    try:
        database.save_shortlist(
            category,
            products_to_add,
        )

        st.success(
            f"{category} shortlist saved to the local database."
        )
        st.rerun()

    except Exception as error:
        st.error(
            f"Could not save the shortlist: {error}"
        )


try:
    saved_names = database.get_shortlist(category)

except Exception as error:
    st.error(
        f"Could not refresh your saved shortlist: {error}"
    )
    st.stop()


saved_products = scored_products[
    scored_products["name"].isin(saved_names)
].copy()

if saved_products.empty:
    st.info(
        f"Your {category.lower()} shortlist is empty. "
        "Select products above and click Save."
    )

else:
    saved_products = saved_products.sort_values(
        by=["match_score", "price_inr"],
        ascending=[False, True],
        na_position="last",
    )

    saved_display = saved_products[
        display_columns
    ].rename(
        columns=rename_columns
    ).copy()

    saved_display["Match Score (/5)"] = (
        saved_display["Match Score (/5)"].round(2)
    )

    st.dataframe(
        saved_display,
        use_container_width=True,
        hide_index=True,
    )

    csv_data = saved_display.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label=f"Download {category} Shortlist (CSV)",
        data=csv_data,
        file_name=(
            f"worthit_{category.lower()}_shortlist.csv"
        ),
        mime="text/csv",
        key=f"download_shortlist_{category}",
    )

    if st.button(
        f"Clear {category} Shortlist",
        key=f"clear_shortlist_{category}",
    ):
        try:
            database.clear_shortlist(category)
            st.success(f"{category} shortlist cleared.")
            st.rerun()

        except Exception as error:
            st.error(
                f"Could not clear the shortlist: {error}"
            )


# ==================================================
# 15. FOOTER
# ==================================================

st.divider()

st.caption(
    "WorthIt? is a prototype using illustrative datasets and "
    "transparent, rule-based scoring. AI integration and verified "
    "product data have not yet been implemented."
)
