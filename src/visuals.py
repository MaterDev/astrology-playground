import os
import jyotichart
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from .utils import theme_log

SIGNS_STANDARD = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
MAP_SIGN_NAME = {"Sagittarius": "Saggitarius", "Aries": "Aries", "Taurus": "Taurus", "Gemini": "Gemini", "Cancer": "Cancer", "Leo": "Leo", "Virgo": "Virgo", "Libra": "Libra", "Scorpio": "Scorpio", "Capricorn": "Capricorn", "Aquarius": "Aquarius", "Pisces": "Pisces"}

# Use reliable ASCII abbreviations to avoid rendering issues (white squares)
PLANET_SYMBOL_MAP = {
    "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
    "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke"
}

def generate_visual_chart(chart_obj, title, filename, output_dir, person_name):
    """Generates North Indian SVG and converts to PNG."""
    try:
        if hasattr(chart_obj, 'ascendant'):
            asc_sign = chart_obj.ascendant.sign
        elif hasattr(chart_obj, 'houses') and len(chart_obj.houses) > 0:
            asc_sign = chart_obj.houses[0].sign
        else:
            return None
            
        v_chart = jyotichart.NorthChart(title, person_name)
        
        # Disable aspect symbols to remove Unicode white squares
        v_chart.updatechartcfg("aspect-visibility", False)
        
        v_chart.set_ascendantsign(MAP_SIGN_NAME.get(asc_sign, asc_sign))
        
        for h_idx, house in enumerate(chart_obj.houses):
            for occupant in house.occupants:
                p_name = occupant.celestial_body
                symbol = PLANET_SYMBOL_MAP.get(p_name, p_name[:2])
                v_chart.add_planet(p_name, symbol, h_idx + 1)

        svg_path = os.path.join(output_dir, f"{filename}.svg")
        png_path = os.path.join(output_dir, f"{filename}.png")
        v_chart.draw(output_dir, filename)
        
        if os.path.exists(svg_path):
            with open(svg_path, "r", encoding="utf-16") as f:
                content = f.read()
            new_content = '<?xml version="1.0" encoding="UTF-8"?>\n' + content.replace('charset="utf-16"', '')
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            
            drawing = svg2rlg(svg_path)
            renderPM.drawToFile(drawing, png_path, fmt="PNG")
            
        theme_log("fox", f"Rendered clean {title} (Aspects Hidden)")
        return png_path
    except Exception as e:
        theme_log("error", f"Visual distortion in {title}: {e}")
        return None
