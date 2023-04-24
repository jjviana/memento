import os
def _load_file(base_dir,tool_name,file_name: str) -> str:
    with open(os.path.join(base_dir,tool_name, file_name), "r") as f:
        return f.read()
    
def utf8(s):
        return s.encode('utf-8')