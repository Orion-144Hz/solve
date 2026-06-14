import marshal
import struct
import os

MAGIC_312 = struct.pack('<I', 3451)

def create_pyc(code_obj):
    import time
    timestamp = struct.pack('<I', int(time.time()))
    source_size = struct.pack('<I', 0)
    return MAGIC_312 + timestamp + source_size + marshal.dumps(code_obj)

os.makedirs('decompiled_pyc', exist_ok=True)

input_dir = 'extracted_raw'
output_dir = 'decompiled_pyc'

valid_count = 0
for fname in sorted(os.listdir(input_dir)):
    if not fname.endswith('.bin'):
        continue
    
    input_path = os.path.join(input_dir, fname)
    output_name = fname.replace('.bin', '.pyc')
    output_path = os.path.join(output_dir, output_name)
    
    try:
        with open(input_path, 'rb') as f:
            data = f.read()
        
        code = marshal.loads(data)
        pyc_data = create_pyc(code)
        
        with open(output_path, 'wb') as f:
            f.write(pyc_data)
        
        valid_count += 1
    except:
        pass

print(f'Created {valid_count} .pyc files in {output_dir}')
