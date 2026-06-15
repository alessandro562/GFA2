#!/usr/bin/env python3
"""GFA deck bundle tool.

The deck is a self-contained HTML "bundle": three <script> blocks carry the
data, and a runtime loader (see top of the HTML) decodes them.

  - script[type="__bundler/manifest"]      -> JSON: { uuid: {mime, compressed, data(base64)} }
  - script[type="__bundler/ext_resources"] -> JSON: [ {id, uuid}, ... ]
  - script[type="__bundler/template"]       -> JSON-encoded string: the actual page HTML

At runtime the loader replaces every occurrence of each manifest UUID inside the
template with a blob: URL built from the (base64) asset bytes. So to add an
image we (1) add a manifest entry, (2) reference its UUID anywhere in the
template (e.g. background-image:url("UUID") or <img src="UUID">).

Usage:
  python3 build/bundle_tool.py decode <deck.html> <outdir>
  python3 build/bundle_tool.py pack   <deck.html> <indir> <out.html>
  python3 build/bundle_tool.py addimg <indir> <uuid> <image_path> [--mime auto]
"""
import sys, os, re, json, base64, mimetypes

BLOCKS = {
    "manifest":      r'<script type="__bundler/manifest">(.*?)</script>',
    "ext_resources": r'<script type="__bundler/ext_resources">(.*?)</script>',
    "template":      r'<script type="__bundler/template">(.*?)</script>',
}

def _read(p):
    with open(p, "r", encoding="utf-8") as f:
        return f.read()

def decode(deck_path, outdir):
    html = _read(deck_path)
    os.makedirs(outdir, exist_ok=True)
    for name, pat in BLOCKS.items():
        m = re.search(pat, html, re.S)
        if not m:
            raise SystemExit(f"block not found: {name}")
        raw = m.group(1).strip()
        data = json.loads(raw)
        if name == "template":
            # template is a JSON-encoded HTML string -> write the decoded HTML
            with open(os.path.join(outdir, "template.html"), "w", encoding="utf-8") as f:
                f.write(data)
        else:
            with open(os.path.join(outdir, f"{name}.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
    print(f"decoded -> {outdir} (manifest.json, ext_resources.json, template.html)")

def pack(deck_path, indir, out_path):
    html = _read(deck_path)
    manifest = json.load(open(os.path.join(indir, "manifest.json"), encoding="utf-8"))
    ext = json.load(open(os.path.join(indir, "ext_resources.json"), encoding="utf-8"))
    template = _read(os.path.join(indir, "template.html"))
    # The deck's own inline <script> blocks live inside the template string;
    # a literal </script> would close the __bundler/template wrapper early, so
    # escape it as <\/script> (json.loads decodes it straight back). Harmless on
    # the other blocks, applied uniformly for safety.
    def enc(obj):
        return json.dumps(obj, separators=(",", ":")).replace("</script>", "<\\/script>")
    payloads = {
        "manifest":      enc(manifest),
        "ext_resources": enc(ext),
        "template":      enc(template),
    }
    for name, pat in BLOCKS.items():
        repl = f'<script type="__bundler/{name}">\n{payloads[name]}\n</script>'
        html, n = re.subn(pat, lambda m: repl, html, count=1, flags=re.S)
        if n != 1:
            raise SystemExit(f"failed to replace block: {name}")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"packed -> {out_path} ({os.path.getsize(out_path)//1024} KB)")

def addimg(indir, uuid, image_path, mime="auto"):
    mpath = os.path.join(indir, "manifest.json")
    manifest = json.load(open(mpath, encoding="utf-8"))
    if mime == "auto":
        mime = mimetypes.guess_type(image_path)[0] or "image/webp"
    with open(image_path, "rb") as f:
        b = f.read()
    manifest[uuid] = {"mime": mime, "compressed": False,
                      "data": base64.b64encode(b).decode("ascii")}
    json.dump(manifest, open(mpath, "w", encoding="utf-8"), indent=2)
    print(f"added asset {uuid} ({mime}, {len(b)//1024} KB) -> {mpath}")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__); raise SystemExit(1)
    cmd = a[0]
    if cmd == "decode": decode(a[1], a[2])
    elif cmd == "pack": pack(a[1], a[2], a[3])
    elif cmd == "addimg":
        mime = "auto"
        if "--mime" in a:
            mime = a[a.index("--mime")+1]
        addimg(a[1], a[2], a[3], mime)
    else:
        raise SystemExit(f"unknown cmd: {cmd}")
