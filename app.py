from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)
        
        # Extract company name from the uploaded file name
        company_name = file.filename.split('.')[0]

        # Convert Date column to datetime format
        df['Date'] = pd.to_datetime(df['Date'])

        # Calculate the 20-day moving average
        df['20-day MA'] = df['Close'].rolling(window=20).mean()

        # Generate chart
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date'], df['Close'], label='Close Price')
        plt.plot(df['Date'], df['20-day MA'], label='20-day Moving Average')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(f'Stock Analysis for {company_name}')
        plt.legend()
        highest_price = df['Close'].max()
        lowest_price = df['Close'].min()
        highest_date = df[df['Close'] == highest_price]['Date'].iloc[0]
        lowest_date = df[df['Close'] == lowest_price]['Date'].iloc[0]

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        chart_base64 = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()

        # Generate explanation based on the chart
        explanation = f"This chart displays the stock's closing prices and the 20-day moving average over time. It provides insights into the price trends of {company_name} stock."

        # Render the results page with the generated chart, company name, and explanation
        return render_template('results.html', chart_base64=chart_base64, explanation=explanation, company_name=company_name, highest_price=highest_price, lowest_price=lowest_price,highest_date=highest_date, lowest_date=lowest_date)

if __name__ == '__main__':
    app.run(debug=True)
