# Bio-Informed Daily Life

A web application to help users make informed decisions based on biology in everyday life.

## Features

- **Air Quality Insights**: Monitor VOCs with MQ-135 sensor data.
- **Food Tips**: Nutrition and spoilage advice.
- **Body Signals**: Circadian rhythm and biometrics.

## Setup

1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the Flask app:
   ```
   python app.py
   ```

3. Open your browser to `http://127.0.0.1:5000/`

## SCSS Compilation

The styles are written in SCSS. To compile `static/style.scss` to `static/style.css`, install a SCSS compiler like `sass`:

```
npm install -g sass
sass static/style.scss static/style.css
```

Or use an online compiler.

## Hardware Integration

- Connect your UNO R4 and MQ-135 sensor.
- Modify `app.py` to read data from a CSV file or serial connection.
- Update API endpoints to use real sensor data.

## Project Structure

- `app.py`: Flask backend with API endpoints.
- `templates/`: HTML templates.
- `static/`: SCSS and JS files.
- `requirements.txt`: Python dependencies.