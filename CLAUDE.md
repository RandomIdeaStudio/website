# Website

The public website of Random Idea Studio: `index.html`, `privacy.html`, `second-shift-manager-privacy.html` (generated from the app's `PRIVACY.md` by `scripts/app_privacy_page.py`, English section only; regenerate, never edit by hand), `second-shift-manager-terms.html` (generated the same way from the app's `TERMS.md`), `second-shift-manager-delete-account.html` (hand-written account deletion page for Google Play, kept in line with the deletion paragraph of the app's `PRIVACY.md`), `style.css`, `favicon.svg` and `fonts/`. The contact address is randomideastudio.dev@gmail.com until the studio has its own e-mail (user decision, 23 Nov 2026). Hosted on GitHub Pages from `main` / root of the public repository RandomIdeaStudio/website, live at https://randomideastudio.com (domain registered at WEDOS/Vedos until 2027-11-23, DNS records at WEDOS, `CNAME` file written by GitHub, HTTPS enforced since 2026-11-23); setup and upkeep are in `README.md`.

## Rules
1. **Talk to the user in Czech.** Code, comments, commit messages and docs are in English.
2. **The site is English only** (user decision, 12 Nov 2026), so its texts live directly in the HTML; this is the exception to the studio rule about language files. Ask before adding another language.
3. **Zero maintenance is the goal** (user decision, 12 Nov 2026): plain HTML and CSS, no JavaScript, no build step, no framework, no cookies, no analytics, no forms, and nothing loaded from another server (fonts, images and icons are files in this repository). `scripts/check_site.py` enforces it. Ask before adding anything that would need updates.
4. **No phone number** on the site (user decision).
5. **Projects shown:** NumBeasts, Second Shift Manager, Steamy & Sparky: Jumping Secrets of Physics (labelled "Game · Arcade"), PDF Editor (added 24 Nov 2026 with a download button to `github.com/RandomIdeaStudio/PdfEditor/releases/latest` and the links to its code signing policy and privacy policy that SignPath Foundation requires; keep them). Other studio projects are not mentioned anywhere until the user says so.
6. **Brand:** colours from `../Branding/README.md`, headings in Nunito ExtraBold (`fonts/nunito-800.woff`, a Latin subset of `../Branding/fonts/Nunito.ttf` instanced at weight 800, WOFF with zlib), body text in the system font. Regenerate the subset with fontTools when characters outside Latin-1 are needed in headings.
7. **Accessibility baseline:** never rely on colour alone, touch targets at least 44 px, text scales with the browser font size, no flashing, the logo animation respects `prefers-reduced-motion`.
8. **Placeholders** are written `PLACEHOLDER` inside a `<span class="pending">`; the check fails while any is left.
9. **Verify before saying "done":** `.\scripts\test.ps1` (Windows) or `bash scripts/test.sh` (Linux, CI), and look at a changed page at phone width in light and dark mode.
10. **Git:** short-lived branches and pull requests, never force-push, ask before pushing to `main` (a push to `main` publishes the site).
11. **Keep docs true:** update this file and `README.md` with any change of structure or rules.
