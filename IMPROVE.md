# Fresh Mic: notes for improvement runs

Live site: https://fresh-soldier.github.io/FRESH-MIC/
Music data and similarity come from Deezer; this site is non-commercial because Deezer's terms limit its data and previews to non-commercial use.

## Rules for automated improvement runs
- Edit `src/template.html` (design, layout, behavior). Never hand-edit `index.html`; run `python3 build.py` to regenerate it.
- Make ONE focused improvement per run. Test it in a browser (Playwright, Chromium at /opt/pw-browsers/chromium) at desktop (1100px) and phone (400px) width, with no console errors, before pushing.
- Do NOT add ads, affiliate links, analytics or trackers. The owner has not signed up for any program.
- Do NOT add new external hosts or API calls. The only exceptions are the Deezer preview call, the SoundCloud player (`w.soundcloud.com`), which loads only when a visitor adds their own SoundCloud link on the My page tab, and the Internet Archive (`archive.org`), used only by the Free music tab (see below). Keep every required credit and link back (see footer).
- Do NOT copy or re-host audio or artwork beyond the picture sheets already in `sheets/`.
- Do not put the owner's real name or email anywhere. Commit as `FRESH-SOLDIER <FRESH-SOLDIER@users.noreply.github.com>`.
- After pushing, wait 2 minutes and check that the live page returns 200 and its title is correct. If it is broken, revert the commit and push the revert.
- Append one line to `CHANGELOG.md`: date, what changed, why.

## My page (profile) rules
- It is client-side only: data lives in the visitor's browser (`freshmic:profile`) and in share links (`#page=...`). There are no accounts and no server.
- Everything read from a share link goes through `sanitizeProfile()`. Never insert it with innerHTML; use textContent. Only https://soundcloud.com permalinks may be embedded, and the player address is built in code, never copied from input.
- Keep a visible "Listen on SoundCloud" link under every embed and do not store or download SoundCloud audio or artwork.
- SoundCloud's terms do not allow embedding its player next to ads. If ads are ever added to the site, remove or rethink the SoundCloud embed first.
- Do not add uploads of audio or images, accounts, or any server calls without the owner's decision (copyright takedown duties, privacy duties and costs apply).

## My page v2 (deep customization) rules
- Every setting is an enum, a fixed-range number, a validated #rrggbb color or a short cleaned string. No user CSS, HTML or script, ever.
- Video: only the 11-character YouTube id is stored; the embed address is built in code on youtube-nocookie.com. SoundCloud as before.
- Sound is synthesized with Web Audio (no files). It never starts without a click. Respect prefers-reduced-motion (no particles, no background video, no animation).
- No image uploads or remote image URLs (they leak visitors' IPs and need a server). Emoji avatars only.
- Share links are compressed (#page=z...) and capped; decompression is size-limited.

## Free music tab rules (owner approved 2026-10-21)
- Source: Internet Archive search and metadata (JSONP) and its audio files, streamed straight from archive.org. Never copy, download or re-host audio or artwork.
- Only items whose licence URL passes `licOf()` (CC0, Public Domain Mark, CC BY 1.0-4.0, CC BY-SA 1.0-4.0) are listed. Never relax this list. No NonCommercial or NoDerivatives items, no unknown licences.
- The licence is re-checked from the item's own metadata before playing; if it cannot be confirmed, do not play.
- Always show the licence name linked to the official creativecommons.org page (built in code from the matched pattern, never copied from the data) and a link to the Internet Archive source page. Keep the "Before you reuse a song" notice and Copy credit.
- All uploader-supplied text is inserted with textContent only. Identifiers are validated before use in URLs.
- Do not add downloads, accounts or other sources without the owner's decision. Say plainly that the licence is declared by the uploader.
