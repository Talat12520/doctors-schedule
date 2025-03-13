from flask import Flask, request, render_template, send_file
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# Load the dataset from Excel
data = pd.read_excel('doctors_data.xlsx')

# Convert Login Time and Logout Time to datetime, handling errors
data['Login Time'] = pd.to_datetime(data['Login Time'], errors='coerce')
data['Logout Time'] = pd.to_datetime(data['Logout Time'], errors='coerce')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_doctors', methods=['POST'])
def get_doctors():
    input_time = request.form['time']
    input_time = datetime.strptime(input_time, '%H:%M').time()

    # Filter doctors based on login time
    filtered_doctors = data[data['Login Time'].dt.time == input_time]

    # Prepare the data for exporting
    if not filtered_doctors.empty:
        output_file = 'filtered_doctors.csv'
        filtered_doctors.to_csv(output_file, index=False)  # Save as CSV
        return send_file(output_file, as_attachment=True)

    return render_template('results.html', message="No doctors found for the specified time.")

if __name__ == '__main__':
    app.run(debug=True)