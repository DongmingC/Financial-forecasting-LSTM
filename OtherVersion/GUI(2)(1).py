import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import numpy as np
import train_LSTM as predictor

# Placeholder function for loading data
def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        data = pd.read_csv(file_path)
        return data
    else:
        return None

# Placeholder function for a simple model prediction
# In real use, replace this with your model's prediction logic
def predict_data(data):
    # Simulating prediction by shifting the close price up by a constant value
    # Replace this logic with actual model prediction
    print(data)
    predicted = predictor.train_model(data)
    return predicted

# Function to plot training and predicted data
def plot_data():
    data = load_data()
    if data is not None:
        data['Date'] = pd.to_datetime(data['Date'])
        predicted = predict_data(data)
        
        data.reset_index(inplace=True)
        # Creating the plot
        fig, ax = plt.subplots(figsize=(10, 5))
        actual_line, = ax.plot(data['Date'], data['Close'], label='Training Data', color='blue')
        predicted_line, = ax.plot(data['Date'], np.concatenate((data['Close'].to_numpy(),np.array(predicted))), label='Predicted Data', linestyle='--', color='orange')
        ax.set(title='Stock Data - Training and Predicted', xlabel='Date', ylabel='Price')
        ax.legend()
        
        # Text annotation for displaying the value
        text_annotation = ax.text(0.7, 0.9, '', transform=ax.transAxes)
        
        def on_move(event):
            if event.inaxes == ax:
                # Find nearest index of the x-data to the mouse position
                xdata = mdates.date2num(data['Date'])  # Convert dates to the correct format for comparison
                index = np.abs(xdata - event.xdata).argmin()
                try:
                    actual_value = data['Close'].iloc[index]
                    predicted_value = np.concatenate((data['Close'].to_numpy(),np.array(predicted)))[index]
                    text_annotation.set_text(f'Actual: {actual_value:.2f}\nPredicted: {predicted_value:.2f}')
                except IndexError:
                    # This can happen if the mouse is beyond the range of the data
                    text_annotation.set_text('')
                
                fig.canvas.draw_idle()

        # Connect the motion notify event to the on_move function
        fig.canvas.mpl_connect('motion_notify_event', on_move)
        
        # Displaying the plot in the GUI
        canvas = FigureCanvasTkAgg(fig, master=window)  # `window` is the tkinter window
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.draw()



# Create the main window
window = tk.Tk()
window.title("Stock Data Plotter")

# Create a button to load the data, train the model, and plot the data
plot_button = tk.Button(window, text="Load and Plot Stock Data", command=plot_data)
plot_button.pack(side=tk.TOP, pady=20)

# Start the GUI event loop
window.mainloop()
