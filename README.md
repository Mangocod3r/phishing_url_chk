# Phishing URL Detection System

A machine learning-based web application that detects and classifies URLs as safe or potentially malicious (phishing) websites.

## Features

- Real-time URL classification using machine learning
- RESTful API endpoints for programmatic access
- Cache system for improved performance
- Comprehensive statistics tracking
- Modern web interface with clear results presentation

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

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
