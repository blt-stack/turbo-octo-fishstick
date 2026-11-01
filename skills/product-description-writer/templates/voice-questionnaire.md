# Voice Questionnaire (Fallback)

Use this when the buyer doesn't have existing listings to analyze. Ask these as a conversational block — don't make it feel like a form. Where helpful, offer 2-3 example answers so the buyer doesn't freeze.

---

**1. If your brand were a person at a dinner party, who would they be?**

Examples to offer if they stall: "The witty older sister who calls bullshit on diet culture." "The patient craftsman explaining how the joint is cut." "The slightly chaotic best friend who insists on ordering dessert."

Capture the gist and translate into a brand archetype (rebel, sage, lover, jester, caregiver, ruler, creator, innocent, magician, hero, everyman, explorer).

→ Save to `brand_voice.archetype`

---

**2. Pick three to five adjectives that describe how your brand should sound.**

Offer a starter palette: warm, witty, direct, technical, playful, irreverent, calm, urgent, lush, plainspoken, cheeky, reverent, no-nonsense, dreamy, sharp.

→ Save to `brand_voice.tone` as a single string like "warm, witty, plainspoken"

---

**3. What words or phrases do you use a lot — or want to?**

Could be product-specific (e.g., "slow craft", "single-origin", "field-tested") or values-based (e.g., "never on sale", "made to last"). 5-10 is enough.

→ Save to `brand_voice.vocabulary_use` as an array

---

**4. What words do you never want to see in your copy?**

Common ones: "luxurious" (overused), "buy now" (pushy), "limited time" (manipulative), "girl boss" (dated), corporate-speak like "synergy" or "leverage." Get the buyer to name their own.

→ Save to `brand_voice.vocabulary_avoid` as an array

---

**5. Do you have 2-3 paragraphs of copy you've already written that capture your voice?**

This could be an About page, a launch email, a product description you're proud of, or an Instagram caption. If yes, paste them in. If no, skip — the previous answers are enough.

→ Save to `brand_voice.voice_examples` as an array of strings

---

## After capturing

Restate the captured voice profile back to the buyer in plain language and ask "sound right?" before saving. Buyers often realize what they meant only when they hear it played back.

Example readback:

> "OK, here's the voice I've got:
> - **Archetype:** The patient craftsman
> - **Tone:** plainspoken, warm, technical
> - **Lean into:** field-tested, made to last, slow craft
> - **Never:** luxurious, buy now, limited time
>
> Want to tweak anything?"
