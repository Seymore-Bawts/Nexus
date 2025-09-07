import datetime
import pytz
from flask import Flask, jsonify

# --- Application Initialization ---
app = Flask(__name__)

# --- API Logic ---
class TimeService:
    """
    A service class to encapsulate the logic for retrieving time information.
    """
    def __init__(self, timezone='UTC'):
        """Initializes the service with a specific timezone."""
        try:
            # We must handle timezone names that contain slashes, like 'America/New_York'.
            self.timezone = pytz.timezone(timezone.replace('_', '/'))
        except pytz.UnknownTimeZoneError:
            # Default to UTC if the provided timezone is invalid. This is robust design.
            self.timezone = pytz.timezone('UTC')

    def get_current_time_data(self):
        """Generates a dictionary containing the current time and timezone info."""
        now = datetime.datetime.now(self.timezone)
        return {
            'timezone': str(self.timezone),
            'current_datetime': now.isoformat(),
            'current_timestamp_utc': datetime.datetime.now(pytz.utc).timestamp()
        }

# --- API Routes (Endpoints) ---

# We add a default route to provide instructions. This is good API practice.
@app.route('/api/time', methods=['GET'])
def get_time_default():
    """Provides a default response or instructions for the API."""
    return jsonify({
        'message': 'This is the Time Service API.',
        'usage': "Append a timezone to the URL, e.g., /api/time/UTC or /api/time/America/New_York"
    })

# This is our new, dynamic route. The <path:timezone> syntax captures
# everything after /api/time/ as a variable named 'timezone'.
@app.route('/api/time/<path:timezone>', methods=['GET'])
def get_time_dynamic(timezone):
    """
    This handler takes the timezone from the URL, creates a TimeService
    instance with it, and returns the time data as a JSON response.
    """
    time_service = TimeService(timezone=timezone)
    time_data = time_service.get_current_time_data()
    return jsonify(time_data)

# --- Execution Block ---
if __name__ == '__main__':
    app.run(debug=True)