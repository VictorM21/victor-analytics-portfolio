markdown

🏷️ Dynamic Pricing Engine


[![Python](https://img.shields.io/badge/Python-3.11-blue)]()

[![PyMC](https://img.shields.io/badge/Bayesian-PyMC-orange)]()

[![FastAPI](https://img.shields.io/badge/API-FastAPI-green)]()

[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)]()

[![Docker](https://img.shields.io/badge/Docker-Ready-blue)]()



💼 Business Value Proposition


The Problem

Every company with inventory or variable demand faces the same challenge:

- Static pricing leaves revenue on the table during high-demand periods

- Manual price adjustments are slow, inconsistent, and error-prone

- Competitor dynamics change faster than humans can track

- Pricing decisions are made without quantifying risk



The Solution

A data-driven pricing engine that:

- Learns price elasticity from historical sales data

- Adapts to competitor movements, seasonality, and product lifecycle

- Quantifies uncertainty — every recommendation includes a confidence interval

- Scales from single products to batch processing thousands of SKUs



Measurable Impact

| Metric | Expected Improvement |

|--------|---------------------|

| Profit Margin | +5-10% lift vs. static pricing |

| Manual Effort | 15+ hours/week saved in pricing decisions |

| Decision Quality | Every recommendation includes risk assessment |

| Response Time | From 3 days to 3 milliseconds |



Real-World Applications

This approach applies to any industry with dynamic pricing needs:



| Industry | Use Case |

|----------|----------|

| E-commerce | Dynamic pricing for thousands of SKUs |

| Travel/Hospitality | Hotel room rates that adjust to demand |

| Ride-sharing | Surge pricing based on real-time supply/demand |

| Retail | Clearance pricing for seasonal inventory |

| SaaS | Usage-based pricing optimization |

| Energy | Time-of-day utility pricing |



What Makes This Different

Most pricing tools give you one number. This system gives you:

- The optimal price (point estimate)

- The range (90% confidence interval)

- The risk (probability of loss)



Because in the real world, decisions require understanding uncertainty.



🧠 Technical Deep Dive


The Challenge

Businesses lose millions by not optimizing prices dynamically. A product priced statically either:

- Leaves money on the table during demand spikes

- Sits unsold during slow periods

- Loses to competitors who adjust faster


The Solution Architecture

┌─────────────┐ ┌──────────────┐ ┌─────────────┐

│ PyMC │────▶│ FastAPI │────▶│ Streamlit │

│ Model │ │ Endpoint │ │ UI │

└─────────────┘ └──────────────┘ └─────────────┘

│ │ │

▼ ▼ ▼

┌─────────────┐ ┌──────────────┐ ┌─────────────┐

│ Elasticity │ │ /predict │ │ Interactive│

│ Estimates │ │ /batch │ │ Dashboard │

└─────────────┘ └──────────────┘ └─────────────┘


text


Key Technical Features

| Feature | Implementation | Why It Matters |

|---------|----------------|----------------|

| Bayesian Uncertainty | PyMC with NUTS sampling | Not just a price, but a *range* with confidence levels |

| Over-dispersed Counts | Negative Binomial likelihood | Handles real-world sales spikes and zeros correctly |

| Informed Priors | `elasticity = -exp(raw)` | Embeds business logic (price increases can't increase demand) |

| Category Hierarchy | Hierarchical model per product type | Shares information across similar products |

| Production API | FastAPI with Pydantic | Ready for integration with existing systems |

| Interactive UI | Streamlit dashboard | Non-technical stakeholders can use it immediately |

| Containerization | Docker + docker-compose | One-command deployment anywhere |



📊 Validation Results

*[To be added after model completes]*


🚀 Quick Start

Prerequisites

- Python 3.11+

- Docker (optional, for containerized run)


Installation

```bash

Clone the repository

git clone https://github.com/VictorM21/10-dynamic-pricing

cd 10-dynamic-pricing


Install dependencies

pip install -r requirements.txt



Generate synthetic data (or use your own)

python data/generate_synthetic_data.py

Run the API

bash

Start the FastAPI server

uvicorn api.main:app --reload

The API will be available at http://localhost:8000



Interactive docs: http://localhost:8000/docs



Alternative docs: http://localhost:8000/redoc



Run the UI

bash

In a new terminal

streamlit run ui/app.py

The UI will open at http://localhost:8501



Run with Docker (Production)

bash

Build and run with docker-compose

docker-compose up --build

This starts both the API and UI services.



🛠️ Tech Stack

Layer	      Technology	                      Why

Modeling       PyMC + ArviZ		  Full uncertainty quantification with MCMC

API	       FastAPI			  Production-ready, auto-documenting, async support

UI	       Streamlit		  Rapid prototyping, stakeholder-friendly

Container      Docker + docker-compose	  Reproducible deployment

Testing	       pytest			  Reliability assurance

Data	       pandas + numpy		  Efficient data manipulation

Visualization  matplotlib + seaborn	  Publication-quality charts


📁 Project Structure

text

├── api/

│   ├── __init__.py

│   ├── main.py            FastAPI application

│   └── schemas.py         Pydantic models

├── data/

│   ├── raw/               Original synthetic data

│   ├── processed/         Feature-engineered data

│   └── generate_synthetic_data.py

├── models/

│   ├── __init__.py

│   ├── train.py           Model training

│   ├── predict.py         Prediction utilities

│   └── artifacts/         Saved model files

├── notebooks/

│   └── 01_bayesian_pricing_model.ipynb

├── tests/

│   ├── __init__.py

│   ├── test_api.py

│   └── test_model.py

├── ui/

│   └── app.py             Streamlit dashboard

├── docker/

│   ├── Dockerfile.api

│   ├── Dockerfile.ui

│   └── docker-compose.yml

├── docs/

│   ├── API_DESIGN.md       Detailed API documentation

│   └── VALIDATION_PLAN.md  Model validation methodology

├── .gitignore

├── README.md

└── requirements.txt


📊 API Documentation

For complete API specifications, including:

All endpoints (/health, /predict, /batch, /model/info)

Request/response formats

Error handling

Rate limits

Authentication

Example clients

👉 See docs/API_DESIGN.md for full documentation


🧪 Validation & Testing

For detailed validation methodology, including:

Convergence diagnostics (R-hat, ESS)

Elasticity recovery plots

Price-profit curves with uncertainty

Posterior predictive checks

Feature effect analysis

Validation checklist and success criteria


👉 See docs/VALIDATION_PLAN.md for complete validation plan

bash

Run tests

pytest tests/ -v


Run with coverage

pytest tests/ --cov=api --cov=models --cov-report=html

👨‍💻 Author

Victor Makanju

GitHub | LinkedIn


📄 License

MIT License - feel free to use and modify for your own projects.


🙏 Acknowledgments

PyMC Labs for their excellent Bayesian modeling resources

FastAPI for the best Python API framework

Streamlit for making data apps accessible to everyone