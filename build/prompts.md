# GFA skin render prompts (Higgsfield · nano_banana_pro · 2:3 portrait, 2K)

**Shared style suffix** (appended to each, for cross-skin coherence):
> Premium 3D-rendered digital-fashion garment, AAA videogame item-shop hero asset, ghost-mannequin presentation (invisible body, the outfit holds a full human silhouette), complete head-to-toe look, centered, floating in a pure black studio void, cinematic three-point rim lighting with a subtle cobalt-blue (#1B2BFF) volumetric glow, physically-based materials, ultra-detailed, octane/redshift quality, sharp focus, vertical composition. No text, no logo, no watermark, no human face, no mannequin head.

1. **Nebula Runner** — `nebula` — *Techwear / Legendary*
   Futuristic techwear outfit: cropped technical tank top with a tactical chest harness and metal buckle, layered utility belt with cargo pouches, baggy tapered cargo pants with a gradient hem fading from deep ink-black into glowing cyan (#39E0FF), floating fingerless tactical gloves. Matte black nylon with cyan accent piping.

2. **Prisma** — `prisma` — *Couture / Mythic*
   High-fashion couture gown: one-shoulder fitted iridescent bodice flowing into a long draped column skirt, fabric shifting through an iridescent gradient from electric cobalt blue into magenta-red, liquid-metallic sheen, elegant soft folds catching light, haute-couture runway piece.

3. **Gridlock** — `gridlock` — *Streetwear / Epic*
   Oversized streetwear fit: boxy cobalt-blue bomber jacket with ribbed orange-red cuffs and hem, bold pixel-grid graphic on the chest, baggy cargo shorts, chunky white high-top sneakers with red sole accents. Hypebeast game-skin energy.

4. **Obsidian Shell** — `obsidian` — *Avatar Armor / Rare*
   Sci-fi avatar armor: faceted matte-black hard-surface armor plates — angular chestplate, shoulder pauldrons, segmented abdominal guard, greaves — with glowing cobalt/periwinkle (#9AA6FF) edge-light seams tracing every panel and a small glowing core node on the chest. Mecha-couture.

## Pipeline per skin
1. generate_image (model nano_banana_pro, aspect_ratio 2:3, resolution 2k, count 2-3 for selection)
2. remove_background -> transparent cutout (sits on the deck's existing branded gradient stages)
3. downscale + WebP -> embed as manifest asset under a fixed UUID
4. wire via SKIN_IMG map in the GFA_SKINS module
