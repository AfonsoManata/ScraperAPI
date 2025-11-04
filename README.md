# 🐍 Scraper API

Python-based API that scrapes package data from the Aptoide app store (https://en.aptoide.com/) and exposes it through a REST endpoint.


1 - This API exposes an endpoint:
```
GET /aptoide?package_name=<package_id>
```

2 - This endpoint:
  - Accepts a package name as a query parameter (e.g. com.facebook.katana).
  - Scrapes or fetch package details from Aptoide.
  - Returns all relevant metadata about the app in JSON format.

## 🧾 Example

Request:
```
GET /aptoide?package_name=com.facebook.katana
```

Response (JSON):
```
{
  "name": "Facebook",
  "size": "152.5 MB",
  "downloads": "2B",
  "version": "532.0.0.55.71",
  "release_date": "2025-09-30 17:06:59",
  "min_screen": "SMALL",
  "supported_cpu": "arm64-v8a",
  "package_id": "com.facebook.katana",
  "sha1_signature": "8A:3C:4B:26:2D:72:1A:CD:49:A4:BF:97:D5:21:31:99:C8:6F:A2:B9",
  "developer_cn": "Facebook Corporation",
  "organization": "Facebook Mobile",
  "local": "Palo Alto",
  "country": "US",
  "state_city": "CA"
}
```

## ⚙️ Setup Instructions

1. **Clone the repository**  
   ```
   git clone https://github.com/yourusername/aptoide-scraper-api.git
   ```
3. **Navigate into the project directory**  
   ```
   cd aptoide-scraper-api
   ```

5. **Create a virtual environment**  
   ```
   python3 -m venv venv
   ```
7. **Activate the virtual environment**  
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```

8. **Install dependencies**  
  ```
   pip install -r requirements.txt  
  ```
10. **Run the FastAPI server**  
  ```
  uvicorn src.main:app --reload
  ```
   The API will be available at http://127.0.0.1:8000
   <img width="1096" height="247" alt="image" src="https://github.com/user-attachments/assets/d7b73aa7-4787-49a3-bd1d-ad79f20fd0d6" />

12. **Test API**  
   - Add more tests and use pytest
   - http://127.0.0.1:8000/docs
<img width="1048" height="888" alt="image" src="https://github.com/user-attachments/assets/96955f4c-cfd7-4040-b283-76087cc129df" />

After completing these steps, your Aptoide Scraper API should be running locally and ready to handle requests.

## 🧠 **Design Decisions & Scalability Approaches**
- Rate Limiter.
- Focus on Error handling.
- Input Validation.
- Versioning.
- Descriptions and good documentation.

** 🎯 **Future Scalability Plans**
- Add caching (e.g., Redis) to avoid repeated scrapes for the same package.
- Deploy using containerization (Docker + Kubernetes) for scalability and reliability in production.
- Add more tests
- Make the scrapping logic more scalable and complete

