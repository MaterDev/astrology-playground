import os
import sys
import json
from src.engine import calculate_full_chart
from src.visuals import generate_visual_chart
from src.reporter import generate_report
from src.utils import theme_log, get_safe_name

def run_system(config_path):
    theme_log("root", "Initializing Primatif Astrology System...")
    
    if not os.path.exists(config_path):
        theme_log("error", f"Profile configuration not found: {config_path}")
        return

    # 1. Load Data
    with open(config_path, 'r') as f:
        user_data = json.load(f)
    
    # 2. Calculate
    chart, birth_date = calculate_full_chart(user_data)
    
    # --- RESTORE DETAILED TERMINAL OUTPUT ---
    p = chart.panchanga
    print(f"\n--- 🖐️ PANCHANGA: {p.tithi} | {p.nakshatra} | {p.yoga} | {p.vaara} ---")
    
    print("\n--- 🪐 PLANETARY STATUS & ANALYSIS ---")
    header = f"{'Planet':<10} | {'Sign':<12} | {'Degree':<8} | {'Strength':<8} | {'Bindu'}"
    print(header)
    print("-" * len(header))
    
    planets = sorted(chart.d1_chart.planets, key=lambda x: x.celestial_body)
    bhav_bindus = chart.ashtakavarga.bhav
    for p_obj in planets:
        p_name = p_obj.celestial_body
        p_sign = p_obj.sign
        sb_total = p_obj.shadbala.get('Shadbala', {}).get('Total', 0)
        bindu = bhav_bindus.get(p_name, {}).get(p_sign, "-")
        print(f"{p_name:<10} | {p_sign:<12} | {p_obj.sign_degrees:>6.2f}° | {sb_total:>8.2f} | {bindu}")

    print("\n--- 📊 SARVASHTAKAVARGA (SAV) ---")
    signs_std = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    asc_sign = chart.d1_chart.houses[0].sign
    asc_idx = signs_std.index(asc_sign)
    sav_dict = chart.ashtakavarga.sav
    for h_num in range(1, 13):
        sign_name = signs_std[(asc_idx + h_num - 1) % 12]
        score = int(sav_dict.get(sign_name, 0))
        bar = "█" * (score // 2)
        print(f"House {h_num:2} ({sign_name:<11}): {score:2} {bar}")

    print("\n--- ⏳ VIMSHOTTARI DASHA TIMELINE ---")
    try:
        mahadashas = chart.dashas.upcoming.get('mahadashas', {})
        for m_lord, m_data in mahadashas.items():
            print(f"▶️ {m_lord.upper()}: {m_data['start'].strftime('%Y-%m-%d')} to {m_data['end'].strftime('%Y-%m-%d')}")
            for a_lord, a_data in list(m_data.get('antardashas', {}).items())[:2]:
                print(f"   ↳ {a_lord:<10} starts {a_data['start'].strftime('%Y-%m-%d')}")
    except: pass
    
    # 3. Setup Workspace
    safe_name = get_safe_name(user_data['name'])
    output_dir = os.path.join(os.getcwd(), "charts", safe_name)
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    
    # 4. Generate Visuals
    print("\n--- 🎨 CAPTURING PLANETARY ALIGNMENTS (IMAGES) ---")
    vargas = [
        (chart.d1_chart, "Physical Rashi", f"varga_{safe_name}_d1"),
        (chart.divisional_charts.get('d9'), "Soul Navamsha", f"varga_{safe_name}_d9"),
        (chart.divisional_charts.get('d10'), "Professional Dashamsha", f"varga_{safe_name}_d10"),
        (chart.divisional_charts.get('d7'), "Creative Saptamsha", f"varga_{safe_name}_d7")
    ]
    
    image_paths = {}
    for c_obj, title, fname in vargas:
        if c_obj:
            path = generate_visual_chart(c_obj, title, fname, output_dir, user_data['name'])
            image_paths[title] = path

    # 5. Weave Report
    final_pdf = os.path.join(output_dir, f"primatif_blueprint_{safe_name}.pdf")
    generate_report(chart, birth_date, user_data, image_paths, final_pdf)
    
    theme_log("success", f"Professional Blueprint Manifested: {final_pdf}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        profile_dir = "profiles"
        profiles = [os.path.join(profile_dir, f) for f in os.listdir(profile_dir) if f.endswith('.json')]
        target = profiles[0] if profiles else None
        
    if target:
        run_system(target)
    else:
        theme_log("error", "No profile configuration provided or found in /profiles.")
