import json
import struct
import os

def analyze_glb(file_path):
    print(f"🔍 INSPECTING: {file_path}")
    
    if not os.path.exists(file_path):
        print("❌ ERROR: File not found.")
        return

    with open(file_path, 'rb') as f:
        # 1. Read Header
        magic = f.read(4)
        if magic != b'glTF':
            print("❌ ERROR: Not a valid GLB file.")
            return
            
        version = struct.unpack('<I', f.read(4))[0]
        print(f"✅ FORMAT: GLB Version {version}")
        
        # 2. Find JSON Chunk
        f.read(4) # Total length
        json_chunk_len = struct.unpack('<I', f.read(4))[0]
        json_type = f.read(4)
        
        if json_type != b'JSON':
            print("❌ ERROR: Could not find JSON chunk.")
            return
            
        json_data = f.read(json_chunk_len)
        data = json.loads(json_data)
        
        # 3. CHECK EXTENSIONS (Draco?)
        extensions = data.get('extensionsUsed', [])
        if 'KHR_draco_mesh_compression' in extensions:
            print("\n⚠️  COMPRESSION DETECTED: Draco (KHR_draco_mesh_compression)")
            print("   👉 You MUST use DRACOLoader in your frontend code.")
        else:
            print("\n✅ COMPRESSION: None (Standard GLB)")

        # 4. CHECK MORPH TARGETS (Muscles)
        print("\n📦 MESH ANALYSIS:")
        meshes = data.get('meshes', [])
        total_targets = 0
        
        for i, mesh in enumerate(meshes):
            name = mesh.get('name', f"Mesh_{i}")
            primitives = mesh.get('primitives', [])
            
            # Check for extras (Blender exports shape key names here sometimes)
            extras_names = mesh.get('extras', {}).get('targetNames', [])
            
            has_targets = False
            for prim in primitives:
                if 'targets' in prim:
                    has_targets = True
                    count = len(prim['targets'])
                    total_targets += count
                    print(f"   • Mesh: '{name}' -> {count} Morph Targets Detected")
                    
                    # Try to guess names if standard names aren't in 'extras'
                    if extras_names:
                        print(f"     Names: {extras_names}")
                    break
            
            if not has_targets:
                print(f"   • Mesh: '{name}' -> Static (No Animation)")

        if total_targets == 0:
            print("\n❌ FATAL: This avatar has 0 Morph Targets.")
            print("   It is a STATUE. It cannot speak.")
            print("   FIX: Re-export from Avaturn/RPM as 'Animatable' or 'T-Pose'.")
        else:
            print("\n✅ SUCCESS: Avatar is animatable.")

# --- RUN IT ---
# Make sure to put the correct path to your avatar
analyze_glb('../frontend/darpan.glb')