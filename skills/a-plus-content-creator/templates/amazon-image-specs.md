# Amazon A+ Content Image Specifications

Amazon enforces strict image dimension and file rules per module type. Images outside spec get the module flagged or the entire A+ Content rejected. This file lists exact specs for every module supported by this skill.

## Cross-module image rules

These rules apply to every image in every module:

- **File format:** JPG or PNG only. No GIF, no WebP.
- **Color profile:** sRGB. Don't upload CMYK or Adobe RGB — Amazon will reject.
- **Max file size:** 5 MB per image. Most A+ images compress comfortably under 1 MB.
- **No text in image that overlaps content text elsewhere in the module** (text-on-text gets cropped by Amazon's mobile rendering and looks broken).
- **No price text in image.** Amazon controls all price display.
- **No promotional text** ("Sale", "Limited time", "Buy now") — Amazon strips these.
- **No copyrighted material.** Only use imagery the seller owns or has rights to.
- **No competitor brand names or logos in images.**
- **Accessibility:** if text is overlaid on an image, contrast ratio must meet WCAG AA. Amazon increasingly enforces this on auto-review.

When Fal AI generates the image, the skill enforces these rules via the negative prompt and the chosen image size.

When the buyer creates the image themselves (Canva or photographer), the brief explicitly cites the spec.

---

## Per-module image dimensions

### Module 1: Standard Company Logo
- Dimensions: **600 × 180 px**
- Aspect ratio: 10:3 (wide)
- Format: PNG with transparent background preferred

### Module 2: Standard Image Header With Text
- Dimensions: **970 × 600 px**
- Aspect ratio: ~16:9 / 1.6:1
- Mobile crop: Amazon may crop to ~970 × 300 on mobile — keep critical visual centered, both vertically and horizontally
- Format: JPG (photos) or PNG (graphics)

### Module 3: Standard Single Image & Highlights
- Single image dimensions: **300 × 300 px**
- Aspect ratio: 1:1 (square)
- Position: right column of module
- Format: JPG or PNG

### Module 4: Standard Single Image & Sidebar
- Primary image: **300 × 300 px** (square)
- Sidebar image: **350 × 175 px** (2:1 ratio)
- Both images appear simultaneously — visually relate them but don't make one redundant
- Format: JPG or PNG

### Module 5: Standard Four Image & Text
- Each of 4 images: **220 × 220 px** (square)
- All 4 images appear in a 2×2 grid
- **Style consistency required:** lighting, color palette, scale should be parallel across all 4. Mixing photo styles looks careless and reduces conversion.
- Format: JPG (photos preferred over graphics for visual consistency)

### Module 6: Standard Comparison Chart
- Per-product image (column header): **150 × 300 px** (1:2 portrait)
- Use the same photographic style across all columns — typically clean catalog-style product shots on white
- Format: JPG or PNG
- Background: white preferred for Amazon's comparison chart aesthetic

### Module 7: Standard Product Description Text
- No images.

### Module 8: Standard Single Side Image
- Image dimensions: **300 × 300 px** (square)
- Image on the left, text on the right (some Amazon templates allow swap)
- Format: JPG or PNG

### Module 9: Standard Image Header With Text Overlay
- Image dimensions: **970 × 300 px**
- Aspect ratio: ~3.2:1 (wide and short)
- **Critical:** image must have enough negative space for the text overlay to remain legible. Generally the left third or right third of the image should be relatively uncomplicated.
- Format: JPG (photographic atmospheres work best for overlay)

### Module 10: Standard Multiple Image Module
- Each of 4 images: **300 × 300 px** (square)
- All 4 appear in a single horizontal row
- Style consistency required (same as Module 5)
- Format: JPG or PNG

### Module 11: Standard Single Left Image
- Image dimensions: **300 × 300 px** (square)
- Image on the left, copy-heavy text on the right
- Format: JPG or PNG

### Module 12: Standard FAQ Module
- No images.

---

## Resolution and rendering

Amazon serves images at the dimensions listed above on most devices. On high-DPI displays (Retina, AMOLED), Amazon scales them up — which means a 300×300 image is shown at effective 600×600 on a 2x display.

**The recommendation:** generate or upload images at **2x the listed dimensions** for sharper rendering on modern devices. Amazon's spec lists minimum dimensions, not maximums. Don't go beyond 2-3x — file size grows quadratically.

For example:
- Module 2 hero: 970×600 spec → upload at 1940×1200 for retina-sharp rendering
- Module 5 grid cell: 220×220 spec → upload at 440×440

The skill's image generation step targets 2x dimensions by default. When briefing Canva designers, the brief notes "minimum [spec]; recommend [2x spec] for retina rendering."

---

## When images need to come from the buyer

Even when Fal AI is generating most module images, some are best sourced from the buyer's existing photo library:

- **Real product packaging shots** — generated images of branded packaging look fake
- **Photos of the buyer's actual workshop, team, or process** — for brand-story modules
- **Real customer-use photos** (UGC) — for use-case modules
- **The buyer's existing approved lifestyle photos** — when they exist and match the brand

The brief should flag these cases explicitly: "Recommended source: your own product packaging photo. Don't generate this one via Fal — it'll look uncanny."

---

## Image alt text per module

Every image in every module gets descriptive alt text. Amazon's character limit is typically 100 characters per alt text field.

Alt text guidelines:
- Describe what the image shows from a shopper's perspective
- Include 1 keyword from the cache when natural (don't stuff)
- Don't repeat the headline verbatim
- Write for screen-reader users, not for SEO bots

Example good alt text: "Hand-thrown ceramic pour-over coffee dripper brewing on a wooden countertop, steam rising in morning light"

Example bad alt text: "ceramic pour over coffee dripper handmade pour over coffee single cup brewer pour over"
