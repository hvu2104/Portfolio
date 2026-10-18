import os
import re
import base64
from io import BytesIO
from PIL import Image

def process_svg(filepath):
    print(f"Processing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.search(r'xlink:href="data:image/png;base64,([^"]+)"', content)
        if not match:
            print("No embedded png found.")
            return
            
        b64_data = match.group(1)
        img_data = base64.b64decode(b64_data)
        img = Image.open(BytesIO(img_data)).convert("RGBA")
        
        datas = img.getdata()
        new_data = []
        for item in datas:
            # Check for white or near-white pixels
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                new_data.append((255, 255, 255, 0)) # Transparent
            else:
                new_data.append(item)
                
        img.putdata(new_data)
        
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        new_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        new_content = content.replace(b64_data, new_b64)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Success.")
    except Exception as e:
        print(f"Error: {e}")

for i in range(2, 6):
    process_svg(f'd:/Portfolio/images/{i}.svg')
