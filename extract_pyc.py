#!/usr/bin/env python3
import struct
import zlib
import marshal
import os
import sys

def main():
    with open('cover.exe', 'rb') as f:
        data = f.read()

    pyz_offset = 8302842
    xz_magic = b'\x78\x9c'

    # Tüm zlib stream pozisyonlarını bul
    positions = []
    pos = pyz_offset
    while True:
        pos = data.find(xz_magic, pos)
        if pos == -1 or pos > len(data) - 100:
            break
        positions.append(pos)
        pos += 1

    print(f'Total modules: {len(positions)}')

    os.makedirs('/workspace/extracted_source', exist_ok=True)

    success_count = 0
    
    for i in range(len(positions)):
        start = positions[i]
        if i < len(positions) - 1:
            end = positions[i + 1]
        else:
            end = min(start + 500000, len(data))
        
        compressed = data[start:end]
        
        try:
            result = zlib.decompress(compressed)
            code_obj = marshal.loads(result)
            
            if hasattr(code_obj, 'co_filename'):
                filename = code_obj.co_filename
                clean_path = filename.replace('\\', '/')
                
                dir_path = os.path.dirname(clean_path)
                if dir_path:
                    full_dir = os.path.join('/workspace/extracted_source', dir_path)
                    os.makedirs(full_dir, exist_ok=True)
                
                output_path = os.path.join('/workspace/extracted_source', clean_path + '.pyc')
                
                magic = b'\x69\x3a\x0d\x0a'
                flags = b'\x00\x00\x00\x00'
                
                with open(output_path, 'wb') as f:
                    f.write(magic + flags)
                    f.write(marshal.dumps(code_obj))
                
                success_count += 1
                
        except Exception as e:
            pass
        
        if i % 20 == 0:
            print(f'Processed {i}/{len(positions)}, saved {success_count}')
            sys.stdout.flush()

    print(f'\nDone! Saved {success_count} modules')

if __name__ == '__main__':
    main()
