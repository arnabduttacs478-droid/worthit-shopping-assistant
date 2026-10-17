# WorthIt? 🛍️

### Spend smarter. Buy what actually fits your needs.

**WorthIt? is an open-source, AI-powered shopping decision assistant in development that aims to help people make more informed purchasing decisions through personalized product comparisons, budget-aware recommendations, and transparent trade-off analysis.**

Instead of choosing products based only on price, popularity, or ratings, WorthIt? focuses on what matters to the individual buyer.

**The idea is simple: help people understand what they're buying, what they're compromising on, and which option best fits their needs.**

> Built for the **Hacktoberfest 2026 DEV Challenge — Week 2: Side Hustle**.

---

## 📌 Table of Contents

- [The Problem](#-the-problem)
- [Our Approach](#-our-approach)
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Using WorthIt](#-using-worthit)
- [Product Data](#-product-data)
- [Scoring Methodology](#-scoring-methodology)
- [Current Limitations](#-current-limitations)
- [Roadmap](#-roadmap)
- [Use Cases](#-use-cases)
- [Contributing](#-contributing)
- [Future Possibilities](#-future-possibilities)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## 💡 The Problem

Online shopping offers countless choices, but choosing the right product is not always easy.

Buyers frequently encounter:

- **Information overload:** Too many products, specifications, and competing claims.
- **Confusing specifications:** Technical details that are difficult to interpret without specialist knowledge.
- **Budget constraints:** Uncertainty about whether a cheaper product provides sufficient value.
- **Generic recommendations:** Rankings that may not reflect individual needs or intended use.
- **Hidden trade-offs:** A product may perform well in one area while falling short in another.
- **Time-consuming research:** Comparing several products manually can take hours.

A product with the highest rating or lowest price is not necessarily the right choice for every person.

WorthIt? explores a more personalized and transparent approach to purchasing decisions.

## 🎯 Our Approach

WorthIt? aims to make product selection more understandable by combining structured product information, user-defined priorities, budget filtering, and explainable comparison logic.

The project is being developed around three principles:

1. **Personalization over generic rankings** — recommendations should reflect the buyer's requirements.
2. **Transparency over black-box scores** — users should be able to examine the features and trade-offs behind a recommendation.
3. **Evidence over assumptions** — product information and calculations should be grounded in available data, with sources provided wherever verified information is available.

The long-term vision is to combine deterministic comparison logic with open-weight AI models, allowing users to describe their needs naturally while keeping product facts and calculations independently verifiable.

## ✨ Features

The current prototype focuses on the foundations of personalized shopping decisions.

### Available in the prototype

- **Budget-aware filtering:** Narrow product options according to a spending limit.
- **Preference-based ranking:** Assign importance to relevant features and rank products accordingly.
- **Product comparison:** Examine competing options using their available specifications and calculated scores.
- **Transparent scoring:** Inspect how product attributes contribute to personalized rankings.
- **Trade-off analysis:** Explore differences between stronger and weaker feature areas.
- **Interactive interface:** Explore product information through a Streamlit web application.
- **Local product datasets:** Work with structured product information without requiring a live shopping API.
- **Automated tests:** Test core scoring and database functionality.

### Planned capabilities

- **Natural-language requirements:** Describe a shopping need in everyday language.
- **Open-weight AI integration:** Interpret requirements and generate understandable explanations.
- **Source-backed product information:** Associate specifications and prices with verifiable sources.
- **Expanded product coverage:** Support additional categories beyond the initial datasets.
- **Improved recommendation explanations:** Make the reasoning behind comparisons easier to understand.
- **Optional live shopping integrations:** Explore external product data and availability where reliable access is possible.

*Planned capabilities are not represented as completed features.*

## ⚙️ How It Works

The intended workflow is straightforward.

1. **Choose a category** — start with a supported product category.
2. **Set your budget** — filter out options that exceed your spending limit.
3. **Define your priorities** — indicate which features matter most to you.
4. **Compare available products** — explore the specifications and personalized scores.
5. **Examine trade-offs** — understand where products perform relatively better or worse.
6. **Make an informed decision** — use the comparison as a guide and verify important details before purchasing.

### Example

Imagine a student looking for wireless earphones for online classes with a budget of ₹1,500.

Their priorities might be:

- Microphone quality: Very important
- Comfort: Very important
- Battery life: Important
- Bass performance: Less important

A conventional ranking might favor a product with a higher overall rating. WorthIt? aims to help the student identify which available option better matches their actual priorities.

The example illustrates the project's intended use; recommendations depend on the quality and completeness of the product data.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application and scoring logic |
| Streamlit | Interactive web interface |
| Pandas | Structured data processing and comparison |
| SQLite | Local shortlist storage |
| CSV | Product datasets and data export |
| `unittest` | Automated testing |
| Git and GitHub | Version control and collaboration |

The architecture is designed to support incremental development without requiring a complex infrastructure for the initial prototype.

## 📂 Project Structure

```text
worthit-shopping-assistant/
│
├── app.py
├── app_logic.py
├── database.py
├── test_database.py
├── test_scoring.py
│
├── data/
│   ├── earbuds.csv
│   ├── laptops.csv
│   └── smartphones.csv
│
├── requirements.txt
├── .gitignore
└── README.md
```

**Key files and directories**

- `app.py` — Streamlit application and user interface.
- `app_logic.py` — Product scoring and feature-normalization logic.
- `database.py` — Local database operations.
- `test_database.py` — Tests for database functionality.
- `test_scoring.py` — Tests for scoring calculations.
- `data/` — Structured datasets for supported product categories.
- `requirements.txt` — Python dependencies.
- `.gitignore` — Files and directories excluded from version control.

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or a compatible Python version for the project's dependencies.
- Git (optional, for cloning the repository).
- A terminal or IDE such as Visual Studio Code.

### 1. Clone the repository

```bash
git clone https://github.com/arnabduttacs478-droid/worthit-shopping-assistant.git
```

Navigate into the project directory:

```bash
cd worthit-shopping-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser to use the application.

### Windows alternative

If your virtual environment is already configured, you can run the application directly:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## 🧪 Running Tests

WorthIt? includes automated tests for its scoring logic and database operations.

Run the test suite from the project root:

```bash
python -m unittest discover -v
```

On Windows, if you prefer using the project's virtual environment directly:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -v
```

Tests help identify issues with calculations and data operations as the project evolves.

## 🛒 Using WorthIt?

Once the application starts:

1. Select a supported product category.
2. Set your maximum budget.
3. Adjust feature priorities to reflect your needs.
4. Review the ranked products.
5. Inspect the available feature comparisons and trade-offs.
6. Compare alternatives before deciding which product deserves further consideration.

The exact recommendations depend on the selected category, available dataset, budget, and scoring configuration.

## 📊 Product Data

The current prototype uses local CSV datasets for its supported categories.

These datasets allow the application to demonstrate filtering, scoring, and comparison without depending on external shopping services.

**Important data considerations:**

- The current dataset is illustrative and should not be treated as a verified live shopping catalogue.
- Prices, availability, specifications, and ratings must be verified with original sellers or authoritative sources before real purchasing decisions.
- Missing or inaccurate values can affect comparisons.
- Live product discovery and automated source verification are future development goals, not current guarantees.

The project aims to make data provenance an important part of future development so users can distinguish verified information from estimates or incomplete records.

## 🧮 Scoring Methodology

WorthIt? uses deterministic scoring logic to compare products against selected feature priorities.

The general approach is:

1. Normalize available feature values to a common scale.
2. Account for whether a higher or lower value is preferable.
3. Apply the user's selected feature priorities.
4. Calculate a weighted score using the available weighted features.
5. Rank products using the resulting scores.

Match Score = Σ (Feature Weight × Normalized Feature Score)
              / Σ (Available Feature Weights)

This approach helps prevent a product from being penalized simply because a feature is missing, although missing information can still reduce the reliability of the comparison.

**A higher match score does not automatically mean higher objective quality.** Scores depend on the available comparison set, feature definitions, data quality, and user-selected priorities.

The methodology will continue to evolve as the project develops.

## ⚠️ Current Limitations

WorthIt? is an early-stage prototype, not a production-ready shopping platform.

Current limitations include:

- Local datasets rather than verified live shopping listings.
- No implemented open-weight AI integration yet.
- No guarantee of current prices or product availability.
- Comparisons limited to the information available in each dataset.
- Relative scoring that depends on the products and features being compared.
- No claim that recommendations have been validated against real-world purchasing outcomes.

The project prioritizes building a reliable comparison foundation before introducing more complex integrations.

## 🗺️ Roadmap

The development roadmap is organized into incremental stages.

### Phase 1 — Core prototype

- [x] Build an interactive Streamlit interface.
- [x] Implement budget-based filtering.
- [x] Implement preference-based scoring and ranking.
- [x] Support structured local product datasets.
- [x] Establish automated tests for core logic and database functionality.

### Phase 2 — Better comparisons

- [ ] Improve explanations of feature-level strengths and trade-offs.
- [ ] Expand validation of product data and missing values.
- [ ] Refine scoring behavior and document its assumptions.
- [ ] Add reproducible comparison examples and stronger test coverage.

### Phase 3 — Trustworthy product information

- [ ] Replace illustrative data with source-verified product records.
- [ ] Record source references and data freshness where available.
- [ ] Improve handling of conflicting, incomplete, or outdated information.
- [ ] Explore reliable ways to update product data.

### Phase 4 — Open-weight AI integration

- [ ] Evaluate suitable open-weight language models.
- [ ] Interpret natural-language requirements into structured preferences.
- [ ] Generate explanations grounded in available product attributes.
- [ ] Prevent unsupported product claims and unverified specifications.
- [ ] Evaluate AI-generated explanations against deterministic calculations.

### Phase 5 — Expansion and evaluation

- [ ] Evaluate recommendations against realistic shopping scenarios.
- [ ] Improve accessibility and usability.
- [ ] Explore additional product categories.
- [ ] Investigate optional shopping integrations.
- [ ] Publish a working public demo when deployment is ready.

Roadmap items may change as the project develops and its assumptions are tested.

## 👥 Who Can Benefit?

WorthIt? is intended for people who want to make more informed purchasing decisions without spending hours comparing specifications.

Potential users include:

- **Students** shopping within limited budgets.
- **Everyday consumers** comparing competing products.
- **Families** balancing affordability and practical requirements.
- **Technology buyers** trying to understand unfamiliar specifications.
- **Developers and researchers** interested in transparent recommendation systems.

The broader objective is to explore how personalized decision support can make product research more understandable and less time-consuming.

## 🤝 Contributing

Contributions, suggestions, bug reports, and constructive feedback are welcome.

Potential contribution areas include:

- Improving the scoring methodology.
- Adding tests and handling edge cases.
- Improving the Streamlit interface.
- Expanding and validating product datasets.
- Improving accessibility and documentation.
- Exploring open-weight AI integration.
- Investigating trustworthy product data sources.

### Contribution workflow

1. Fork the repository.
2. Create a branch for your changes.
3. Make a focused improvement.
4. Run the automated tests.
5. Submit a pull request describing the change and its reasoning.

Please avoid introducing unverified product claims or presenting planned features as implemented capabilities.

## 🔭 Future Possibilities

WorthIt? is being developed as an exploration of more transparent, user-centered shopping assistance.

Potential future directions include:

- Natural-language shopping requirements.
- Explainable AI-assisted comparisons.
- Source-backed product discovery.
- More extensive category coverage.
- Optional affiliate partnerships or premium features, if validated and implemented responsibly.

These are possibilities rather than commitments. Any future monetization should preserve the project's emphasis on transparent comparisons and clearly distinguish commercial incentives from user-focused recommendations.

## 🔐 Privacy and Data Handling

The current prototype is designed around local product datasets and local shortlist storage.

It does not currently require a live shopping account or an external AI service for its core deterministic comparison workflow. Future integrations may introduce additional data flows and will need to be documented appropriately.

Users should avoid entering sensitive personal information into experimental applications.

## 📄 License

This project is intended to be released under the MIT License. The repository should include a `LICENSE` file containing the applicable license text before the project is represented as formally MIT-licensed.

## 🙌 Acknowledgements

WorthIt? is being developed as an open-source learning and experimentation project, with an emphasis on practical problem-solving, transparent logic, and responsible AI integration.

Thanks to the open-source communities behind Python, Streamlit, Pandas, SQLite, and the wider developer ecosystem.

---

## 💬 Final Note

WorthIt? is still evolving. The current prototype establishes the foundation for personalized product comparison, while future development will focus on reliable data, more understandable explanations, and carefully integrated open-weight AI.

**WorthIt? — Because the best purchase isn't always the cheapest one.**

**Repository:** https://github.com/arnabduttacs478-droid/worthit-shopping-assistant
