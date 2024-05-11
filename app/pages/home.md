# Luzcast

![logo](../assets/powerpricelogo.png)
Luzcast is a power price forecasting project designed to attempt predicting current day power prices across the ERCOT (Electric Reliability Council of Texas) regions. By leveraging historical data on load, wind, and solar energy, alongside historical pricing information, this tool provides power price forecasts.


## Key Features 
For now, we attempt to predict these prices based on the following historical data:
* **Historical Data Training**: Models are trained using historical datasets from ERCOT, including load metrics and renewable energy production (wind and solar), as well as historical power prices.
* **Price Prediction**: Utilizes trained models to predict current day power prices based on current conditions.
* **Price and data visualization**: Features interactive graphs displaying power prices across various ERCOT regions.

**This are the current features, there can be additions in the future**

## How It Works
1. **Data Collection**: Aggregate historical data from ERCOT on power load and prices, as well as wind and solar energy production.
    - More data features can be added for better trend understanding and forecasting
2. **Model Training**: Train predictive models using this historical data to understand and forecast power price trends.
3. **Price Forecasting**: Use these models daily to predict power prices for the current day, ensuring forecasts are revelant.
    - Data for predictions will come from ERCOT rtd
4. **Visualization**: Display the forecasted prices through a series of dynamic graphs, which detail the pricing trends across different ERCOT regions.