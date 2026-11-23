import os
import struct
import zlib
import math

# 5x7 bitmap font for ASCII characters
FONT_5X7 = {
    ' ': ["     ", "     ", "     ", "     ", "     ", "     ", "     "],
    'A': [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    'B': ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    'C': [" ####", "#    ", "#    ", "#    ", "#    ", "#    ", " ####"],
    'D': ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    'E': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    'F': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    'G': [" ####", "#    ", "#    ", "#  ##", "#   #", "#   #", " ####"],
    'H': ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    'I': [" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    'J': ["  ###", "    #", "    #", "    #", "    #", "#   #", " ### "],
    'K': ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    'L': ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    'M': ["#   #", "## ##", "# # #", "#   #", "#   #", "#   #", "#   #"],
    'N': ["#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"],
    'O': [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    'P': ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    'Q': [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    'R': ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    'S': [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    'T': ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    'U': ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    'V': ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    'W': ["#   #", "#   #", "#   #", "# # #", "## ##", "#   #", "#   #"],
    'X': ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    'Y': ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    'Z': ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    '0': [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    '1': ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", "#####"],
    '2': [" ### ", "#   #", "    #", " ### ", "#    ", "#    ", "#####"],
    '3': [" ### ", "#   #", "    #", "  ## ", "    #", "#   #", " ### "],
    '4': ["#    ", "#   #", "#   #", "#####", "    #", "    #", "    #"],
    '5': ["#####", "#    ", "#    ", "#### ", "    #", "#   #", " ### "],
    '6': [" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "],
    '7': ["#####", "    #", "   # ", "  #  ", "  #  ", "  #  ", "  #  "],
    '8': [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    '9': [" ### ", "#   #", "#   #", " ####", "    #", "#   #", " ### "],
    '.': ["     ", "     ", "     ", "     ", "     ", " ##  ", " ##  "],
    '-': ["     ", "     ", "     ", "#####", "     ", "     ", "     "],
    ',': ["     ", "     ", "     ", "     ", "     ", " ##  ", "  #  "],
    ':': ["     ", "     ", " ##  ", "     ", "     ", " ##  ", "     "],
    '/': ["    #", "   # ", "  #  ", "  #  ", " #   ", "#    ", "     "],
    '%': ["##  #", "##  #", "   # ", "  #  ", " #   ", "#  ##", "#  ##"],
    '$': ["  #  ", " #####", " # # ", " #####", "  # #", " #####", "  #  "],
    '+': ["     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "],
    '\'':["  #  ", "  #  ", "   # ", "     ", "     ", "     ", "     "],
    '?': [" ### ", "#   #", "    #", "  ## ", "  #  ", "     ", "  #  "],
    '!': ["  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "],
    '&': [" ##  ", "#  # ", " ##  ", "# # #", "#  # ", "#  # ", " ## #"],
    '|': ["  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    '(': ["   # ", "  #  ", " #   ", " #   ", " #   ", "  #  ", "   # "],
    ')': [" #   ", "  #  ", "   # ", "   # ", "   # ", "  #  ", " #   "],
    '"': [" # # ", " # # ", "     ", "     ", "     ", "     ", "     "],
    '_': ["     ", "     ", "     ", "     ", "     ", "     ", "#####"],
}

def get_char_pattern(c):
    c_upper = c.upper()
    if c_upper in FONT_5X7:
        return FONT_5X7[c_upper]
    return FONT_5X7['?']

WIDTH, HEIGHT = 1024, 1024
BG_COLOR = (248, 249, 250)
WHITE = (255, 255, 255)
BLACK = (20, 24, 30)
MUTED = (108, 117, 125)
BORDER = (222, 226, 230)

CONTINENT_COLORS = {
    "Europe": (37, 99, 235),       # Blue
    "Asia": (220, 38, 38),         # Red
    "Africa": (22, 163, 74),        # Green
    "North America": (234, 88, 12), # Orange
    "South America": (147, 51, 234),# Purple
    "Oceania": (13, 148, 136)      # Teal
}

pixels = bytearray([BG_COLOR[0], BG_COLOR[1], BG_COLOR[2]] * (WIDTH * HEIGHT))

def set_pixel(x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        idx = (y * WIDTH + x) * 3
        pixels[idx] = color[0]
        pixels[idx+1] = color[1]
        pixels[idx+2] = color[2]

def fill_rect(x, y, w, h, color):
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(WIDTH, x + w)
    y1 = min(HEIGHT, y + h)
    for py in range(y0, y1):
        row_offset = py * WIDTH * 3
        for px in range(x0, x1):
            idx = row_offset + px * 3
            pixels[idx] = color[0]
            pixels[idx+1] = color[1]
            pixels[idx+2] = color[2]

def draw_rect(x, y, w, h, color):
    for px in range(x, x + w):
        set_pixel(px, y, color)
        set_pixel(px, y + h - 1, color)
    for py in range(y, y + h):
        set_pixel(x, py, color)
        set_pixel(x + w - 1, py, color)

def draw_line(x0, y0, x1, y1, color):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        set_pixel(x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def draw_char(x, y, char, color, scale=1):
    pattern = get_char_pattern(char)
    for row_idx, row in enumerate(pattern):
        for col_idx, ch in enumerate(row):
            if ch == '#':
                for sy in range(scale):
                    for sx in range(scale):
                        set_pixel(x + col_idx * scale + sx, y + row_idx * scale + sy, color)

def draw_text(x, y, text, color, scale=1):
    cur_x = x
    for char in text:
        draw_char(cur_x, y, char, color, scale)
        cur_x += (5 + 1) * scale

def measure_text_width(text, scale=1):
    if not text:
        return 0
    return len(text) * (5 + 1) * scale - scale

def wrap_text(text, max_width, scale=1):
    words = text.split(' ')
    lines = []
    current_line = []
    char_w = (5 + 1) * scale
    
    for word in words:
        word_w = len(word) * char_w
        if word_w > max_width:
            max_chars = max(1, (max_width - 3 * char_w) // char_w)
            word = word[:max_chars] + "..."
        
        test_line = current_line + [word]
        test_str = " ".join(test_line)
        if measure_text_width(test_str, scale) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def generate_worldmap_file():
    cols, rows = 96, 48
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    
    def fill_box(lat_min, lat_max, lon_min, lon_max):
        r_min = int((90.0 - lat_max) / 180.0 * rows)
        r_max = int((90.0 - lat_min) / 180.0 * rows)
        c_min = int((lon_min + 180.0) / 360.0 * cols)
        c_max = int((lon_max + 180.0) / 360.0 * cols)
        
        r_min = max(0, min(rows - 1, r_min))
        r_max = max(0, min(rows - 1, r_max))
        c_min = max(0, min(cols - 1, c_min))
        c_max = max(0, min(cols - 1, c_max))
        
        for r in range(min(r_min, r_max), max(r_min, r_max) + 1):
            for c in range(min(c_min, c_max), max(c_min, c_max) + 1):
                grid[r][c] = '#'

    fill_box(15, 75, -165, -50)
    fill_box(-55, 12, -82, -34)
    fill_box(-35, 37, -18, 52)
    fill_box(5, 75, -10, 180)
    fill_box(-42, -10, 113, 155)
    fill_box(60, 83, -73, -12)
    
    content = "\n".join("".join(row) for row in grid)
    with open("worldmap.txt", "w") as f:
        f.write(content)

generate_worldmap_file()

STORIES_DATA = [
    {"id": 1, "continent": "Asia", "category": "WAR", "headline": "Iran strikes US bases in Bahrain", "deck": "Iran fires missiles and drones at US military bases in Bahrain, the IRGC claims it destroyed two Patriot radars, a claim the US has not confirmed, and a fire breaks out at a civilian site.", "lat": 26.23, "lon": 50.59},
    {"id": 2, "continent": "Asia", "category": "CLIMATE", "headline": "COP31 climate talks collapse", "deck": "COP31 climate talks in Antalya collapse with no deal on fossil fuels, Australia's PM calls the failure a sign of difficult geopolitical times.", "lat": 36.9, "lon": 30.7},
    {"id": 3, "continent": "Europe", "category": "WAR", "headline": "Russian cargo ship ablaze off Finland", "deck": "A Russian cargo ship is still on fire off Finland after an attack, Ukraine is reported to have hit it with a drone and Russia is towing it away.", "lat": 59.9, "lon": 23.5},
    {"id": 4, "continent": "Europe", "category": "WAR", "headline": "Russian drone hits Kyiv region building", "deck": "At least 14 people are missing after a Russian drone hits a building in the Kyiv region, Ukraine's president says.", "lat": 50.45, "lon": 30.52},
    {"id": 5, "continent": "North America", "category": "CRIME", "headline": "Mexico captures FBI most-wanted cartel boss", "deck": "Mexican authorities capture FBI most-wanted cartel boss 'El Chapo Isidro' after firefights in Sinaloa leave 11 dead.", "lat": 24.8, "lon": -107.4},
    {"id": 6, "continent": "North America", "category": "TECH", "headline": "FBI crime database hacked, Trump confirms", "deck": "The FBI's National Crime Information Centre is hacked, President Trump confirms, as the bureau probes the breach.", "lat": 38.88, "lon": -77.23},
    {"id": 7, "continent": "Europe", "category": "DIPLOMACY", "headline": "UN states to keep talking on killer robots", "deck": "Nations agree at a UN conference to continue negotiations on lethal autonomous weapons systems.", "lat": 46.2, "lon": 6.14},
    {"id": 8, "continent": "Asia", "category": "POLITICS", "headline": "South Korea minister quits over AI exam cheating", "deck": "South Korea's education minister resigns over an AI-driven exam cheating scandal.", "lat": 37.57, "lon": 126.98},
    {"id": 9, "continent": "Asia", "category": "DIPLOMACY", "headline": "Nepal PM holds talks with Modi in Delhi", "deck": "Nepal PM Balendra Shah holds bilateral talks with PM Modi on a state visit to India.", "lat": 28.61, "lon": 77.21},
    {"id": 10, "continent": "Asia", "category": "WAR", "headline": "Saudi coalition intercepts Houthi missile", "deck": "The Saudi-led coalition says it intercepted a Houthi missile over western Saudi Arabia as Gulf attacks widen.", "lat": 24.71, "lon": 46.68},
    {"id": 11, "continent": "North America", "category": "MARKETS", "headline": "Global stocks fall as AI sell-off deepens", "deck": "Global stocks fall as the AI sell-off deepens, the S+P 500 drops 3.7% and Japan's Nikkei falls 5.06%.", "lat": 40.71, "lon": -74.01},
    {"id": 12, "continent": "Europe", "category": "COURTS", "headline": "UN court: Myanmar committed Rohingya genocide", "deck": "The UN's top court rules Myanmar committed genocide against the Rohingya Muslim minority.", "lat": 52.09, "lon": 4.31},
    {"id": 13, "continent": "South America", "category": "POLITICS", "headline": "Bolsonaro 'stable' in intensive care", "deck": "Brazil's ex-leader Jair Bolsonaro is stable in intensive care, doctors say.", "lat": -15.79, "lon": -47.88},
    {"id": 14, "continent": "Africa", "category": "CONFLICT", "headline": "24 civilians killed in South Sudan violence", "deck": "24 civilians are killed in fresh violence in South Sudan, officials say.", "lat": 4.85, "lon": 31.58},
    {"id": 15, "continent": "Oceania", "category": "SPORT", "headline": "India post record 720/9 in Wellington Test", "deck": "India post a record 720 for 9 declared in the Wellington Test against New Zealand.", "lat": -41.29, "lon": 174.78},
    {"id": 16, "continent": "Asia", "category": "POLITICS", "headline": "N. Korea's Kim: we seek security, not supremacy", "lat": 39.04, "lon": 125.75},
    {"id": 17, "continent": "Africa", "category": "HEALTH", "headline": "WHO chief pleads for peace in Ebola-hit DR Congo", "lat": -4.32, "lon": 15.31},
    {"id": 18, "continent": "Africa", "category": "WAR", "headline": "Drone strikes hit homes, UN building in Khartoum", "lat": 15.5, "lon": 32.56},
    {"id": 19, "continent": "Asia", "category": "POLITICS", "headline": "Eisenkot calls settler violence 'Jewish terrorism'", "lat": 32.08, "lon": 34.78},
    {"id": 20, "continent": "Africa", "category": "CONFLICT", "headline": "35 Fulanis killed in revenge attacks in Nigeria", "lat": 9.06, "lon": 7.49},
    {"id": 21, "continent": "Europe", "category": "WAR", "headline": "Poland says three Russian cruise missiles hit", "lat": 52.23, "lon": 21.01},
    {"id": 22, "continent": "Asia", "category": "POLITICS", "headline": "Myanmar calls ASEAN decision 'unfair'", "lat": 16.84, "lon": 96.17},
    {"id": 23, "continent": "Asia", "category": "DISASTER", "headline": "Indonesian factory fire: 7 dead, 50 missing", "lat": -6.2, "lon": 106.85},
    {"id": 24, "continent": "Europe", "category": "PROTEST", "headline": "Thousands march in Lisbon over living costs", "lat": 38.72, "lon": -9.14},
    {"id": 25, "continent": "North America", "category": "TECH", "headline": "Nvidia row: AI chips diverted to China", "lat": 37.37, "lon": -121.92},
    {"id": 26, "continent": "North America", "category": "TECH", "headline": "Waymo pulls driverless taxis from US freeways", "lat": 37.77, "lon": -122.42},
    {"id": 27, "continent": "Africa", "category": "DISASTER", "headline": "Migrant boat capsizes off Senegal, dozens missing", "lat": 14.72, "lon": -17.47},
    {"id": 28, "continent": "Africa", "category": "POLITICS", "headline": "South Sudan delays first elections to Feb 2027", "lat": 4.85, "lon": 31.58},
    {"id": 29, "continent": "Africa", "category": "CRIME", "headline": "Mass shootings kill 17 in South Africa", "lat": -26.2, "lon": 28.05},
    {"id": 30, "continent": "Europe", "category": "DEFENCE", "headline": "UK to produce Ukrainian drones in new deal", "lat": 51.5, "lon": -0.12},
    {"id": 31, "continent": "Asia", "category": "DIPLOMACY", "headline": "Trump, Xi and Putin to meet at APEC Shenzhen", "lat": 22.54, "lon": 114.06},
    {"id": 32, "continent": "Asia", "category": "ECONOMY", "headline": "EU and Indonesia sign trade deal", "lat": -6.2, "lon": 106.85},
    {"id": 33, "continent": "North America", "category": "TECH", "headline": "Amazon nears $7.5B deal for Israeli AI startup Decart", "lat": 47.61, "lon": -122.33},
    {"id": 34, "continent": "North America", "category": "CULTURE", "headline": "GTA 6 sets record $3.79B launch day", "lat": 34.05, "lon": -118.24},
    {"id": 35, "continent": "Europe", "category": "SPORT", "headline": "Alcaraz beats Zverev to win ATP Finals", "lat": 45.07, "lon": 7.69},
]

def render_page():
    # 1. MASTHEAD
    mx, my, mw, mh = 16, 16, 992, 95
    fill_rect(mx, my, mw, mh, WHITE)
    draw_rect(mx, my, mw, mh, BORDER)
    
    draw_text(mx + 20, my + 14, "THE DAY IN WORLD NEWS", MUTED, scale=1)
    draw_text(mx + 20, my + 30, "MONDAY 23 NOVEMBER 2026", BLACK, scale=3)
    draw_text(mx + 20, my + 72, "35 STORIES - 6 CONTINENTS", MUTED, scale=1)
    
    # Continent Legend on right of Masthead
    legend_items = [
        ("Europe", CONTINENT_COLORS["Europe"]),
        ("Asia", CONTINENT_COLORS["Asia"]),
        ("Africa", CONTINENT_COLORS["Africa"]),
        ("N.America", CONTINENT_COLORS["North America"]),
        ("S.America", CONTINENT_COLORS["South America"]),
        ("Oceania", CONTINENT_COLORS["Oceania"])
    ]
    lx = mx + mw - 320
    ly = my + 18
    for idx, (c_name, c_col) in enumerate(legend_items):
        col_idx = idx % 3
        row_idx = idx // 3
        item_x = lx + col_idx * 105
        item_y = ly + row_idx * 30
        fill_rect(item_x, item_y + 4, 10, 10, c_col)
        draw_rect(item_x, item_y + 4, 10, 10, BLACK)
        draw_text(item_x + 14, item_y + 4, c_name, BLACK, scale=1)

    # 2. HERO PANELS (1-3)
    hx, hy, hw, hh = 16, 122, 316, 225
    gap = 14
    
    for i in range(3):
        panel_x = hx + i * (hw + gap)
        story = STORIES_DATA[i]
        c_col = CONTINENT_COLORS.get(story["continent"], BLACK)
        
        fill_rect(panel_x, hy, hw, hh, WHITE)
        draw_rect(panel_x, hy, hw, hh, BORDER)
        
        # Illustration area top 110px
        art_y = hy + 1
        art_h = 110
        fill_rect(panel_x + 1, art_y, hw - 2, art_h, (235, 238, 242))
        
        # Hero Art specific drawings
        if i == 0:
            # Hero 1: Bahrain strikes - two red missiles & orange blast square
            fill_rect(panel_x + 60, art_y + 30, 40, 20, (220, 38, 38))
            fill_rect(panel_x + 140, art_y + 60, 40, 20, (220, 38, 38))
            fill_rect(panel_x + 210, art_y + 40, 35, 35, (234, 88, 12))
            draw_line(panel_x + 40, art_y + 40, panel_x + 60, art_y + 40, BLACK)
            draw_line(panel_x + 120, art_y + 70, panel_x + 140, art_y + 70, BLACK)
        elif i == 1:
            # Hero 2: COP31 collapse - three flagpoles with blue, green, orange flags
            for fx in [80, 150, 220]:
                draw_line(panel_x + fx, art_y + 20, panel_x + fx, art_y + 90, BLACK)
            fill_rect(panel_x + 81, art_y + 20, 30, 18, CONTINENT_COLORS["Europe"])
            fill_rect(panel_x + 151, art_y + 35, 30, 18, CONTINENT_COLORS["Africa"])
            fill_rect(panel_x + 221, art_y + 50, 30, 18, CONTINENT_COLORS["North America"])
        elif i == 2:
            # Hero 3: Ship ablaze off Finland - orange flame over dark ship on blue waves
            fill_rect(panel_x + 80, art_y + 70, 160, 20, BLACK) # ship hull
            fill_rect(panel_x + 110, art_y + 50, 100, 20, BLACK) # superstructure
            fill_rect(panel_x + 130, art_y + 20, 30, 35, (234, 88, 12)) # flames
            fill_rect(panel_x + 170, art_y + 25, 25, 30, (220, 38, 38))
            fill_rect(panel_x + 20, art_y + 92, hw - 40, 14, CONTINENT_COLORS["Europe"])
            
        # Data badge
        badge_y = hy + 113
        fill_rect(panel_x + 12, badge_y, hw - 24, 22, c_col)
        badge_text = ["BAHRAIN STRIKES", "COP31 COLLAPSE", "SHIP ABLAZE"][i]
        draw_text(panel_x + 20, badge_y + 4, badge_text, WHITE, scale=1)
        
        # Continent | Category
        meta_y = badge_y + 28
        meta_str = f"{story['continent'].upper()} | {story['category']}"
        draw_text(panel_x + 12, meta_y, meta_str, MUTED, scale=1)
        
        # Headline (max 2 lines)
        head_y = meta_y + 16
        head_lines = wrap_text(story["headline"], hw - 24, scale=1)
        for hl_idx, hl in enumerate(head_lines[:2]):
            draw_text(panel_x + 12, head_y + hl_idx * 14, hl, BLACK, scale=1)
            
        # Deck (max 2 lines)
        deck_y = head_y + len(head_lines[:2]) * 14 + 4
        deck_lines = wrap_text(story["deck"], hw - 24, scale=1)
        for dl_idx, dl in enumerate(deck_lines[:2]):
            draw_text(panel_x + 12, deck_y + dl_idx * 12, dl, MUTED, scale=1)

    # 3. NUMBERED GRID (Stories 4-15)
    gx, gy, gw, gh = 16, 359, 316, 105
    col_gap, row_gap = 14, 6
    
    for idx in range(12):
        story = STORIES_DATA[3 + idx]
        c = idx % 3
        r = idx // 3
        cell_x = gx + c * (gw + col_gap)
        cell_y = gy + r * (gh + row_gap)
        
        fill_rect(cell_x, cell_y, gw, gh, WHITE)
        draw_rect(cell_x, cell_y, gw, gh, BORDER)
        
        c_col = CONTINENT_COLORS.get(story["continent"], BLACK)
        
        # Number chip + Category tag
        fill_rect(cell_x + 10, cell_y + 8, 22, 16, c_col)
        draw_text(cell_x + 14, cell_y + 10, str(story["id"]), WHITE, scale=1)
        
        cat_str = f"{story['continent']} | {story['category']}"
        draw_text(cell_x + 38, cell_y + 10, cat_str, MUTED, scale=1)
        
        # Small pictogram top-right
        pic_x = cell_x + gw - 35
        pic_y = cell_y + 8
        if idx % 4 == 0:
            # Triangle
            draw_line(pic_x + 12, pic_y, pic_x, pic_y + 20, BLACK)
            draw_line(pic_x, pic_y + 20, pic_x + 24, pic_y + 20, BLACK)
            draw_line(pic_x + 24, pic_y + 20, pic_x + 12, pic_y, BLACK)
        elif idx % 4 == 1:
            # Circle
            fill_rect(pic_x + 6, pic_y + 4, 12, 12, MUTED)
        elif idx % 4 == 2:
            # Cross
            draw_line(pic_x + 4, pic_y + 10, pic_x + 20, pic_y + 10, BLACK)
            draw_line(pic_x + 12, pic_y + 2, pic_x + 12, pic_y + 18, BLACK)
        else:
            # Diamond
            draw_line(pic_x + 12, pic_y, pic_x + 24, pic_y + 10, BLACK)
            draw_line(pic_x + 24, pic_y + 10, pic_x + 12, pic_y + 20, BLACK)
            draw_line(pic_x + 12, pic_y + 20, pic_x, pic_y + 10, BLACK)
            draw_line(pic_x, pic_y + 10, pic_x + 12, pic_y, BLACK)
            
        # Headline (max 2 lines)
        head_lines = wrap_text(story["headline"], gw - 20, scale=1)
        for hl_idx, hl in enumerate(head_lines[:2]):
            draw_text(cell_x + 10, cell_y + 32 + hl_idx * 14, hl, BLACK, scale=1)
            
        # Deck (max 2 lines)
        if "deck" in story:
            deck_lines = wrap_text(story["deck"], gw - 20, scale=1)
            for dl_idx, dl in enumerate(deck_lines[:2]):
                draw_text(cell_x + 10, cell_y + 64 + dl_idx * 12, dl, MUTED, scale=1)

    # 4. BOTTOM ROW (y = 805, height = 175)
    by = 805
    bh = 175
    
    # Left Map Panel (width 480, x = 16)
    mw_panel_x, mw_panel_w = 16, 480
    fill_rect(mw_panel_x, by, mw_panel_w, bh, WHITE)
    draw_rect(mw_panel_x, by, mw_panel_w, bh, BORDER)
    draw_text(mw_panel_x + 12, by + 10, "WHERE IT HAPPENED (TOP 15 STORIES PINNED)", BLACK, scale=1)
    
    # Draw World Map & Pinned Stories 1-15
    with open("worldmap.txt", "r") as f:
        map_lines = f.read().strip().split('\n')
    map_rows = len(map_lines)
    map_cols = len(map_lines[0])
    
    map_x = mw_panel_x + 12
    map_y = by + 28
    map_w = mw_panel_w - 24
    map_h = bh - 38
    
    cell_w = map_w / map_cols
    cell_h = map_h / map_rows
    
    for r in range(map_rows):
        for c in range(map_cols):
            if map_lines[r][c] == '#':
                px = int(map_x + c * cell_w)
                py = int(map_y + r * cell_h)
                fill_rect(px, py, max(1, int(cell_w)), max(1, int(cell_h)), (210, 215, 222))
                
    for story in STORIES_DATA[:15]:
        lat, lon = story["lat"], story["lon"]
        c = int((lon + 180.0) / 360.0 * map_cols)
        r = int((90.0 - lat) / 180.0 * map_rows)
        px = int(map_x + c * cell_w)
        py = int(map_y + r * cell_h)
        
        col = CONTINENT_COLORS.get(story["continent"], BLACK)
        sq_x = px - 3
        sq_y = py - 3
        fill_rect(sq_x, sq_y, 7, 7, col)
        draw_rect(sq_x, sq_y, 7, 7, BLACK)
        draw_text(sq_x + 8, sq_y - 2, str(story["id"]), BLACK, scale=1)

    # Right Also Panel (Stories 16-35)
    aw_panel_x, aw_panel_w = 506, 502
    fill_rect(aw_panel_x, by, aw_panel_w, bh, WHITE)
    draw_rect(aw_panel_x, by, aw_panel_w, bh, BORDER)
    draw_text(aw_panel_x + 12, by + 10, "ALSO ON 23 NOVEMBER 2026 (STORIES 16-35)", BLACK, scale=1)
    
    # List 20 stories in 2 columns of 10
    also_stories = STORIES_DATA[15:] # 16 to 35
    col1 = also_stories[:10]
    col2 = also_stories[10:]
    
    def render_also_column(stories, col_x, start_y):
        curr_y = start_y
        for s in stories:
            # Format: "N. CAT | headline truncated to fit ~220px"
            line_str = f"{s['id']}. {s['category'][:3]} | {s['headline']}"
            # truncate to fit ~36 chars (~220px at scale 1)
            if len(line_str) > 38:
                line_str = line_str[:35] + "..."
            draw_text(col_x, curr_y, line_str, BLACK, scale=1)
            curr_y += 13

    render_also_column(col1, aw_panel_x + 12, by + 28)
    render_also_column(col2, aw_panel_x + 258, by + 28)

    # 5. FOOTER
    fy = 994
    footer_text = "Every story happened or was first reported on Monday 23 November 2026. Disputed claims are attributed. Sources: AP - Reuters - AFP - BBC"
    draw_text(16, 1002, footer_text, MUTED, scale=1)

render_page()

def save_png(filename, width, height, pixels):
    scanlines = bytearray()
    row_size = width * 3
    for y in range(height):
        scanlines.append(0)
        start = y * row_size
        scanlines.extend(pixels[start:start+row_size])
    
    compressed = zlib.compress(bytes(scanlines), level=9)
    
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', 0xffffffff & zlib.crc32(tag + data))

    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    
    png_bytes = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', compressed) + chunk(b'IEND', b'')
    
    with open(filename, 'wb') as f:
        f.write(png_bytes)

save_png("entry.png", WIDTH, HEIGHT, pixels)
print("Successfully generated entry.png")
