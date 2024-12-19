import pandas as pd  # Add this line
import matplotlib.pyplot as plt

# Load and visualize Dollar Index data
dxy_data = pd.read_csv("historical_data/Dollar_Index_(DXY).csv")
plt.plot(dxy_data['Date'], dxy_data['Close'])
plt.title("Dollar Index (DXY) - Closing Prices")
plt.xlabel("Date")
plt.ylabel("Price")
plt.xticks(rotation=45)
plt.show()
