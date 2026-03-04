from datetime import datetime
from jyotishganit import calculate_birth_chart
from .utils import theme_log

def calculate_full_chart(user_data):
    """Encapsulates high-precision NASA JPL ephemeris calculations."""
    theme_log("wind", f"Calibrating ephemeris for {user_data['name']}...")
    
    try:
        birth_date = datetime.strptime(user_data['birth_date'], '%Y-%m-%d %H:%M:%S')
        chart = calculate_birth_chart(
            birth_date=birth_date,
            latitude=user_data['latitude'],
            longitude=user_data['longitude'],
            timezone_offset=user_data['timezone_offset'],
            name=user_data['name']
        )
        theme_log("stars", f"Ayanamsa fixed at {chart.ayanamsa.value:.4f}° ({chart.ayanamsa.name})")
        return chart, birth_date
    except Exception as e:
        theme_log("error", f"Calculation drift: {e}")
        raise
