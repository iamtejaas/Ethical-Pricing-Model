from flask import Flask, render_template, request
from model_updated import assess_price
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# In-memory prediction history
history = []
last_result=None

# Load dropdown options from CSV
try:
    df = pd.read_csv("ethical_pricing_mock_dataset_extended.csv")
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    category_items = df.groupby("item_category")["item_name"].unique().apply(list).to_dict()
    sorted_categories = sorted(category_items.keys())
    unique_cities = sorted(df["city"].unique().tolist())
except Exception as e:
    print("Error loading dropdown data:", e)
    category_items = {}
    sorted_categories = []
    unique_cities = []

from flask import Flask, render_template, request, redirect, url_for

from flask import session
import json

app.secret_key = 'your_secret_key'  # You must set a secret key for sessions

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected_category = request.form.get("item_category")
        selected_item = request.form.get("item_name")
        selected_city = request.form.get("city")

        if selected_category and selected_item and selected_city:
            result = assess_price(selected_category, selected_item, selected_city)
            # Save result in session as JSON string (if complex)
            session['last_result'] = json.dumps(result)
            # Save selected values too if you want to prefill after redirect
            session['selected_category'] = selected_category
            session['selected_item'] = selected_item
            session['selected_city'] = selected_city

            # Save history as before
            history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "category": selected_category,
                "item": selected_item,
                "city": selected_city,
                "predicted_price": result.get("predicted_price"),
                "fair_label": result.get("fair_label")
            })

            # Redirect after POST
            return redirect(url_for('index'))

    # GET request: retrieve and pop result from session
    last_result_json = session.pop('last_result', None)
    selected_category = session.pop('selected_category', None)
    selected_item = session.pop('selected_item', None)
    selected_city = session.pop('selected_city', None)

    result = json.loads(last_result_json) if last_result_json else None

    return render_template("index.html",
                           categories=sorted_categories,
                           category_items=category_items,
                           cities=unique_cities,
                           category=selected_category,
                           item_name=selected_item,
                           city=selected_city,
                           result=result)


@app.route("/get_items_for_category", methods=["POST"])
def get_items_for_category():
    category = request.form.get("category")
    if category and category in category_items:
        return category_items[category]
    return []

@app.route("/history")
def view_history():
    return render_template("history.html", history=history)

@app.route("/compare", methods=["POST"])
def compare():
    try:
        category = request.form.get("comp_category")
        item = request.form.get("comp_item")
        selected_cities = request.form.getlist("compare_cities")

        if not category or not item or not selected_cities:
            return "Please select category, item, and cities.", 400

        if len(selected_cities) > 10:
            return "You can compare a maximum of 5 cities.", 400

        filtered_df = df[
            (df["item_category"] == category) &
            (df["item_name"] == item) &
            (df["city"].isin(selected_cities))
        ]

        if filtered_df.empty:
            return "No data available for comparison.", 404

        # Group stats
        comparison = filtered_df.groupby("city")["base_price"].agg(["min", "max", "mean"]).reset_index()
        comparison_html = comparison.to_html(index=False, float_format="₹{:,.2f}".format, classes="stats-table")

        # Optional: Bar plot of mean prices
        import matplotlib.pyplot as plt
        import seaborn as sns
        plt.figure(figsize=(8, 5))
        sns.barplot(x="city", y="mean", data=comparison, palette="coolwarm")
        plt.title(f"Average Price Comparison for '{item}'")
        plt.ylabel("Mean Price")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plot_path = "static/compare_plot.png"
        plt.savefig(plot_path)
        plt.close()

        # HTML response
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Price Comparison</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(to right top, #f4f7f8, #d0e9ff, #138dc5);
                    padding: 40px;
                }}
                .container {{
                    max-width: 900px;
                    margin: auto;
                    background: #ffffffcc;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                }}
                h2 {{
                    text-align: center;
                    color: #01579b;
                    margin-bottom: 20px;
                }}
                .stats-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                .stats-table th, .stats-table td {{
                    padding: 12px;
                    text-align: center;
                    border: 1px solid #ddd;
                }}
                .stats-table th {{
                    background-color: #0288d1;
                    color: white;
                }}
                .stats-table tr:nth-child(even) {{
                    background-color: #f2f9fc;
                }}
                .stats-table tr:hover {{
                    background-color: #e1f5fe;
                }}
                .back-button {{
                    margin-top: 30px;
                    display: inline-block;
                    background: #0288d1;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: bold;
                }}
                img {{
                    display: block;
                    margin: 30px auto;
                    max-width: 100%;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Price Comparison for {item}</h2>
                {comparison_html}
                <img src="/{plot_path}" alt="Comparison Graph">
                <div style="text-align: center;">
                    <a href="/" class="back-button">⬅ Back to Home</a>
                </div>
            </div>
        </body>
        </html>
        """
        return html

    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route('/about')
def about():
    return render_template("about.html")

from flask import make_response

@app.route("/download_result", methods=["GET"])
def download_result():
    global last_result  # Make sure you store the latest result in a global variable
    if not last_result:
        return "No result available to download.", 400

    output = f"""Prediction Summary for {last_result.get('item_name', 'Item')}

🔮 Predicted Price: ₹{last_result['predicted_price']}
⚖️ Fairness Label: {last_result['fair_label']}
📊 Tier-3 Max Suggested Price: ₹{last_result['tier3_max']}
📉 Price Prediction MSE: {last_result['mse_price']}
✅ Fairness Accuracy: {round(last_result['fairness_accuracy'] * 100, 2)}%
💰 Avg Market Price: ₹{last_result['avg_market_price']}
🌿 Sustainability Score: {last_result['sustainability']}
📊 Local Demand Index: {last_result['local_demand']}
🏭 Production Cost: ₹{last_result['production_cost']}
📈 Profit Margin: {round(last_result['profit_margin'] * 100, 2)}%
💵 Fair Wage Multiplier: {last_result['wage_score']}
"""

    response = make_response(output)
    response.headers["Content-Disposition"] = "attachment; filename=ethical_price_result.txt"
    response.headers["Content-Type"] = "text/plain"
    return response


if __name__ == "__main__":
    app.run(debug=True)
