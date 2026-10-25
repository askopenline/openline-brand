import json, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
state=Path(sys.argv[1])
changed=json.loads((state/"public-change-list.json").read_text())
names=set(changed)|{"index.html","studio.html"}
names.update(str(p.relative_to(root/"dist")) for p in (root/"dist/assets").rglob("*") if p.is_file())
assert all((root/"dist"/name).is_file() for name in names)
(state/"release-files.json").write_text(json.dumps(sorted(names),indent=2))
print("Release files:",len(names),"bytes:",sum((root/"dist"/n).stat().st_size for n in names))
