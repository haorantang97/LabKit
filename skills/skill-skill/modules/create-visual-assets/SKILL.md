---
name: create-visual-assets
description: "Create or revise a repository's hero, theme variants, social preview and badge row. Use for repository visual assets or a README renovation; apply the supplied reference and product identity. Use an appropriate image tool for raster illustration."
license: PolyForm-Noncommercial-1.0.0
---

# Repository visual assets

Read the [repository presentation standard](../../references/repository-presentation.md) before designing. Inspect the repository identity and its existing rendered assets, not just filenames.

Resolve style from the user's reference or assets/STYLE.md. A supplied reference is already a style choice. If the user asks for the same style, closely preserve its composition, motif language, palette, typography and spacing; change the target name and factual copy. Do not reinterpret a same-style request as permission to invent a different visual identity. Ask only for a consequential missing preference. With no reference, choose a restrained product-specific direction and record it.

Design a visual motif that explains the repository: a collection uses its own name and represents its independent tools. Internal module names stay inside their component. Match palette, typography and supporting graphics across the page. Do not default to a copied blank rectangle with a new title.

Produce light and dark SVGs for vector compositions. Preserve established asset paths where practical; otherwise update every consumer. Use a viewBox, accessible title/description, deliberate spacing and readable text. Choose dimensions for the composition and inspect scaling rather than enforcing a fixed template size. For photos or complex raster artwork, use the relevant image-generation/editing capability.

Embed theme variants through picture/source plus img fallback, with descriptive alt text and a sensible display width. Store assets in the repository. Record the motif, colors, type choices, references and dimensions in assets/STYLE.md.

When social sharing is in scope, create a dedicated 1280 × 640 PNG with the same identity and a legible title at thumbnail size. Verify separately whether GitHub's social-preview setting actually uses it.

Use a small badge row tied to real facts. CI links must name their actual coverage. License badges must match the applicable license; release badges need a real tag/release. Avoid empty links, static update dates that imply activity, unsupported popularity and inflated module counts.

Render and inspect both themes at README width and a narrow width. Read the words inside the artwork, check clipping/contrast, then inspect the hero in the assembled page. Search for obsolete parent names and template tokens. Report asset creation, visual inspection and remote configuration separately.
