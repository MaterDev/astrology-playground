from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime
import os
from .utils import strip_emojis, theme_log

class PrimatifPDF(FPDF):
    def __init__(self, user_name):
        super().__init__()
        self.user_name = user_name

    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(128)
            self.cell(0, 10, f'Primatif Astrology - {self.user_name}', align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapter_title(self, label):
        self.set_font('helvetica', 'B', 14)
        self.set_fill_color(230, 240, 230)
        self.cell(0, 10, f" {label}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        self.ln(4)

    def sub_title(self, label):
        self.set_font('helvetica', 'B', 12)
        self.set_text_color(50, 100, 50)
        self.cell(0, 10, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0)

def generate_report(chart, birth_date, user_data, image_paths, output_path):
    """Compiles the final Primatif PDF document with detailed methodology."""
    theme_log("root", f"Weaving the ultimate document for {user_data['name']}...")
    
    pdf = PrimatifPDF(user_data['name'])
    
    # --- COVER PAGE ---
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 32)
    pdf.ln(60)
    pdf.cell(0, 20, 'PRIMATIF ASTROLOGY', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('helvetica', '', 18)
    pdf.cell(0, 15, f'ULTIMATE COSMIC BLUEPRINT', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)
    pdf.set_font('helvetica', 'B', 22)
    pdf.cell(0, 15, user_data['name'].upper(), align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('helvetica', 'I', 12)
    pdf.cell(0, 10, f'Compiled on {datetime.now().strftime("%B %d, %Y")}', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # --- METHODOLOGY PAGE ---
    pdf.add_page()
    pdf.chapter_title('Methodology & Astronomical Framework')
    
    methodology = (
        "This report is generated using a specific configuration of the Vedic (Jyotish) system. "
        "It is important to note that results may vary between different practitioners and software "
        "engines due to variations in the underlying astronomical data and chosen parameters.\n\n"
        "1. Ephemeris (Data Source): We utilize the NASA JPL DE421 ephemeris. This is a professional-grade, "
        "high-precision data set used by space agencies for planetary tracking. It provides arc-second "
        "accuracy for planetary positions.\n\n"
        "2. Ayanamsa (Zodiac Offset): Unlike Western Astrology (Tropical), Vedic Astrology uses the Sidereal "
        "zodiac, which accounts for the wobble of the Earth's axis (precession). This report uses the "
        "'True Chitra Paksha' Ayanamsa. This is often the preferred choice for high-precision scientific "
        "astrology, though other systems (like Lahiri or Raman) may shift planetary degrees by a small margin.\n\n"
        "3. House System: We use the 'Sripathi' house system for calculations and the traditional "
        "Whole Sign house system for visual representation. This choice prioritizes the clear "
        "interaction between planetary signs and their respective areas of life.\n\n"
        "4. Sidereal Framework: All positions are sidereal. If you compare this to a Western Tropical "
        "chart, your placements will likely be shifted backwards by approximately 24 degrees."
    )
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 5, methodology)
    pdf.ln(5)

    # --- DATA PAGE ---
    pdf.add_page()
    pdf.chapter_title('Astronomical Coordinates & Foundation')
    details = (f"Origin Date: {birth_date.strftime('%B %d, %Y')}\n"
               f"Origin Time: {birth_date.strftime('%H:%M:%S')}\n"
               f"Latitude: {user_data['latitude']}N | Longitude: {user_data['longitude']}W\n"
               f"Ayanamsa Value: {chart.ayanamsa.value:.4f} degrees\n"
               f"System: Sidereal / True Chitra Paksha")
    pdf.set_font('helvetica', '', 11)
    pdf.multi_cell(0, 6, details)
    pdf.ln(5)

    pdf.chapter_title('Panchanga (The Five Limbs)')
    p = chart.panchanga
    pan_text = (f"Tithi (Lunar Day): {p.tithi}\n"
                f"Nakshatra (Star): {p.nakshatra}\n"
                f"Yoga (Energy): {p.yoga}\n"
                f"Karana (Action): {p.karana}\n"
                f"Vaara (Weekday): {p.vaara}")
    pdf.multi_cell(0, 6, pan_text)
    
    pdf.chapter_title('Chart Legend (Abbreviations)')
    legend = "Su: Sun | Mo: Moon | Ma: Mars | Me: Mercury | Ju: Jupiter | Ve: Venus | Sa: Saturn | Ra: Rahu | Ke: Ketu"
    pdf.set_font('helvetica', 'I', 10)
    pdf.cell(0, 8, legend, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # --- PLANETARY PAGE ---
    pdf.add_page()
    pdf.chapter_title('Planetary Analysis (Shadbala & Positions)')
    pdf.set_font('courier', 'B', 10)
    cols = [40, 40, 40, 40, 30]
    headers = ['Planet', 'Sign', 'Degree', 'Strength', 'Bindu']
    for i, h in enumerate(headers):
        pdf.cell(cols[i], 8, h, 1)
    pdf.ln()
    
    pdf.set_font('courier', '', 10)
    planets = sorted(chart.d1_chart.planets, key=lambda x: x.celestial_body)
    bhav_bindus = chart.ashtakavarga.bhav
    for p_obj in planets:
        p_name = p_obj.celestial_body
        p_sign = p_obj.sign
        sb = p_obj.shadbala.get('Shadbala', {}).get('Total', 0)
        bindu = str(bhav_bindus.get(p_name, {}).get(p_sign, "-"))
        pdf.cell(cols[0], 8, p_name, 1)
        pdf.cell(cols[1], 8, p_sign, 1)
        pdf.cell(cols[2], 8, f"{p_obj.sign_degrees:.2f}", 1)
        pdf.cell(cols[3], 8, f"{sb:.2f}", 1)
        pdf.cell(cols[4], 8, bindu, 1)
        pdf.ln()

    strongest = max([p for p in planets if p.celestial_body not in ['Rahu', 'Ketu']], key=lambda x: x.shadbala.get('Shadbala', {}).get('Total', 0))
    pdf.ln(5)
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, f"Strongest Functional Planet: {strongest.celestial_body} ({strongest.shadbala.get('Shadbala', {}).get('Total', 0):.2f})")

    # --- ASHTAKAVARGA PAGE ---
    pdf.add_page()
    pdf.chapter_title('Sarvashtakavarga (House Support Points)')
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 5, "SAV scores represent the collective strength of a house. 28 is average. > 30 is Strong; < 25 is Lower.\n")
    signs_std = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    asc_sign = chart.d1_chart.houses[0].sign
    asc_idx = signs_std.index(asc_sign)
    sav_dict = chart.ashtakavarga.sav
    for h_num in range(1, 13):
        sign_name = signs_std[(asc_idx + h_num - 1) % 12]
        score = int(sav_dict.get(sign_name, 0))
        bar = "|" + ("#" * (score // 2))
        pdf.set_font('courier', '', 10)
        pdf.cell(60, 6, f"House {h_num:2} ({sign_name:<11}): {score:2}", 0)
        pdf.cell(0, 6, bar, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # --- DASHA PAGE ---
    pdf.add_page()
    pdf.chapter_title('Vimshottari Dasha Timeline')
    try:
        mahadashas = chart.dashas.upcoming.get('mahadashas', {})
        for m_lord, m_data in mahadashas.items():
            m_start = m_data['start'].strftime('%Y-%m-%d')
            m_end = m_data['end'].strftime('%Y-%m-%d')
            pdf.set_font('helvetica', 'B', 11)
            pdf.cell(0, 8, f"MAHADASHA: {m_lord.upper()} ({m_start} to {m_end})", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            antars = m_data.get('antardashas', {})
            pdf.set_font('helvetica', '', 10)
            for a_lord, a_data in list(antars.items())[:5]:
                pdf.cell(10)
                pdf.cell(0, 6, f"-> {a_lord:<10} starts {a_data['start'].strftime('%Y-%m-%d')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(4)
    except: pass

    # --- VARGA PAGES ---
    descriptions = {
        "Physical Rashi": "D1: Root of existence. Physical health, appearance, and life template.",
        "Soul Navamsha": "D9: Internal strength. True soul nature, partnerships, and 'fruit' of life.",
        "Professional Dashamsha": "D10: Career blueprint. Achievements, public status, and karmic impact.",
        "Creative Saptamsha": "D7: Fruit of union. Creativity, progeny, and partnership expansion."
    }

    v_key_map = {"Physical Rashi": "d1", "Soul Navamsha": "d9", "Professional Dashamsha": "d10", "Creative Saptamsha": "d7"}

    for title, img_path in image_paths.items():
        if img_path:
            pdf.add_page()
            pdf.chapter_title(title)
            pdf.set_font('helvetica', 'I', 10)
            pdf.multi_cell(0, 5, descriptions.get(title, ""))
            pdf.ln(5)
            img_width = 140
            pdf.image(img_path, x=(pdf.w - img_width)/2, w=img_width)
            pdf.ln(5)
            pdf.sub_title(f"{title} Positions")
            pdf.set_font('courier', '', 9)
            v_key = v_key_map.get(title)
            v_chart = chart.d1_chart if v_key == "d1" else chart.divisional_charts.get(v_key)
            if v_chart:
                pdf.cell(40, 6, "Planet", 1)
                pdf.cell(40, 6, "Sign", 1)
                pdf.cell(40, 6, "House", 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                for h_idx, house in enumerate(v_chart.houses):
                    for occ in house.occupants:
                        pdf.cell(40, 6, occ.celestial_body, 1)
                        pdf.cell(40, 6, occ.sign, 1)
                        pdf.cell(40, 6, str(h_idx + 1), 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.output(output_path)
    return output_path
