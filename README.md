# Sentinel HealthOS 6.0 🌍⚕️

Sentinel HealthOS is an integrated public health intelligence platform designed to monitor climate risk, environmental variables, and disease outbreak dynamics across South Africa's provinces.

## API Endpoint Reference

| Category | Endpoint | Description |
| :--- | :--- | :--- |
| **System** | `GET /` | API status and version health check |
| **Provinces** | `GET /api/provinces/risk-profiles` | Provincial risk levels and capacity metrics |
| **Earth Observation** | `GET /api/earth-obs/metrics/{province_code}` | NDVI, land surface temp, precipitation & cloud metrics |
| **Surveillance** | `GET /api/surveillance/predictions/{province_code}` | Outbreak prediction risk scores & primary drivers |
| **Climate** | `GET /api/climate/vulnerability/{province_code}` | Heat wave, drought, and flood susceptibility metrics |
| **Air Quality** | `GET /api/air-quality/metrics/{province_code}` | AQI, PM2.5, PM10, and NO2 exposure levels |

## Local Development Setup

```bash
# Clone the repository
git clone [https://github.com/6-0-Industries/Sentinel-healthos.git](https://github.com/6-0-Industries/Sentinel-healthos.git)
cd Sentinel-healthos

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn src.api.main:app --reload
