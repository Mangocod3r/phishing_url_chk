# Phishing URL Detection System

A machine learning-based web application that detects and classifies URLs as safe or potentially malicious (phishing) websites.

## Features

- Real-time URL classification using machine learning
- RESTful API endpoints for programmatic access
- Cache system for improved performance
- Comprehensive statistics tracking
- Modern web interface with clear results presentation

## Working Flow

### URL Classification Process

1. **Input URL**
   - User submits a URL through the web interface or Chrome extension
   - The URL is validated and sanitized

2. **Feature Extraction**
   - The system extracts multiple features from the URL:
     - Domain analysis
     - IP address detection
     - URL length and structure
     - Suspicious keywords
     - SSL certificate status
     - Domain registration details
     - Page content analysis

3. **Machine Learning Classification**
   - Features are processed and normalized
   - The trained model (Gradient Boosting Classifier) predicts the URL's safety
   - Confidence scores are calculated for both safe and unsafe predictions

4. **Caching Layer**
   - Results are cached for 24 hours
   - Cache hit rate and performance metrics are tracked
   - Cache invalidation occurs when model is updated

5. **Response Generation**
   - Returns a JSON response with:
     - Safety classification (safe/unsafe)
     - Confidence percentage
     - URL analysis details
     - Cache status

### API Endpoints

- `POST /api/check_url`
  - Accepts: URL to check
  - Returns: Safety classification and confidence scores
  - Example response:
  ```json
  {
    "url": "example.com",
    "safe": true,
    "confidence": 95.2,
    "unsafe_confidence": 4.8,
    "cache_hit": true
  }
  ```

- `GET /api/cache_stats`
  - Returns cache performance metrics
  - Includes: cache hits, requests served, average time saved
  - Example response:
  ```json
  {
    "requests_served": 1234,
    "cache_hits": 850,
    "avg_time_saved": 0.15,
    "estimated_cost_savings": "$17.00",
    "bandwidth_saved_kb": 850
  }
  ```

### Performance Optimization

- **Caching Strategy**
  - Results cached for 24 hours
  - Cache invalidation on model updates
  - Cache hit rate monitoring

- **Resource Management**
  - Efficient feature extraction
  - Optimized model loading
  - Memory usage monitoring

- **Scalability**
  - Designed for serverless deployment
  - Automatic scaling based on load
  - Efficient resource utilization

## Tech Stack

- Backend: Python Flask
- Machine Learning: Scikit-learn
- Data Processing: Pandas, NumPy
- API: RESTful endpoints with CORS support
- Environment Management: python-dotenv

## Project Structure

```
phishing_url_proj/
├── app.py              # Main Flask application
├── feature.py          # Feature extraction logic
├── advanced_features.py # Advanced feature extraction
├── cache_manager.py    # Cache management system
├── cache_metrics.py    # Cache performance metrics
├── pickle/            # Machine learning model
├── templates/         # HTML templates
├── static/            # Static files (CSS, JS)
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
└── README.md          # Project documentation
```

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and configure as needed
5. Run the application:
   ```bash
   python app.py
   ```

## API Endpoints

- `GET /` - Main web interface
- `POST /api/check_url` - URL classification API
- `GET /api/cache_stats` - Cache statistics

## Environment Variables

Create a `.env` file with the following variables:

```env
# Flask Configuration
HOST=0.0.0.0
PORT=5001
DEBUG=True

# Model Configuration
MODEL_PATH=pickle/model.pkl
```

## Usage

1. Access the web interface at `http://localhost:5001`
2. Enter a URL to check
3. View the classification results and confidence scores

### Using with Chrome Extension

This API can be integrated with a Chrome extension for real-time URL safety checking. The extension code is located at: [url-safety-checker-extension](https://github.com/Mangocod3r/url-safety-checker-extension)

#### Integration Steps

1. Deploy this API to a production environment (like Vercel or any other hosting service)
2. Clone the Chrome extension repository:
   ```bash
   git clone https://github.com/Mangocod3r/url-safety-checker-extension.git
   ```
3. Configure the extension's API endpoint:
   - Open `src/background.js` in the extension directory
   - Update the `API_ENDPOINT` constant with your deployed API URL
4. Load the extension in Chrome:
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode" in the top right
   - Click "Load unpacked" and select the extension directory

#### Extension Features

- Real-time URL safety checking as you type
- Visual indicators for safe/unsafe URLs
- Confidence score display
- Cache support for faster repeated checks
- Automatic updates for cached results

The extension uses the `/api/check_url` endpoint to get safety information about URLs. It caches results locally to improve performance and reduce API calls.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
