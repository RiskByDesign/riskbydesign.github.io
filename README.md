# M. Walker / RiskByDesign - personal site

Static portfolio and product site. Dark charcoal portfolio with soft raised cards and a brass-gold accent, zero dependencies: plain HTML, CSS, and vanilla JavaScript. No build step, no frameworks, no external fonts or CDNs, no analytics.

## Structure

```
index.html        Single page: hero, what I believe in, work, contact
css/style.css     All styling (design tokens at the top in :root)
js/main.js        Mobile nav, scroll reveal, footer year
assets/           MW_BR.PNG (logo), 1729897914759.jpg (headshot),
                  favicon.svg, logo.svg (unused vector recreation, kept as backup)
```

## Logo and headshot

The header shows `assets/MW_BR.PNG` cropped to the monogram inside a white rounded badge. The crop is a CSS transform on `.brand-badge img` in `css/style.css`; adjust the `scale`/`translateY` values there if the framing needs a nudge. The hero photo is `assets/1729897914759.jpg`; replace that file to change the headshot (a square image works best).

## Before launch: things to confirm

1. **Email**: contact card uses `cyber@2600.host`.
2. **LinkedIn**: links to `linkedin.com/in/michael-w-b8b551159`.
3. **GitHub repo links**: cards link to `github.com/RiskByDesign/forlas-crq` and `github.com/RiskByDesign/calibration-trainer`. Confirm those are the public repo paths after the handle rename.

## Adding sales later

Each product card has a `SALES SLOT` comment in `index.html`. When a paid edition ships, add the second button shown in the comment (pointing at your Stripe/Gumroad/checkout URL) and update the "Free during beta" note. No layout changes needed.

## Preview locally

```powershell
cd E:\Development\website
python -m http.server 8080
# open http://localhost:8080
```

Or just open `index.html` directly in a browser; everything works from disk.

## Deploy (free options)

- **GitHub Pages**: push this folder to a repo, enable Pages on the main branch. If the repo is named `riskbydesign.github.io` it serves at that URL directly.
- **Cloudflare Pages**: connect the repo, no build command, output directory `/`. Fast, free, custom domain support.

If you buy a domain (for example `riskbydesign.dev`), point it at either host and set the email alias on the same domain.

## Design tokens

Colours, fonts, and spacing live in the `:root` block at the top of `css/style.css`. The palette is charcoal surfaces (`--bg`, `--card-top`, `--card-bottom`), soft dual shadows for the raised-card look (`--shadow-out`), and a brass-gold accent (`--accent`) taken from the logo's dot. Change `--accent` and `--accent-bright` to retheme in two lines. The font stack is Aptos first, falling back to Segoe UI Variable / Segoe UI / system-ui; all system fonts, nothing downloaded.
