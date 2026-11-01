# First-Run Onboarding

The first time any skill in The E-Commerce Seller plugin runs, walk the buyer through this flow. The whole thing should take 2-5 minutes. Save answers to `~/.the-ecommerce-seller/config/the-ecommerce-seller.config.json` (create the `~/.the-ecommerce-seller/config/` folder if it doesn't exist).

Use the AskUserQuestion tool for multi-choice questions where possible. For free-text answers (brand name, audience, voice examples), ask directly in chat.

---

## Section 1: Store basics

Ask in chat, free-text, one at a time or all at once:

1. What's your brand name?
2. Do you have a tagline or one-line description of what you sell?
3. Your store URL (if you have one — Shopify, Amazon storefront, Etsy shop, your own site)?
4. What's your primary product category? (e.g., "handmade leather goods", "supplements", "home decor", "kids' clothing")

Save to `config.store`.

---

## Section 2: Platforms

Use AskUserQuestion (multiSelect: true):

**Question:** Which platforms do you currently sell on?

**Options:**
- Shopify
- Amazon
- Etsy
- eBay
- Walmart
- TikTok Shop

Save the result to `config.platforms_enabled` as booleans. If the buyer says they're "thinking about adding X," include X — the skill will write copy for it when they're ready.

---

## Section 3: Brand voice — analyze or capture

If Shopify is connected and the buyer's store has at least 3 published products, prefer the analyze path. Otherwise use the questionnaire path.

### Analyze path

1. Pull 3-5 of the buyer's existing product descriptions via the Shopify connector.
2. Use the prompt in `voice-analysis-prompt.md` to infer:
   - Brand archetype
   - Tone (3-5 adjectives)
   - Vocabulary the brand uses repeatedly (`vocabulary_use`)
   - Words that are conspicuously absent (`vocabulary_avoid` — flag and confirm with buyer)
   - 2-3 short representative passages (`voice_examples`)
3. Present the inferred profile to the buyer in a clean summary:

   > "Here's what I'm reading from your existing listings:
   > - **Archetype:** Sage
   > - **Tone:** warm, knowledgeable, slightly bookish
   > - **Words you lean into:** crafted, considered, season, ritual
   > - **Words you seem to avoid:** cheap, sale, limited time
   >
   > Sound right? Edit anything before I save it."

4. Let the buyer edit. Save final profile to `config.brand_voice`. Set `captured_via: "analyzed"`.

### Questionnaire path

If analysis isn't possible, use the questionnaire in `voice-questionnaire.md`. Save to `config.brand_voice` with `captured_via: "questionnaire"`.

---

## Section 4: Audience

Ask in chat, free-text:

1. **Who do you sell to?** Two or three sentences. Demographics, life stage, what they care about.
2. **What problem are they trying to solve when they buy from you?**
3. **What's the aspiration?** What do they want their life to look like?

Save to `config.audience`.

If the buyer struggles with these questions, offer prompts:
- For #1: "Imagine your best customer. What's their morning look like?"
- For #2: "What were they doing before they found you?"
- For #3: "What's the photo they'd post after using your product?"

---

## Section 5: Output preferences

Use AskUserQuestion:

**Question:** Where should I save the description files?

**Options:**
- The current workspace folder (recommended)
- A specific subfolder (I'll ask which)
- Default to my Downloads folder

If they pick a specific subfolder, ask for the path. Save to `config.output_preferences.output_folder`. Empty string means workspace root.

---

## Section 6: Connector detection

This step is silent — don't ask the buyer. Just check which connectors are available right now and record the state:

- Try `mcp__mcp-registry__list_connectors` if available.
- Otherwise, attempt a low-cost ping (e.g., list_calendars for the Google Calendar connector, list_labels for Gmail) for each connector category and note success/failure.

Save results to `config.connectors_known` as one of: `"connected"`, `"not_installed"`, `"installed_but_unauthorized"`. Update this section any time the skill detects a change.

---

## Section 7: Optional API keys

Ask one question via AskUserQuestion:

**Question:** Do you have a Fal AI API key for image generation? (Used by the Ad Creative Generator and A+ Content Creator skills.)

**Options:**
- Yes, I'll paste it now
- I'll add one later (you'll still get Canva-ready specs for image work)
- I don't know what that is — explain later

If they pick option 1, ask for the key in chat (it'll be saved locally to `config.api_keys.fal_ai`). If option 3, send them a short note saying "Fal AI is a fast image generation service. The ad creative skills can produce finished ad images directly if you give it a key. Otherwise they output Canva briefs you'd build yourself."

---

## After onboarding

1. Write the completed config to `~/.the-ecommerce-seller/config/the-ecommerce-seller.config.json`.
2. Set `brand_voice.last_updated` to today's date.
3. Tell the buyer:

   > "All set. Your brand voice and store info are saved — every skill in The E-Commerce Seller plugin will use them automatically. You can update any of this anytime by saying 'redo my e-commerce seller onboarding.' Now, back to your original request..."

4. Continue with whatever the buyer originally asked for.

---

## Re-running onboarding

If the buyer says any of: "redo onboarding," "update my brand voice," "I changed my brand name," "rerun setup" — run the relevant sections again and overwrite the config. Confirm what you're about to change before overwriting in case they only meant one section.
