&#x20; Dynamic Pricing Engine for Electronics



\[!\[Python](https://img.shields.io/badge/Python-3.11-blue)]()

\[!\[FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)]()

\[!\[Bayesian](https://img.shields.io/badge/Bayesian-PyMC-orange)]()

\[!\[Docker](https://img.shields.io/badge/Docker-Ready-blue)]()



&#x20; The Problem

Electronics retailers lose millions using static pricing. A laptop priced at $999 might sell out during a holiday spike, while the same laptop sits unsold during a slow week. Competitors change prices dynamically, stealing customers and eroding margins.



&#x20; The Solution

A Bayesian pricing engine that:

\- Learns price elasticity for each product category

\- Accounts for competitor prices, product age, and seasonality

\- Quantifies uncertainty so you never trust a bad recommendation

\- Delivers prices via API or simple UI in milliseconds



&#x20;Tech Stack

| Layer | Technology |

|-------|------------|

| Modeling | PyMC + scikit-learn |

| API | FastAPI |

| UI | Streamlit |

| Container | Docker |

| Testing | pytest |



Quick Start (Coming Soon)

```bash

&#x20;Once built:

docker-compose up



Project Structure

├── api/          # FastAPI service

├── data/         # Raw and processed data

├── docker/       # Dockerfiles

├── models/       # Training and prediction

├── notebooks/    # Exploratory analysis

├── tests/        # Unit tests

└── ui/           # Streamlit interface



👨‍💻 Author

Victor Makanju

