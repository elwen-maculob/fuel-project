# Fuel Route Optimizer API 🚚⛽

A high-performance Django REST API that calculates driving routes across the USA, identifies optimal and cost-effective fuel stops along the route based on real fuel price data, and computes total fuel expenses.

---

## 📌 Project Overview

This project solves the challenge of route-based fuel optimization for long-distance transport within the USA. Given a starting point and destination, the API fetches the route geometry using the **OSRM Routing API**, cross-references coordinates against a dataset of US fuel stations, and determines the most cost-effective fueling strategy under specific vehicle constraints.

### **Key Features**
- **Single-Call Routing:** Uses OSRM to retrieve total distance and route geometry efficiently, minimizing external API overhead.
- **Geospatial Proximity Filtering:** Filters stations based on distance from the exact route path.
- **Performance Optimization:** Features coordinate sampling (`[::25]`) on route geometries to prevent timeouts on long cross-country requests (e.g., NY to SF).
- **Fast Data Access:** Implements class-based CSV parsing with lazy loading and in-memory memoization.
- **Vehicle Constraints:** Evaluates fuel stops based on a **500-mile vehicle range** and **10 MPG fuel efficiency**.

---

## 🛠️ Tech Stack

- **Framework:** Django, Django REST Framework (DRF)
- **External APIs:** OSRM (Open Source Routing Machine), Nominatim Geocoder
- **Data Handling:** Python CSV Parser, JSON Caching
- **Testing & API Client:** Insomnia / Postman

---

## 🚀 Getting Started

### **Prerequisites**
- Python 3.10+
- `pip` package manager

### **Installation**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/elwen-maculob/fuel-project.git
   cd fuel-project
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django djangorestframework requests
   ```

4. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be live at `http://127.0.0.1:8000/api/optimize/`.

---

## 📖 API Reference

### **Endpoint:** `GET /api/optimize/`

Calculates driving route metrics, fuel stops, and total cost.

#### **Query Parameters**
| Parameter | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `start` | `string` | **Yes** | Starting city/state or address | `New York, NY` |
| `finish` | `string` | **Yes** | Destination city/state or address | `Miami, FL` |

---

### **Sample Request & Response**

#### Request:
```http
GET http://127.0.0.1:8000/api/optimize/?start=New%20York,%20NY&finish=Miami,%20FL
```

#### Response (`200 OK`):
```json
{
  "total_distance_miles": 1279.55,
  "stops": [
    {
      "station_name": "DELAWARE TRUCK PLAZA",
      "city": "New Castle",
      "state": "DE",
      "price_per_gallon": 3.45,
      "lat": 39.6159851,
      "lon": -75.662956
    }
  ],
  "total_cost": 441.45
}
```

---

## 🧪 Testing with Insomnia

An exported Insomnia API collection is included directly in the root directory:
- `Insomnia_collection.json`

To test the endpoints:
1. Open Insomnia.
2. Go to **Import** -> **From File**.
3. Select `Insomnia_collection.json` to load pre-configured requests.

---

## 📁 Repository Architecture

```text
Fuel_Project/
├── fuel_project/          # Project configurations (settings, urls, wsgi)
├── route_app/             # Main Django app
│   ├── apps.py            # Application configuration
│   ├── urls.py            # Route mappings
│   ├── views.py           # APIView request validation & handling
│   ├── geocoding_routing.py # OSRM integration & distance calculation
│   ├── csv_parser_fp.py   # Dataset loading & memoized caching
│   └── fuel_calculator.py # Core optimization algorithm
├── Insomnia_collection.json # Exported API tests
├── fuel_prices.csv        # US Fuel Price Dataset
├── manage.py
└── README.md
```