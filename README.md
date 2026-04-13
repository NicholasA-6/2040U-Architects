# Watch Cataloging System - The Architects
The Watch Catalog System is a cataloging application built for browsing, managing, and discovering watches. The system is a catalogue and does not include buying, selling, or marketplace functionality, features a site like Amazon or Ebay have.
## Group Members
Fawzan Shaikh – Technical Manager  
Nick Allan – Project Manager  
Rafay Farooqui – Backend Lead  
Qadeer Khan – Frontend Lead  
Liam Sheridan – Software Quality Lead
## Installation & Running

## Live Demo
https://two040u-architects-watch-catalogue.onrender.com

## Run Locally
1. pip install -r requirements.txt
2. python app.py
3. Open http://127.0.0.1:5000

Optional (Windows/Linux build scripts available in /scripts)

User-generated data (wishlists and reviews) is stored in CSV files; however, due to deployment limitations on the hosting platform, these changes are not guaranteed to persist across server restarts or redeployments.


## Notable Features
Role-based access control (Admin vs User)  
Add, edit, and delete watches (Admin only)  
Search and filter watches  
Login/logout system  
Clean and consistent user interface  
Product is strictly a catalogue, not a marketplace, so no purchasing system or need to mention retailers  
Wishlist, comparison, recommendations

## Project Structure

```
├── app.py                          # Main Flask application
├── backend.py                      # Backend logic and data handling
├── requirements.txt                # Python dependencies for deployment
├── Procfile                        # Render deployment configuration
├── data/                           # Runtime data files
│   ├── users.csv                   # User credentials and roles
│   ├── watches.csv                 # Watch catalogue data
│   ├── reviews.csv                 # Product reviews data
│   └── testdata.csv                # Sample test dataset
├── Diagrams/                       # Project diagrams and documentation
│   └── UML_Diagram.pdf             # UML class diagram
├── scripts/                        # Build and utility scripts
│   ├── build.sh                    # Unix/Linux build script
│   └── build.bat                   # Windows build script
├── templates/                      # HTML view templates
│   ├── catalogue.html              # Main catalogue page
│   └── login.html                  # Login page
├── test_backend.py                 # Backend test suite
├── test_frontend.py                # Frontend test suite
└── README.md                       # Project documentation
```

