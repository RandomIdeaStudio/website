# Random Idea Studio – website

The studio's public website: three static pages, one stylesheet and one font file. No JavaScript, no build step, no cookies, no analytics and nothing loaded from other servers, so there is nothing to update or maintain.

## Files

| File | What it is |
|---|---|
| `index.html` | The home page: the studio, how we work, the projects, contact and company details |
| `privacy.html` | Privacy policy of the website |
| `second-shift-manager-privacy.html` | Privacy policy of the Second Shift Manager app (Google sign-in and the stores link to it). Generated from the English section of `../SecondShiftManager/PRIVACY.md` with `scripts/app_privacy_page.py`; never edit it by hand, regenerate it whenever the app's policy changes |
| `style.css` | All styles of the pages (dark by default, light when the system asks for it) |
| `favicon.svg` | Browser tab icon (the studio mark) |
| `fonts/nunito-800.woff` | Nunito ExtraBold for headings, a Latin subset made from `../Branding/fonts/Nunito.ttf`; licence in `fonts/OFL.txt` |
| `.nojekyll` | Tells GitHub Pages to publish the files as they are |
| `scripts/` | The check run before publishing (`test.ps1` / `test.sh` → `check_site.py`) and `app_privacy_page.py`, which makes an app's privacy page |

Everything outside the table (README, scripts, CI) is also visible on the published site's repository, which is public; nothing secret belongs here.

## Change a text

Edit `index.html` or `privacy.html`, then run the check:

```powershell
.\scripts\test.ps1
```

```bash
bash scripts/test.sh
```

It fails when a page loads something from another server, has a script, links to a missing file or anchor, or still contains `PLACEHOLDER`. Commit and push; GitHub Pages republishes within a minute or two.

## Where it runs today

- Repository: RandomIdeaStudio/website (public), GitHub Pages from `main` / root.
- Address: https://randomideastudio.com (www redirects to it), HTTPS enforced.
- Domain: registered at WEDOS (Vedos brand) until 2027-11-23; its DNS records in the WEDOS administration: four `A` and four `AAAA` records of GitHub Pages on the apex and `www` as a `CNAME` to `randomideastudio.github.io`.

## Publish on GitHub Pages (once)

GitHub Pages is free for public repositories.

1. Create a public repository (for example `website`) and push this folder to its `main` branch.
2. Repository → **Settings → Pages**: *Source* = **Deploy from a branch**, branch **main**, folder **/ (root)**.
3. Same page, **Custom domain**: enter the domain (for example `randomideastudio.cz`) and save. GitHub adds a `CNAME` file to the repository; pull it.
4. At the domain registrar set the DNS records:
   - apex domain: four `A` records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` and four `AAAA` records `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`,
   - `www`: a `CNAME` record pointing to `<github-account>.github.io`.
5. When the DNS check passes, tick **Enforce HTTPS**. The certificate is issued and renewed automatically.
6. Account or organization → **Settings → Pages → Verified domains**: verify the domain, so nobody else can publish a site on it.

Check the current values of the IP addresses in GitHub's documentation ("Managing a custom domain for your GitHub Pages site") when setting them up.

## The only upkeep

- Keep the domain renewing automatically and the registrar's payment card valid. An expired domain is the only thing that can take the site down.
- Update the company details if they change (registered office, name).
