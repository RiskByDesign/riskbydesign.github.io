# RiskByDesign - site

Static portfolio and product site published at [riskbydesign.net](https://riskbydesign.net). Dark charcoal design with soft raised cards and a brass-gold accent, zero dependencies: plain HTML, CSS, and vanilla JavaScript. No build step, no frameworks, no external fonts or CDNs, no analytics.

## Structure

```
index.html        Home: hero, beliefs, work (products), contact
lab/              Product detail hub for FORLAS CRQ, Calibrated Course, BowCRQ
blog/             Writing (posts + index)
bowcrq/           Hidden (noindex) BowCRQ policy documents used for the
                  Play Store listing: privacy, security model, SBOM, licence
css/style.css     All styling (design tokens at the top in :root)
js/main.js        Mobile nav, scroll reveal, footer year
tools/            One-off regenerators (BowCRQ doc pages from source .md)
assets/           Logo, headshot, favicon, product screenshots
```
