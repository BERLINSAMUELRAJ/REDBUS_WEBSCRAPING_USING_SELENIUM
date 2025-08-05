# 🚌 Redbus Data Scraping & Visualization

## 📌 Overview

This project automates the extraction of bus route data from [Redbus](https://www.redbus.in/) using **Selenium**, stores the data in an **SQL database**, and provides a **Streamlit app** to visualize and filter the data interactively.

It supports:
- Multi-state scraping
- Dynamic page navigation
- Lazy loading
- Sub-tab clicks (e.g., APSRTC, KSRTC Buses)

---

## 🎯 Objective

- Scrape bus routes and detailed schedule info from Redbus.
- Store data in a structured SQL database.
- Visualize and filter the data with Streamlit.

---

## 🛠 Tech Stack

| Area            | Tool/Tech              |
|-----------------|------------------------|
| Web Scraping    | Selenium (Python)      |
| Data Storage    | SQLite / MySQL         |
| Visualization   | Streamlit              |
| Language        | Python                 |

---

## 📊 Data Extracted

- Route Name  
- Bus Name & Type  
- Departure Time  
- Duration  
- Arrival Time  
- Star Rating  
- Price  
- Seat Availability  

---

## 🗃 Database Schema

| Column Name        | Type            |
|--------------------|-----------------|
| id (Primary Key)   | INTEGER         |
| route_name         | TEXT            |
| route_link         | TEXT            |
| bus_name           | TEXT            |
| bus_type           | TEXT            |
| departing_time     | VARCHAR(100)    |
| duration           | TEXT            |
| reaching_time      | VARCHAR(100)    |
| star_rating        | FLOAT           |
| price              | FLOAT           |
| seat_availability  | INT             |

---

## 🚀 How It Works

1. **Scraping**:
   - Navigate Redbus by state
   - Extract route links
   - Click and load each route
   - Scroll to load all buses
   - Click sub-tabs for government buses
   - Scrape all bus details

2. **Database Integration**:
   - Store data in SQL (with duplicate handling)

3. **Streamlit App**:
   - Connect to database
   - Show all scraped data
   - Add filters (route, price, rating, etc.)

---

## 📈 Features

- Full automation of Redbus navigation
- Handles dynamic and lazy-loaded content
- Saves clean data in SQL
- Responsive, filterable dashboard in Streamlit

---

## 🧪 Future Enhancements

- Real-time scraping scheduler
- Map-based route visualization
- Filter by departure/arrival time
- Export to CSV/Excel

---

## 📷 Screenshots

> *(You can add screenshots of your Streamlit app here)*

---

## 💡 Use Cases

- Route planning
- Public transport analysis
- Competitor pricing research
- Travel app backend

---

## 📧 Contact

**[Your Name]**  
GitHub: [github.com/yourusername](https://github.com/yourusername)
