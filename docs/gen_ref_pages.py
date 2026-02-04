
"""Generate the code reference pages."""
from pathlib import Path
import mkdocs_gen_files

root = Path(__file__).parent.parent
src = root / "src" / "LASMnemonicsID"

for path in sorted(src.rglob("*.py")):
    module_path = path.relative_to(src.parent).with_suffix("")
    doc_path = path.relative_to(src.parent).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)
    
    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue
        
    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = ".".join(parts)
        print(f"::: {identifier}", file=fd)
    
    mkdocs_gen_files.set_edit_path(full_doc_path, path)
