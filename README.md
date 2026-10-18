# WorthIt? 🛍️
### Demo🌐: https://worthit-shopping-assistant.onrender.com/
### Spend smarter. Buy what actually fits your needs.

**WorthIt?** is an open-source, AI-powered shopping decision assistant designed to help users make more informed purchasing decisions.

Instead of relying only on price, popularity, or a single rating, WorthIt? combines transparent, rule-based scoring with AI-generated explanations to compare products according to a user's budget, requirements, and personal priorities.

The idea is simple: **a good purchase isn't necessarily the cheapest or most expensive one. It's the one that makes the most sense for you.**

> Built for the **Hacktoberfest 2026 DEV Challenge — Week 2: Side Hustle**, as part of the open-source AI challenge.

---

## 📌 Table of Contents

- [The Problem](#-the-problem)
- [The Proposed Solution](#-the-proposed-solution)
- [Key Features](#-key-features)
- [How It Works](#-how-it-works)
- [Open-Source AI Integration](#-open-source-ai-integration)
- [Technology Stack](#️-technology-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Running Tests](#-running-tests)
- [Deployment on Render](#-deployment-on-render)
- [Current Limitations](#️-current-limitations)
- [Roadmap](#️-roadmap)
- [Hacktoberfest 2026 — Week 2: Side Hustle](#-hacktoberfest-2026--week-2-side-hustle)
- [Potential Use Cases and Future Scope](#-potential-use-cases-and-future-scope)
- [Contributing](#-contributing)
- [License](#-license)

---

## 💡 The Problem

Buying a product online often involves comparing multiple options with different specifications, prices, and advertised features. Finding the right product is not always straightforward.

- **Too many choices:** Similar products have different specifications that can be difficult to compare.
- **Different priorities:** A student buying earphones for online classes may value microphone quality and comfort more than bass.
- **Budget constraints:** The cheapest product may not meet essential requirements, while a more expensive option may offer features the user does not need.
- **Confusing specifications:** Technical details do not always explain how products differ in practical terms.
- **Limited personalization:** Generic rankings may not reflect an individual's intended use or priorities.
- **Unclear trade-offs:** Users need to understand what they gain or sacrifice when choosing one product over another.

These challenges can make purchasing decisions unnecessarily time-consuming, especially for people who want to make informed choices without researching every specification individually.

## 💡 The Proposed Solution

WorthIt? provides an interactive way to compare products using structured data, customizable feature priorities, and AI-assisted explanations.

Users can select a product category, set a budget, adjust the importance of individual features, and explore ranked results. The application calculates match scores using a transparent scoring algorithm.

An integrated AI assistant accepts requirements written in everyday language and compares available candidates. It explains relevant differences, highlights advantages and disadvantages, discusses budget-related trade-offs, and provides a recommendation grounded in the supplied product data.

The goal is not to make purchasing decisions on behalf of users. Instead, WorthIt? aims to make those decisions easier to understand.

---

## ✨ Key Features

### 1. Multiple Product Categories

The current prototype supports three categories:

- Wireless earbuds
- Laptops
- Smartphones

Each category has its own product dataset and comparison criteria.

### 2. Budget-Based Filtering

Users can define a budget to narrow the available options and focus on products that fall within their spending limit.

### 3. Customizable Feature Priorities

Users can assign different importance levels to supported product features.

For example, someone purchasing earbuds for online classes may prioritize microphone quality and comfort over bass performance.

The scoring system uses these priorities to calculate personalized match scores.

### 4. Transparent Product Scoring

WorthIt? uses deterministic, rule-based calculations to compare available products.

Supported feature types include:

- **Rating-based features:** Higher recorded values receive higher normalized scores.
- **Quantity-based features:** Higher values receive higher normalized scores.
- **Lower-is-better features:** Lower values receive higher normalized scores, such as product weight.

Missing feature values are excluded from the corresponding weighted calculation rather than being treated as genuine zero scores.

The result is a match score on a five-point scale, based on the available features and their assigned priorities.

### 5. AI Shopping Assistant

Users can describe their requirements in natural language.

For example:

> I need wireless earbuds for online classes under ₹1,500. Microphone quality and comfort matter more to me than bass.

The AI assistant analyzes the supplied requirements and candidate products to provide:

- A quick recommendation.
- A side-by-side comparison table.
- An explanation of the most important differences.
- Product-specific strengths and trade-offs.
- Conditional recommendations based on different needs.
- A list of information that should be verified before purchasing.

The AI assistant works with the products supplied by the application. It does not independently verify live market information.

### 6. Product Comparison and Explanations

Users can compare up to three selected products and examine their recorded specifications and calculated scores.

The application also includes supporting analyses, including price-versus-score visualization, feature explanations, budget trade-offs, and product-fit guidance.

### 7. Shortlist Management

Users can save products to a shortlist for later consideration.

SQLite is used to persist shortlisted products, with separate shortlists for different product categories.

### 8. CSV Export

Product results can be downloaded as a CSV file for further inspection or comparison.

### 9. Input Validation and Automated Tests

The project includes input validation for product data and automated unit tests for scoring calculations and shortlist database behavior.

---

## ⚙️ How It Works

WorthIt? combines deterministic application logic with generative AI.

1. **Choose a category:** Select earbuds, laptops, or smartphones.
2. **Set your requirements:** Apply a budget and available product filters.
3. **Adjust feature priorities:** Assign importance levels to supported features.
4. **Review ranked results:** The application calculates match scores from the available product data.
5. **Ask the AI assistant:** Describe your needs in natural language.
6. **Understand the trade-offs:** Receive a structured comparison and a recommendation based on the supplied data.
7. **Save or export:** Shortlist products or download the results.

### Why use both rule-based scoring and AI?

The two components have different responsibilities.

| Component | Responsibility |
|---|---|
| Structured product dataset | Supplies product attributes and prices |
| Rule-based scoring | Calculates normalized feature scores and weighted matches |
| Streamlit interface | Collects preferences and displays results |
| Open-weight AI model | Interprets requirements and explains product comparisons |
| SQLite database | Stores product shortlists |
| Pandas | Handles structured data and calculations |

This separation keeps numerical calculations explicit while using AI for explanations that are easier to understand in natural language.

---

## 🧠 Open-Source AI Integration

WorthIt? uses the open-weight **`openai/gpt-oss-20b`** language model through a hosted inference service to provide AI-assisted shopping guidance.

The model receives the user's requirements, feature priorities, and a limited set of candidate products from the application's existing results.

The AI is instructed to:

- Use the supplied product names and recorded values.
- Explain differences relevant to the user's requirements.
- Avoid inventing specifications, prices, reviews, or product capabilities.
- Identify missing information and unsupported requirements.
- Discuss trade-offs instead of automatically favoring the most expensive product.
- Remind users that the current dataset contains illustrative sample information.

The project combines this language-model integration with structured data and deterministic scoring rather than relying on AI-generated product facts alone.

**Important:** AI-generated explanations may still be incomplete or incorrect. The model does not independently verify product information, and the current application does not run the model locally.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| Pandas | Product data processing and scoring |
| SQLite | Persistent shortlist storage |
| Groq Python SDK | Communication with the hosted inference service |
| `openai/gpt-oss-20b` | Open-weight language model for explanations |
| Git and GitHub | Version control and collaboration |
| Render | Planned public web deployment |

---

## 📁 Project Structure

```text
worthit-shopping-assistant/
│
├── .streamlit/
│   └── secrets.toml          # Local configuration; keep private
│
├── data/
│   └──                         # Illustrative product datasets
│
├── app.py                    # Main Streamlit application
├── app_logic.py              # Feature normalization and scoring
├── ai_assistant.py           # AI comparison and recommendation logic
├── database.py               # SQLite shortlist operations
│
├── test_scoring.py           # Scoring and normalization tests
├── test_database.py          # Shortlist database tests
│
├── requirements.txt          # Python dependencies
├── .gitignore                # Excludes local and sensitive files
├── LICENSE                   # Project license
└── README.md                 # Project documentation
```

The exact contents of the `data/` directory may evolve as the prototype develops.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have:

- Python 3.10 or a compatible newer version.
- Git.
- An internet connection for AI-assisted comparisons.
- Access to the configured AI inference service.

### 1. Clone the repository

```bash
git clone https://github.com/arnabduttacs478-droid/worthit-shopping-assistant.git
cd worthit-shopping-assistant
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks environment activation, you can use the virtual environment's Python executable directly.

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the application

Configure the AI inference credentials locally using the application's supported secrets mechanism. Keep credentials private and outside version control.

The application can be started independently of the AI assistant for inspecting the interface and exploring features that do not require AI inference. AI-assisted comparisons require a valid configuration and network access.

### 5. Run the application

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser to use the application.

---

## 🧪 Running Tests

The repository contains unit tests for feature normalization, weighted scoring, missing-value handling, and shortlist database operations.

From the project root, run:

```bash
python -m unittest -v
```

The current development version has **12 passing unit tests** covering the scoring and shortlist database logic.

The tests do not represent exhaustive testing of the Streamlit interface, hosted AI inference, or the deployed application.

---

## 🌐 Deployment on Render

The application is designed to run as a Streamlit web application. A public deployment can be configured through Render.

### Deployment steps

1. Push the latest project files to GitHub.
2. Sign in to Render and create a new web service using the repository.
3. Configure the build command:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the start command:

   ```bash
   streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
   ```

5. Configure the AI inference credentials securely through Render's environment or secret settings.
6. Deploy the application and review the deployment logs.
7. Test the product filters, scoring, shortlist functionality, and AI assistant through the public URL.

The public deployment URL and deployment status should be added here once the deployment is complete and verified.

---

## ⚠️ Current Limitations

WorthIt? is an early-stage prototype, and several limitations should be understood before using its recommendations for actual purchases.

- **Illustrative product data:** Current datasets are sample data and must not be treated as verified market listings.
- **No live shopping integration:** The application does not currently fetch live prices, inventory, or seller information.
- **No independent product verification:** Product specifications, reviews, and real-world performance are not independently verified by the application.
- **AI limitations:** Generated explanations may be incomplete or incorrect despite safeguards in the prompt.
- **Hosted inference:** AI features require internet access and a working inference configuration, and may be affected by provider limits or availability.
- **Scoring limitations:** Match scores depend on the available attributes, their normalization, and the priorities selected by the user. They are not objective measures of overall product quality.
- **Natural-language interpretation:** The AI assistant uses written requirements to explain the existing candidate results; it does not automatically convert every natural-language preference into changes to the scoring sliders.
- **Testing scope:** Existing automated tests cover core scoring and database behavior, not every possible user interaction or external service failure.

Users should verify important product details directly with the original seller before making a purchase.

---

## 🗺️ Roadmap

- [x] Build the initial Streamlit application.
- [x] Support multiple product categories.
- [x] Implement budget filtering and feature-priority controls.
- [x] Implement transparent, rule-based match scoring.
- [x] Add product comparison and supporting visual analysis.
- [x] Implement persistent, category-specific shortlists.
- [x] Add CSV export.
- [x] Integrate an open-weight AI model through a hosted inference service.
- [x] Add AI-generated comparison tables and requirement-based explanations.
- [x] Add unit tests for scoring and shortlist database operations.
- [ ] Deploy and validate the public demo.
- [ ] Improve automated testing for AI integration and the complete application.
- [ ] Replace illustrative data with verified product information and source references.
- [ ] Explore responsible ways to retrieve updated product prices and specifications.
- [ ] Evaluate recommendation quality against realistic shopping scenarios.
- [ ] Consider additional product categories and future integrations.

---

## 🏆 Hacktoberfest 2026 — Week 2: Side Hustle

WorthIt? is being developed for the **Hacktoberfest 2026 DEV Challenge, Week 2: Side Hustle**, under the open-source AI challenge theme.

The challenge encourages participants to build a new project with open-source AI at its core and share their work through a DEV Community post.

### The problem being explored

Online shopping creates an information gap between the specifications sellers provide and the practical decisions customers need to make.

WorthIt? explores whether transparent scoring, structured product information, and AI-generated explanations can help users evaluate that information more effectively.

### The approach

The project combines:

- An open-weight language model for natural-language comparison and explanations.
- Deterministic calculations for feature normalization and weighted match scores.
- Structured datasets for product attributes.
- An interactive interface for budget and preference-based exploration.

### Why this direction?

A useful shopping assistant should do more than generate a generic recommendation. It should explain why an option fits a user's requirements, where it falls short, and what information remains uncertain.

WorthIt? is an early experiment in making AI-assisted purchase decisions more transparent, understandable, and adaptable to individual needs.

### Challenge goals

- Explore a practical problem with potential real-world value.
- Build a working prototype around open-source AI.
- Combine AI explanations with explicit, structured calculations.
- Document implementation choices, limitations, and future improvements.
- Develop the project openly and invite feedback.

**Tags for the accompanying DEV post:** `#devchallenge` `#hf26challenge`

---

## 💼 Potential Use Cases and Future Scope

WorthIt? is intended for people who want to make informed purchasing decisions without spending hours manually comparing specifications.

Potential users include:

- Students working within a limited budget.
- Buyers comparing similar products for a specific use case.
- Families evaluating different options against their needs.
- People who find technical specifications difficult to interpret.

Future development could explore verified product-data sources, broader categories, additional comparison criteria, and optional monetization models. These are possibilities for further investigation, not features currently implemented.

---

## 🤝 Contributing

Contributions, suggestions, bug reports, and constructive feedback are welcome.

Potential areas for contribution include:

- Improving feature normalization and comparison logic.
- Adding tests for edge cases.
- Improving accessibility and interface usability.
- Integrating verified product-data sources.
- Evaluating AI-generated explanations.
- Improving documentation and setup instructions.

When contributing, please avoid committing credentials, private data, or unverified claims about product specifications.

---

## 📄 License

This project is intended to be released under the **MIT License**. Refer to the repository's `LICENSE` file for the applicable license terms.

---

## 🛍️ WorthIt?

**Because the best purchase isn't always the cheapest one.**

Built as an exploration of open-source AI, transparent scoring, and more informed shopping decisions.

If you find the idea useful, consider starring the repository, sharing feedback, or contributing to its development.
