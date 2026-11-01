# HTML Conventions for Tailwind Output

The HTML output is one `.html` file containing each page block as a self-contained Tailwind-styled `<section>`. Buyers can paste a block at a time into Shopify sections, PageFly/GemPages/Shogun, or any Tailwind-aware setup. This file specifies the conventions every block must follow.

---

## File-level structure

The output is a single `.html` file with this top-level shape:

```html
<!--
  Landing Page HTML — [Page name / Product name]
  Generated [date] · Brand: [brand_name] · Page type: [type]
  Framework: [chosen framework]

  USAGE:
  - Each <section> below is self-contained — copy and paste any block into your page builder.
  - Tailwind required (CDN load: <script src="https://cdn.tailwindcss.com"></script>)
  - Replace REPLACE_WITH_YOUR_IMAGE placeholders with your real image URLs.
  - All blocks are mobile-first and responsive.
-->

<section class="lp-hero">
  ...
</section>

<section class="lp-value-props">
  ...
</section>

...
```

Header comment lists block summary so the buyer can navigate quickly. Each block starts with a comment header (`<!-- HERO -->`, `<!-- VALUE PROPS -->`, etc.) for find-in-page navigation.

---

## Class naming convention

Each block-level `<section>` gets a class like:

| Block | Class |
|---|---|
| Hero | `lp-hero` |
| Value props | `lp-value-props` |
| Story | `lp-story` |
| Product walkthrough | `lp-walkthrough` |
| How it works | `lp-how-it-works` |
| Comparison | `lp-comparison` |
| Social proof | `lp-social-proof` |
| FAQ | `lp-faq` |
| Sticky CTA / final | `lp-final-cta` |
| Cross-sell | `lp-cross-sell` |
| Trust footer | `lp-trust-footer` |
| Collection hero | `lp-collection-hero` |
| Collection top-of-grid | `lp-collection-top` |
| Collection mid-break | `lp-collection-break` |
| About hero | `lp-about-hero` |
| About story | `lp-about-story` |
| About principles | `lp-about-principles` |
| About team | `lp-about-team` |

These let the buyer target blocks with custom CSS (e.g., to override Tailwind defaults with theme colors) without rewriting the HTML.

The classes are *additional* to Tailwind utility classes; they don't replace them. Style with Tailwind, identify with `.lp-*` classes.

---

## Tailwind class patterns

### Section container

Every `<section>` follows this base pattern:

```html
<section class="lp-[block-name] w-full py-12 md:py-20 px-4 md:px-8">
  <div class="max-w-7xl mx-auto">
    <!-- block content -->
  </div>
</section>
```

- `w-full` — full-width section background
- `py-12 md:py-20` — generous vertical padding, bigger on desktop
- `px-4 md:px-8` — horizontal padding, bigger on desktop
- `max-w-7xl mx-auto` — content max-width with horizontal centering

### Headlines

```html
<h1 class="text-3xl md:text-5xl font-bold tracking-tight text-gray-900">...</h1>
<h2 class="text-2xl md:text-4xl font-bold tracking-tight text-gray-900">...</h2>
<h3 class="text-xl md:text-2xl font-semibold text-gray-900">...</h3>
```

Heading hierarchy matters for SEO and accessibility. There should be exactly one `<h1>` per page (the hero headline). Subsequent block headlines are `<h2>`. Sub-points within blocks are `<h3>`.

### Body text

```html
<p class="text-base md:text-lg text-gray-700 leading-relaxed">...</p>
```

For longer paragraphs in the story / about blocks, use `leading-loose` for extra breathing room.

### CTAs (buttons)

```html
<a href="#" class="inline-flex items-center justify-center px-8 py-4 text-base md:text-lg font-semibold text-white bg-gray-900 rounded-lg hover:bg-gray-800 transition-colors">
  Shop the pour-over
</a>
```

CTA button colors should use theme tokens when shipped into a real theme. Defaults: `bg-gray-900` for primary CTAs, `bg-white text-gray-900 border border-gray-900` for secondary CTAs.

Mobile note: CTAs should be `w-full md:w-auto` so they're full-width on mobile (tappable) and natural-width on desktop.

### Grids (value props, walkthrough features)

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
  <!-- grid items -->
</div>
```

Mobile: 1 column. Tablet: 2. Desktop: 3 (sometimes 4 for icon-only value props).

### Image placeholders

Always use this format:

```html
<img
  src="REPLACE_WITH_YOUR_IMAGE"
  alt="[descriptive alt text — what the image should show]"
  width="1200"
  height="800"
  class="w-full h-auto rounded-lg object-cover"
/>
```

The `alt` attribute should describe what the image *should* be, written in instructional terms ("Hero shot: pour-over on a wooden countertop with steam rising"). The buyer replaces the alt text with shopper-facing alt text when they add the real image.

`width` and `height` should be the recommended image dimensions for the block (specified in the page-architecture file).

### Star ratings + review counts

```html
<div class="flex items-center gap-2">
  <div class="flex" aria-label="Rating: 4.8 out of 5">
    <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
    </svg>
    <!-- repeat star 5x; rendering of partial stars handled by theme -->
  </div>
  <span class="text-sm text-gray-700">4.8 · 1,247 reviews</span>
</div>
```

---

## Accessibility rules

Every HTML output must follow these accessibility minimums:

1. **Exactly one `<h1>`** per page — the hero headline.
2. **Heading hierarchy** is correct (`<h1>` → `<h2>` → `<h3>` — never skip levels).
3. **Every `<img>` has `alt` text.** Even decorative images get `alt=""`.
4. **Icon-only buttons have `aria-label`.** (e.g., a star-rating widget has `aria-label="Rating: 4.8 out of 5"`)
5. **CTA buttons use `<button>` or `<a href="#">` with descriptive text.** Never `<div onclick>`.
6. **Color contrast** — default Tailwind classes meet WCAG AA. If the buyer's theme overrides colors, that's their responsibility, but recommend testing.
7. **Form inputs (in newsletter capture or CTA forms) have `<label>` elements.** No placeholder-as-label.
8. **Skip-to-content link** for the marketing LP (single-purpose page where main content is the whole page).

---

## Mobile-first defaults

- All grids start at `grid-cols-1`, scale up with `md:` and `lg:` prefixes
- All text sizes start small, scale up with `md:` and `lg:` prefixes
- CTAs are `w-full md:w-auto`
- Padding scales: `py-12 md:py-20` (mobile gets less padding)
- Hide-on-mobile patterns: `hidden md:block` (for desktop-only content). Use sparingly — better to design content that works on both.

---

## Comments inside the HTML

Every block starts with a clear comment header for navigation:

```html
<!-- =================================================================
     HERO BLOCK
     Conversion job: 3-second qualification ("am I in the right place?")
     A/B test slot: see Hero A/B/C alternates at the bottom of this file
     ================================================================= -->
<section class="lp-hero ...">
  ...
</section>
```

Inline comments explain non-obvious styling choices:

```html
<!-- Visual rhythm break: this section uses a darker background to separate the story from the spec walkthrough -->
<section class="lp-story bg-gray-50 ...">
```

---

## Alternate hero placement

The three alternate heroes go *at the bottom of the file*, after all main page blocks, so the main page reads top-to-bottom cleanly. Each alternate is wrapped in a clearly-labeled section:

```html
<!-- =================================================================
     ALTERNATE HERO A — Problem-aware
     For A/B testing against the main hero above.
     ================================================================= -->
<section class="lp-hero lp-hero-alt-a ...">
  ...
</section>

<!-- =================================================================
     ALTERNATE HERO B — Outcome-aware
     ================================================================= -->
<section class="lp-hero lp-hero-alt-b ...">
  ...
</section>

<!-- =================================================================
     ALTERNATE HERO C — Social-proof-aware
     ================================================================= -->
<section class="lp-hero lp-hero-alt-c ...">
  ...
</section>
```

The buyer copies one alternate at a time into their A/B testing tool.

---

## What this output is NOT

- Not a full HTML document. No `<html>`, `<head>`, `<body>` tags. The output is a collection of paste-ready `<section>` blocks. The buyer's existing theme wraps them.
- Not JavaScript-driven. Static HTML + Tailwind only. Interactivity (carousels, accordions for FAQ, sticky bars) gets noted in a comment for the buyer to wire up in their theme.
- Not theme-locked. The HTML works in any setup where Tailwind is loaded. The buyer adjusts colors/fonts via their theme's Tailwind config.

---

## When the buyer's theme doesn't use Tailwind

If the buyer says "my theme doesn't use Tailwind," recommend they:

1. Add the Tailwind CDN script to their theme's `<head>`: `<script src="https://cdn.tailwindcss.com"></script>` (good for testing, not production)
2. OR install Tailwind via their theme's build process (production-ready)
3. OR use the .docx brief instead and have a designer/developer implement the design

Don't try to swap Tailwind for another framework on the fly — the HTML is built for Tailwind.
