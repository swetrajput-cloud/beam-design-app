from flask import Flask, render_template, request, jsonify
import pandas as pd
import math

app = Flask(__name__)

# Lookup table for tc values based on % steel
TC_LOOKUP = {
    0.15: 0.28, 0.25: 0.36, 0.5: 0.46, 0.75: 0.54,
    1: 0.62, 1.25: 0.68, 1.5: 0.74, 2: 0.82, 3: 0.93
}

def get_tc_value(percent_steel):
    """Get tc value from lookup table with interpolation"""
    if percent_steel in TC_LOOKUP:
        return TC_LOOKUP[percent_steel]
    
    # Linear interpolation
    keys = sorted(TC_LOOKUP.keys())
    for i in range(len(keys)-1):
        if keys[i] <= percent_steel <= keys[i+1]:
            x1, x2 = keys[i], keys[i+1]
            y1, y2 = TC_LOOKUP[x1], TC_LOOKUP[x2]
            return y1 + (y2-y1)*(percent_steel-x1)/(x2-x1)
    
    return TC_LOOKUP[max(keys)] if percent_steel > max(keys) else TC_LOOKUP[min(keys)]

def calculate_beam_design(b, d, cover, fck, fy, Mu_input):
    """Complete beam design calculation"""
    results = {}
    
    # Effective depth
    results['d_eff'] = d - cover
    
    # Moment and shear
    results['Mu'] = Mu_input
    results['Vu'] = Mu_input / results['d_eff'] * 1000  # Approximate
    
    # Lever arm (approximate)
    results['z'] = 0.9 * results['d_eff']
    
    # Limiting R value
    if fy == 415:
        R_lim = 0.138
    elif fy == 500:
        R_lim = 0.149
    else:
        R_lim = 0.138
    results['R_lim'] = R_lim
    
    # Mu_lim
    results['Mu_lim'] = R_lim * fck * b * results['d_eff']**2
    
    # Check if under-reinforced
    results['check_mu'] = "OK - Under-reinforced" if Mu_input <= results['Mu_lim'] else "FAIL - Over-reinforced"
    
    # Required Ast
    results['Ast_required'] = (Mu_input * 1e6) / (0.87 * fy * results['z'])
    
    # Minimum Ast
    results['Ast_min'] = 0.85 * b * results['d_eff'] / fy
    
    # Use Ast
    results['Ast_use'] = max(results['Ast_required'], results['Ast_min'])
    
    # Area of one bar (assuming 16mm diameter)
    bar_dia = 16
    results['bar_area'] = math.pi * bar_dia**2 / 4
    
    # Number of bars
    results['num_bars'] = math.ceil(results['Ast_use'] / results['bar_area'])
    
    # Provided Ast
    results['Ast_provided'] = results['num_bars'] * results['bar_area']
    
    # % tension steel
    results['percent_steel'] = (results['Ast_provided'] / (b * results['d_eff'])) * 100
    
    # Nominal shear stress
    results['tau_v'] = results['Vu'] / (b * results['d_eff'])
    
    # Allowable shear stress (from IS456 Table 19)
    results['tc'] = get_tc_value(results['percent_steel'])
    
    # Shear check
    results['shear_check'] = "Shear OK (no additional shear design needed)" if results['tau_v'] <= results['tc'] else "Additional shear reinforcement required"
    
    # Stirrup design (assuming 8mm dia, 2-legged)
    stirrup_dia = 8
    results['stirrup_area_single'] = math.pi * stirrup_dia**2 / 4
    results['stirrup_area_total'] = 2 * results['stirrup_area_single']  # 2 legs
    
    # Spacing calculation (if shear reinforcement needed)
    if results['tau_v'] > results['tc']:
        Vus = (results['tau_v'] - results['tc']) * b * results['d_eff']
        results['spacing_required'] = (0.87 * fy * results['stirrup_area_total'] * results['d_eff']) / Vus
    else:
        results['spacing_required'] = None
    
    # Recommended max spacing
    results['max_spacing'] = min(b/2, 0.75*results['d_eff'])
    
    return results

def load_beam_data():
    """Load beam design data from Excel file"""
    try:
        df = pd.read_excel('data/singly_reinforced_beam_design.xlsx')
        return df
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/calculator')
def calculator():
    beam_data = load_beam_data()
    if beam_data is not None:
        data = beam_data.to_dict('records')
    else:
        data = []
    return render_template('calculator.html', beam_data=data)

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """API endpoint to calculate complete beam design"""
    try:
        data = request.get_json()
        
        # Get input parameters
        b = float(data.get('width', 300))  # mm
        d = float(data.get('depth', 500))  # mm
        cover = float(data.get('cover', 40))  # mm
        fck = float(data.get('fck', 20))  # N/mm²
        fy = float(data.get('fy', 415))  # N/mm²
        Mu = float(data.get('moment', 100))  # kN-m
        
        # Perform calculations
        results = calculate_beam_design(b, d, cover, fck, fy, Mu)
        
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)