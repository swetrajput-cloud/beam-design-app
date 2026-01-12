📐 RCC Beam Design Web Application

A professional Flask-based civil engineering web app for designing singly reinforced RCC beams according to IS 456.
The app calculates required steel, number of bars, shear check, and stirrup spacing with a clean, interactive UI.

🚀 Features

Calculate Ast (area of steel)

Find number of bars (16 mm dia)

Check under-reinforced condition

Compute shear stress (τᵥ) and τc

Design stirrups and spacing

Load and display beam data from Excel

Modern responsive UI

🛠 Tech Stack
Layer	Technology
Backend	Python, Flask
Calculations	Engineering formulas (IS 456)
Data	Excel (Pandas, OpenPyXL)
Frontend	HTML5, CSS3 (Flexbox), JavaScript
Hosting	GitHub
📂 Project Structure
beam-design-app/
│
├── app.py
├── requirements.txt
│
├── data/
│   └── singly_reinforced_beam_design.xlsx
│
├── static/
│   └── css/
│       └── style.css
│
└── templates/
    ├── index.html
    ├── about.html
    ├── contact.html
    └── calculator.html

⚙️ How to Run Locally
1️⃣ Clone the repository
git clone https://github.com/swetrajput-cloud/beam-design-app.git
cd beam-design-app

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the application
python app.py

4️⃣ Open in browser
http://127.0.0.1:5000

🧮 How to Use

Open the Calculator page

Enter:

Beam width

Depth

Cover

Concrete grade

Steel grade

Design moment

Click Calculate

The app will display:

Effective depth

Ast required & provided

Number of bars

% steel

Shear check

Stirrup spacing

📊 Example

Input:

Beam width = 300 mm

Depth = 500 mm

Concrete = M25

Steel = Fe415

Moment = 100 kN-m

Output:

Ast required

No. of bars

Shear check

Stirrup spacing

(All computed automatically by the app)

👨‍💻 Author

Swet Raj
Civil Engineering | Python | Structural Design

GitHub: https://github.com/swetrajput-cloud

📜 License

This project is open-source and free to use for learning and academic purposes.
