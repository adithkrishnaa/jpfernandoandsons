# J.P. Fernando & Sons — website

A rebuilt static website for jpfernandoandsons.com. It has no framework and no server-side code, and it can be hosted anywhere that serves static files.

## Folders

| Folder | What it is |
|---|---|
| *(repo root)* | **The finished website**: `index.html`, the page folders, `assets/`, `404.html`, `sitemap.xml`, `robots.txt`. Upload these to the web host. |
| `src/content.py` | All page text, products, brands and contact details. Edit this to change content. |
| `src/build.py` | Page templates. Generates every HTML page into the repo root. |
| `assets/css/main.css` | Design system: colours, type, layout, animation. |
| `assets/js/main.js` | Interactions: the hero net, scroll reveals, the product explorer, the enquiry list and forms. |
| `assets/img/` | Images, all taken from the original site and the company banner. |

## Change content and rebuild

```bash
python src/build.py
```

Then preview locally:

```bash
python -m http.server 8770
```

Open http://localhost:8770. Pages use clean URLs (`/ropes/pp/`), so preview through a server rather than by double-clicking the files.

## URLs

All 16 original WordPress URLs are kept, so existing links and search results still work. New pages: `/products/`, `/brands/`, plus `404.html`, `sitemap.xml` and `robots.txt`.

## Enquiry form: important

Right now, pressing **Send enquiry** opens the visitor's email app with the enquiry written out, addressed to contact@jpfernando.com and dinesh@jpfernando.com. Nothing is sent without that email app.

To have forms deliver straight to an inbox, open `src/content.py` and fill in one value:

- **Web3Forms** (recommended): paste the access key into `FORM_ACCESS_KEY`.
- **Formspree** or any other service: paste the form URL into `FORM_ENDPOINT`.

Then run `python src/build.py` and upload the website files again. Every form on the site will send directly, show a real success or failure message, and include the visitor's enquiry list. A hidden spam trap blocks simple bots.

## Things to confirm with the client

- **WhatsApp:** not linked, because no WhatsApp number is published anywhere. Add one if they want it.
- **Product specifications:** the old site gave no sizes or specs, so product pages ask buyers for their size and quantity instead of listing figures. Add real specs in `content.py` when the client supplies them.
- **Product photos:** the `prod-*.jpg` images (nylon nets, fishing lines, PP, Vinylon and Kuralon rope, Kuralon twine, TORAY yarn, fishing accessories) come from the client's product image sheet. Older photos stay in each page's gallery.
- **Cricket, safety and agriculture net photos:** these are free photos from Wikimedia Commons, not the company's own. Their licences need the photo credit in the footer (`PHOTO_CREDITS` in `content.py`). Replace them with real product photos when possible, and remove the matching credit.
- **Better photography:** most original images are small (about 800 px wide). New high-resolution photos of the products and the Sea Street store would lift the whole site.
