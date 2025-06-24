
# 🧠 AI Ethical Price Prediction

An Ethical Pricing Prediction Model that uses machine learning to determine fair and sustainable product prices, considering factors like production costs, fair wages, and environmental impact.

---

## 📊 Ethical Pricing Prediction Model

This repository houses the code and web app for an Ethical Pricing Prediction Model, designed to determine fair and sustainable prices for various products. The project leverages machine learning to integrate crucial ethical considerations such as production costs, fair wages, environmental sustainability, and local market dynamics into pricing strategies.

---

## 🧠 Project Overview

The primary goal of this project is to create a robust model that can suggest an ethical price range and a specific ethical price for products. This is achieved by training a **RandomForestRegressor** on a synthetic dataset that simulates real-world pricing factors. The model helps businesses establish prices that are not only competitive but also socially responsible and environmentally conscious.

---

##  ✨ Key Features

- **Ethical Price Prediction**: Generates a recommended ethical price and an acceptable price range for a given product, category, and city.

- **Multi-factor Analysis**: Incorporates a wide array of factors including:
  - `production_cost`
  - `fair_wage_multiplier`
  - `sustainability_score`
  - `local_demand_index`
  - `market_avg_price_city`
  - `profit_margin_standard`
  - `regulatory_adjustment`

- **Machine Learning Powered**: Utilizes a RandomForestRegressor for its ability to handle complex relationships and provide accurate predictions.

- **Comprehensive Dataset**: Built upon `ethical_pricing_mock_dataset_extended.csv`, a detailed mock dataset containing diverse product entries, categories, and geographical locations.

- **Web Interface**: A Flask-based web application where users can input product details and get predictions, comparisons, and history.

- **Model Graphs**: Automatic generation of:
  - Price distribution plots
  - Marketplace comparisons
  - City-level trends

---

## 🧪 Model Details

- **Model**: RandomForestRegressor
- **Preprocessing**: Label Encoding for `item_category`, `item_name`, `city`
- **Target Variable**: `base_price`
- **Evaluation Metrics**:
  - Price MSE
  - Ethical Classification Accuracy
- **Persistence**: Notebooks save trained models and encoders for reuse
  
---


## ⚠️ Disclaimer
The Ethical Price Predictor estimates product prices by analyzing factors such as production cost, fair wage multipliers, sustainability, and demand. While the system leverages machine learning and fairness-driven metrics, all outputs are indicative and should be interpreted as supportive insights. Users are encouraged to apply their own judgment and consider additional data when making pricing-related decisions.

---

## 📁 Files in this Repository

```
ETHICAL PRICING MODEL/
├── .venv/                            # Virtual environment (optional, can be in .gitignore)
├── __pycache__/                      # Python cache files
├── app.py                            # Main Flask backend
├── ethical_pricing.py                # EDA, training, visualization
├── ethical_pricing_mock_dataset_extended.csv # Original dataset
├── model_updated.py                  # Prediction model
├── pricing_model.pkl                 # Final model
├── updates.ipynb                     # Any updates or exploratory notebooks
├── static/
│   ├── logos/                        # Company logos
│   │   ├── Ajio_Logo.png
│   │   ├── amazon_logo.jpg
│   │   ├── EBay_logo.png
│   │   ├── Flipkart_logo.png
│   │   ├── jio_mart_logo.png
│   │   ├── myntra_logo.png
│   │   ├── nykaa_new.jiff
│   │   ├── reliance_logo.png
│   │   ├── Snapdeal_logo.png
│   │   ├── tata_cliq_logo.png
│   ├── compare_plot.png
│   ├── plot_distribution.png
│   ├── plot_importance.png
│   ├── plot_local_demand.png
│   ├── plot_marketplace.png
│   ├── plot_price_distribution.png
│   ├── plot_trend.png
│   ├── plot.png
│   └── style.css                    # Styling for all HTML pages
├── templates/
│   ├── index.html                   # Main input page
│   ├── history.html                 # Prediction history
│   ├── about.html                   # About the project
│   └── result.html                  # Prediction output
└── README.md                        # Project overview

---

## ⚠️ Disclaimer
The Ethical Price Predictor estimates product prices by analyzing factors such as production cost, fair wage multipliers, sustainability, and demand. While the system leverages machine learning and fairness-driven metrics, all outputs are indicative and should be interpreted as supportive insights. Users are encouraged to apply their own judgment and consider additional data when making pricing-related decisions.
