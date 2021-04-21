import xml.etree.ElementTree as ET


def to_string(pt): return '{0},{1}'.format(pt[1], pt[0])

def make_svg_path(pts):
    
    string = 'M {} C '.format(to_string(pts[0]))
    
    for p in pts[1:]:
        string += to_string(p) + ' '
    
    return string

def make_svg_stroke(pts):
    
    string = 'M {} C'.format(to_string(pts[0]))
    
    for p in pts[1:]:
        string += to_string(p) + ' '
    
    return string + ' Z'

def make_svg_offsets(kv, thk):
    
    string = ''
    
    #for u, off in zip(kv[3:-3], thk):
    for i, off in enumerate(thk):
        
        string += '{0:.5g},{1:.5g} | '.format(i, off)
        
    return string[:-3]

def generate_svg_file(dwg):
    
    # Convert a drawing object to a SVG file readable with Inkscape
    
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.register_namespace('inkscape', "http://www.inkscape.org/namespaces/inkscape")
    tree = ET.parse('templates/blank.svg')
    
    root = tree.getroot()
    layer_lines = root[3]
    layer_strokes = root[4]
    
    for i, ln in enumerate(dwg.lines):
        if ln.valid:
    
            pth_ln = ET.Element('path')
            pth_stk = ET.Element('path')
        
            id_stk = 'stroke{}'.format(i)
            stroke_svg = make_svg_stroke(ln.stroke)
    
            pth_stk.set('style', 'fill:#000000;fill-rule:nonzero;stroke:none;stroke-width:3.0px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1')
            pth_stk.set('id', id_stk)
            pth_stk.set('d', stroke_svg)
            
            id_ln = 'path{}'.format(i)
            path_svg = make_svg_path(ln.bezier_points)
            
            pth_ln.set('style', 'fill:none;fill-rule:nonzero;stroke:#000000;stroke-width:1.0px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1')
            pth_ln.set('id', id_ln)
            pth_ln.set('d', path_svg)
            
            layer_strokes.append(pth_stk)
            layer_lines.append(pth_ln)
    
    tree.write('output.svg')

def generate_svg_file_old(dwg):
    
    # Convert a drawing object to a SVG file readable with Inkscape
    
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.register_namespace('inkscape', "http://www.inkscape.org/namespaces/inkscape")
    tree = ET.parse('templates/power.svg')
    
    root = tree.getroot()
    mk_g = root[3]
    mk_defs = root[0]
    
    for i, ln in enumerate(dwg.lines):
        if ln.valid:
            
            # Definition of the path effect :
            
            pth_eff = ET.Element('inkscape:path-effect')
            
            id_pth_effect = 'path-effect{}'.format(i)
            offsets = make_svg_offsets(ln.knot_vector, ln.thickness)
            
            pth_eff.set('effect', 'powerstroke')
            pth_eff.set('id', id_pth_effect)
            pth_eff.set('is_visible', 'true')
            pth_eff.set('lpeversion', '1')
            pth_eff.set('offset_points', offsets)
            pth_eff.set('sort_points', 'true')
            pth_eff.set('interpolator_type', 'CentripetalCatmullRom')
            pth_eff.set('interpolator_beta', '0.2')
            pth_eff.set('start_linecap_type', 'zerowidth')
            pth_eff.set('linejoin_type', 'round')
            pth_eff.set('miter_limit', '4')
            pth_eff.set('scale_width', '1')
            pth_eff.set('end_linecap_type', 'zerowidth')
            
            #mk_defs.append(pth_eff)
            
            # Definition of the path object :
    
            pth = ET.Element('path')
        
            id_pth = 'path{}'.format(i)
            pth_string = make_svg_path(ln.bezier_points)
    
            pth.set('style', 'fill:none;fill-rule:nonzero;stroke:#000000;stroke-width:3.0px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1')
            pth.set('id', id_pth)
            pth.set('inkscape:path-effect', id_pth_effect)
            #pth.set('d', pth_string)
            pth.set('d', pth_string)
            pth.set('inkscape:original-d', pth_string)
            #pth.set('sodipodi:nodetypes', 'cc')
            
            mk_g.append(pth)
    
    tree.write('output.svg')
