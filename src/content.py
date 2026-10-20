"""Site content. Every fact here comes from the original jpfernandoandsons.com
pages, the company's own banner artwork or its business card. Do not add
claims that cannot be traced back to the company."""

SITE = "https://www.jpfernandoandsons.com/"
NAME = "J.P. Fernando & Sons"
NAME_SI = "ජේ. පී. ප්‍රනාන්දු සහ පුත්‍රයෝ"
NAME_TA = "J. P. பெர்னாண்டோ அன் சன்ஸ்"   # as printed on the business card
FOUNDED = 1953
EMAIL = "jpfernandoandsons287@gmail.com"
ADDRESS = ["No. 287/1, Sea Street", "Colombo 11", "Sri Lanka"]
PHONES = [
    # (display, tel, label) — contact details from the business card
    ("+94 11 243 5634", "+94112435634", "Office"),
    ("+94 11 243 5636", "+94112435636", "Office"),
    ("+94 11 247 3342", "+94112473342", "Office"),
]
MOBILE = ("+94 76 239 2263", "+94762392263")   # mobile and WhatsApp
HOURS = [("Monday – Friday", "9:00 – 17:00"), ("Saturday", "9:00 – 13:00"), ("Sunday", "Closed")]
MAP_Q = "287/1 Sea Street, Colombo 11, Sri Lanka"

# Social media profiles for the floating quick-access bar, menu and footer.
# Paste the full profile URL to show an icon; leave "" to hide it.
# whatsapp takes the number in international format, digits only, e.g. "94762392263".
SOCIAL = {
    "facebook": "",
    "instagram": "",
    "linkedin": "",
    "x": "",
    "whatsapp": "94762392263",
}

# Enquiry form delivery. Fill in ONE of these, then run: python src/build.py
#   Web3Forms: paste the access key emailed to you (endpoint is filled in automatically)
#   Formspree: paste your form URL, e.g. "https://formspree.io/f/abcdwxyz"
# Leave both empty and the form falls back to opening the visitor's email app.
FORM_ACCESS_KEY = ""   # Web3Forms access key
FORM_ENDPOINT = ""     # Formspree (or any other service) form URL

# ---------------------------------------------------------------------------
# Product categories (top level) and their product pages (children)
# group: used by the products hub filter
# ---------------------------------------------------------------------------
CATEGORIES = [
    {
        "slug": "nylon-fishing-nets/",
        "name": "Nylon Fishing Nets",
        "title_html": "Nylon <em>fishing nets</em>",
        "group": "nets",
        "img": "nylon-nets.jpg",
        "fit": "cover",
        "blurb": "Our own SuperCatch nets, knitted locally from TORAY Japan yarn, alongside imported Japanese-technology nets.",
        "intro": "Fishing nets bring in the largest share of Asia's catch, and they are made in many configurations depending on the species being targeted.",
        "tag": [("Made in", "Sri Lanka, on Japanese machines"), ("Yarn", "TORAY Japan nylon")],
        "body": [
            ("p.big", "Nylon nets are where J.P. Fernando & Sons began. In 1953 the company became the first in Sri Lanka to distribute imported fishing nets, and nylon netting is still the heart of the business."),
            ("h2", "Made here, from the best yarn we know"),
            ("p", "Since the mid-1990s we have manufactured our own brands of nylon fishing nets in Sri Lanka using the latest Japanese machines. Every one of our own net brands is made from TORAY Japan nylon yarn — the material behind our &ldquo;Quality First&rdquo; principle."),
            ("p", "Alongside our own nets we distribute leading imported brands, so buyers can choose the net that suits their fishery and their budget."),
            ("h3", "Brands in this range"),
            ("ul", ["<strong>SuperCatch</strong> — our own brand, one of the most popular quality net brands in Sri Lanka today.", "<strong>Nitto</strong> — Japanese-technology fishing nets, &ldquo;engineered for big catch and for long time use&rdquo;."]),
        ],
        "ask": ["Mesh size and twine thickness", "Net depth and length", "Colour", "Quantity required"],
        "children": ["super-catch", "nitto"],
        "gallery": [("nylon-nets.jpg", "Nylon fishing nets"), ("supercatch-logo.jpg", "SuperCatch brand mark"), ("nitto-poster.jpg", "Nitto Japanese-technology fishing nets"), ("acc-cast-net.jpg", "Hand-thrown cast net")],
    },
    {
        "slug": "hdpe-fishing-nets/",
        "name": "HDPE Fishing Nets",
        "title_html": "HDPE <em>fishing nets</em>",
        "group": "nets",
        "img": "hdpe-net-wide.jpg",
        "fit": "cover",
        "blurb": "Strong, hard-wearing high-density polyethylene netting in green, blue and white — made to your requirements.",
        "intro": "HDPE fishing nets are made from premium-quality high-density polyethylene, a strong and hard-wearing material.",
        "tag": [("Colours", "Green · Blue · White"), ("Made to", "Your thickness & length")],
        "body": [
            ("p.big", "HDPE nets are made from premium-quality high-density polyethylene, which gives a strong, hard netting."),
            ("h2", "Bright colours, built to order"),
            ("p", "Our HDPE fishing nets come in bright colours such as green, blue and white. They are available in different thicknesses and lengths, and can be customised to each customer's requirements."),
            ("ul", ["Available in green, blue and white", "Choice of twine thickness", "Supplied in different lengths", "Can be customised to your specification"]),
        ],
        "ask": ["Thickness required", "Length and depth", "Colour", "Quantity required"],
        "children": [],
        "gallery": [("hdpe-net-wide.jpg", "Blue HDPE netting"), ("hdpe-net.jpg", "HDPE net bundles")],
    },
    {
        "slug": "fishing-lines/",
        "name": "Fishing Lines",
        "title_html": "Monofilament <em>fishing lines</em>",
        "group": "lines",
        "img": "monofilament.jpg",
        "fit": "cover",
        "blurb": "Monofilament line in a range of diameters and colours — from clear to fluorescent.",
        "intro": "Most fishing lines today are monofilament: economical to produce and made in a wide range of diameters.",
        "tag": [("Type", "Monofilament"), ("Colours", "Clear to fluorescent")],
        "body": [
            ("p.big", "Most fishing lines are now monofilament, because monofilament fibre is economical to produce and is made in a wide range of diameters."),
            ("h2", "Choose your diameter and colour"),
            ("p", "Monofilament line is manufactured in many colours, including clear, white, green, blue, red and fluorescent. Tell us the diameter and colour you need and we will advise on availability."),
            ("ul", ["Wide range of diameters", "Clear, white, green, blue, red and fluorescent colours", "For hand-lines and net-making alike"]),
        ],
        "ask": ["Line diameter", "Colour", "Spool or hank size", "Quantity required"],
        "children": [],
        "gallery": [("monofilament.jpg", "Monofilament line hanks"), ("acc-mono.jpg", "Packed monofilament line")],
    },
    {
        "slug": "ropes/",
        "name": "Ropes",
        "title_html": "Fishing <em>ropes</em>",
        "group": "lines",
        "img": "ropes.jpg",
        "fit": "contain",
        "blurb": "HDPE, PP and Vinylon ropes in a range of sizes and colours, including our own SuperCatch rope.",
        "intro": "Today's fishing methods demand high rope performance — which is why we carry ropes in three materials and many sizes.",
        "tag": [("Materials", "HDPE · PP · Vinylon"), ("Brand", "SuperCatch")],
        "body": [
            ("p.big", "Today's advanced fishing methods demand high performance from rope. That is why we stock a range of ropes in different materials and sizes."),
            ("h2", "Three materials, many sizes"),
            ("p", "Our rope range covers HDPE, PP (polypropylene) and Vinylon. Ropes are supplied in coils in a choice of colours, with many carrying our own SuperCatch label."),
        ],
        "ask": ["Material (HDPE, PP or Vinylon)", "Diameter", "Coil length", "Colour and quantity"],
        "children": ["hdpe", "pp", "vinylon"],
        "gallery": [("ropes.jpg", "SuperCatch rope coils"), ("rope-orange.jpg", "Rope hanks"), ("rope-twisted.jpg", "Twisted rope coils"), ("rope-green.jpg", "Green and black rope coils"), ("rope-white.jpg", "White rope coils"), ("rope-hanks.jpg", "White rope hanks")],
    },
    {
        "slug": "fishing-tackles-and-swivel/",
        "name": "Fishing Tackles & Swivels",
        "title_html": "Tackle <em>&amp; swivels</em>",
        "group": "tackle",
        "img": "lures.jpg",
        "fit": "contain",
        "blurb": "Hooks, lures, sinkers, floats and swivels — the working kit of every angler.",
        "intro": "Fishing tackle is the equipment anglers use when fishing — almost any piece of fishing gear can be called tackle.",
        "tag": [("For", "Anglers & boat crews"), ("Includes", "Hooks · Lures · Swivels")],
        "body": [
            ("h2", "Fishing tackle"),
            ("p", "Fishing tackle is the equipment anglers use when fishing. Almost any equipment used for fishing can be called tackle — hooks, lines, sinkers, floats, rods, reels, baits, lures, spears, nets, gaffs, traps, waders and tackle boxes."),
            ("h2", "Swivels"),
            ("p", "Fishing swivels range in size from a few millimetres to several centimetres. They are traditionally flat black or brass in colour, while more modern swivels also come in lustrous red and blue. Swivel colour may even play a part in attracting fish, especially in low light."),
        ],
        "ask": ["Item type", "Size or weight", "Finish or colour", "Quantity required"],
        "children": [],
        "gallery": [("lures.jpg", "Jointed fishing lures"), ("acc-hook-swivel.jpg", "Hook and swivel"), ("acc-lures-feather.jpg", "Feather lures and feeders"), ("acc-reel.jpg", "Spinning reel and lures")],
    },
    {
        "slug": "fishing-accessories/",
        "name": "Fishing Accessories",
        "title_html": "Fishing <em>accessories</em>",
        "group": "tackle",
        "img": "acc-floats.jpg",
        "fit": "cover",
        "blurb": "Floats, cast nets, reels, rods and diving gear — the everyday items that keep fishing going.",
        "intro": "Beyond nets and rope, we supply the everyday accessories that fishermen and anglers rely on.",
        "tag": [("Includes", "Floats · Reels · Rods"), ("Also", "Masks & fins")],
        "body": [
            ("p.big", "Beyond nets, lines and ropes, we supply the accessories that fishing crews and anglers rely on every day."),
            ("h2", "What you'll find"),
            ("p", "Our accessories range includes items such as:"),
            ("ul", ["Net floats", "Hand-thrown cast nets", "Spinning reels and fishing rods", "Hooks, swivels and lures", "Snorkelling masks, snorkels and fins"]),
            ("p", "Stock changes through the year, so please contact us to check what is currently available."),
        ],
        "ask": ["Item you are looking for", "Size or model", "Quantity required"],
        "children": [],
        "gallery": [("acc-floats.jpg", "Net floats"), ("acc-cast-net.jpg", "Cast net"), ("acc-reel.jpg", "Spinning reel"), ("acc-rods.jpg", "Fishing rods and reels"), ("acc-snorkel.jpg", "Mask, snorkel and fins"), ("acc-hook-swivel.jpg", "Hook and swivel")],
    },
    {
        "slug": "nylon-yarn-twine/",
        "name": "Nylon Yarn & Twine",
        "title_html": "Nylon <em>yarn &amp; twine</em>",
        "group": "yarn",
        "img": "toray-yarn.jpg",
        "fit": "cover",
        "blurb": "TORAY Japan nylon yarn — we are the sole agent and single distributor for TORAY products in Sri Lanka.",
        "intro": "Nylon, the world's first synthetic fibre, was first produced on a large scale in Japan by Toray in 1951.",
        "tag": [("Brand", "TORAY Japan"), ("Status", "Sole agent in Sri Lanka")],
        "body": [
            ("p.big", "Nylon, the world's first synthetic fibre, was first manufactured on a large scale in Japan by Toray in 1951."),
            ("h2", "TORAY yarn, Japan"),
            ("p", "Nylon offers excellent tensile strength, abrasion resistance and chemical resistance, as well as good colour properties. In industry it is used for tyre cords, carpets and — most importantly for us — fishing nets. Toray has the largest share of the nylon market in Japan."),
            ("p", "J.P. Fernando &amp; Sons is the sole agent and single distributor of TORAY products in Sri Lanka, and TORAY Japan yarn goes into every one of our own net brands."),
        ],
        "ask": ["Yarn or twine type", "Denier or ply", "Quantity required"],
        "children": ["toray"],
        "gallery": [("toray-yarn.jpg", "TORAY nylon yarn bobbins")],
    },
]

PRODUCTS = {
    "super-catch": {
        "parent": "nylon-fishing-nets/",
        "slug": "nylon-fishing-nets/super-catch/",
        "name": "SuperCatch",
        "title_html": "Super<em>Catch</em>",
        "kind": "Nylon fishing nets · Our own brand",
        "img": "supercatch-logo.jpg",
        "fit": "contain",
        "blurb": "Our own nylon net brand, knitted in Sri Lanka from TORAY Japan yarn.",
        "tag": [("Brand", "SuperCatch"), ("Maker", "J.P. Fernando & Sons")],
        "body": [
            ("p.big", "SuperCatch is J.P. Fernando &amp; Sons' own brand — today one of the most popular quality fishing-net brands in Sri Lanka."),
            ("p", "SuperCatch nets are manufactured locally on the latest Japanese machines, using TORAY Japan nylon yarn. The SuperCatch name also appears on our rope range."),
        ],
        "spec": [("Brand", "SuperCatch"), ("Manufactured by", "J.P. Fernando & Sons, Sri Lanka"), ("Yarn", "TORAY Japan nylon"), ("Machinery", "Japanese net-making machines"), ("Also available", "SuperCatch ropes")],
        "gallery": [("supercatch-logo.jpg", "SuperCatch brand mark"), ("nylon-nets.jpg", "Nylon fishing nets"), ("ropes.jpg", "SuperCatch rope coils")],
    },
    "nitto": {
        "parent": "nylon-fishing-nets/",
        "slug": "nylon-fishing-nets/nitto/",
        "name": "Nitto",
        "title_html": "Nitto",
        "kind": "Nylon fishing nets · Japanese technology",
        "img": "nitto-poster.jpg",
        "fit": "contain",
        "blurb": "Japanese-technology fishing nets, engineered for big catch and long use.",
        "tag": [("Brand", "Nitto"), ("Technology", "Japanese")],
        "body": [
            ("p.big", "Nitto nets are presented as &ldquo;Japanese Technology Fishing Nets&rdquo; — engineered for big catch and for long time use."),
            ("p", "We distribute Nitto nets as part of our nylon net range. Contact us for the mesh sizes, depths and quantities currently available."),
        ],
        "spec": [("Brand", "Nitto"), ("Category", "Nylon fishing nets"), ("Technology", "Japanese"), ("Supplied by", "J.P. Fernando & Sons")],
        "gallery": [("nitto-poster.jpg", "Nitto Japanese-technology fishing nets")],
    },
    "hdpe": {
        "parent": "ropes/",
        "slug": "ropes/hdpe/",
        "name": "HDPE Rope",
        "title_html": "HDPE <em>rope</em>",
        "kind": "Ropes · High-density polyethylene",
        "img": "ropes.jpg",
        "fit": "contain",
        "blurb": "Polyethylene rope in coils and many colours, including our SuperCatch label.",
        "tag": [("Material", "HDPE"), ("Label", "SuperCatch")],
        "body": [
            ("p.big", "HDPE (high-density polyethylene) rope is a light, practical rope used widely across fishing and marine work."),
            ("p", "Our polyethylene ropes are supplied in coils in a range of sizes and colours — including blue, green, red, yellow and white — many under our own SuperCatch label."),
        ],
        "spec": [("Material", "High-density polyethylene (HDPE)"), ("Supplied as", "Coils"), ("Colours", "Blue, green, red, yellow, white"), ("Sizes", "Range of diameters — please ask")],
        "gallery": [("ropes.jpg", "SuperCatch PE rope coils"), ("rope-green.jpg", "Green and black rope coils"), ("rope-mixed.jpg", "Assorted rope coils")],
    },
    "pp": {
        "parent": "ropes/",
        "slug": "ropes/pp/",
        "name": "PP Rope",
        "title_html": "PP <em>rope</em>",
        "kind": "Ropes · Polypropylene",
        "img": "rope-twisted.jpg",
        "fit": "cover",
        "blurb": "Polypropylene rope — light, and a familiar workhorse on fishing boats.",
        "tag": [("Material", "Polypropylene"), ("Supplied as", "Coils & hanks")],
        "body": [
            ("p.big", "PP (polypropylene) rope is a light synthetic rope and a familiar sight on fishing boats."),
            ("p", "We supply PP rope in a range of sizes. Tell us the diameter, length and colour you need and we will confirm availability and price."),
        ],
        "spec": [("Material", "Polypropylene (PP)"), ("Supplied as", "Coils and hanks"), ("Sizes", "Range of diameters — please ask")],
        "gallery": [("rope-twisted.jpg", "Twisted rope coils"), ("rope-orange.jpg", "Rope hanks"), ("rope-mixed.jpg", "Assorted rope coils")],
    },
    "vinylon": {
        "parent": "ropes/",
        "slug": "ropes/vinylon/",
        "name": "Vinylon Rope",
        "title_html": "Vinylon <em>rope</em>",
        "kind": "Ropes · Vinylon fibre",
        "img": "rope-white.jpg",
        "fit": "cover",
        "blurb": "Vinylon rope for fishing work, available in a range of sizes.",
        "tag": [("Material", "Vinylon"), ("Sizes", "Range — please ask")],
        "body": [
            ("p.big", "Vinylon is a synthetic fibre with a long history in fishing ropes."),
            ("p", "Vinylon rope is part of our rope range alongside HDPE and PP. Contact us with the diameter and length you need to check current stock."),
        ],
        "spec": [("Material", "Vinylon"), ("Sizes", "Range of diameters — please ask")],
        "gallery": [("rope-white.jpg", "White rope coils"), ("rope-hanks.jpg", "Rope hanks")],
    },
    "toray": {
        "parent": "nylon-yarn-twine/",
        "slug": "nylon-yarn-twine/toray/",
        "name": "TORAY Yarn",
        "title_html": "TORAY <em>yarn</em>",
        "kind": "Nylon yarn · Japan",
        "img": "toray-yarn.jpg",
        "fit": "cover",
        "blurb": "TORAY Japan nylon yarn — supplied in Sri Lanka exclusively by J.P. Fernando & Sons.",
        "tag": [("Origin", "Japan"), ("Agent", "Sole agent in Sri Lanka")],
        "body": [
            ("p.big", "J.P. Fernando &amp; Sons is the sole agent and single distributor of TORAY products in Sri Lanka."),
            ("p", "Toray first produced nylon on a large scale in Japan in 1951 and holds the largest share of Japan's nylon market. Our &ldquo;Quality First&rdquo; principle led us to use TORAY Japan yarn in all of our own fishing-net brands."),
        ],
        "spec": [("Brand", "TORAY"), ("Origin", "Japan"), ("Distribution in Sri Lanka", "J.P. Fernando & Sons (sole agent)"), ("Used in", "All our own net brands, including SuperCatch")],
        "gallery": [("toray-yarn.jpg", "TORAY nylon yarn bobbins"), ("brand-toray.jpg", "TORAY wordmark")],
    },
}

BRANDS = [
    {"name": "TORAY", "img": "brand-toray.jpg", "where": "Japan", "note": "Sole agent and single distributor of TORAY products in Sri Lanka. TORAY yarn goes into all of our own net brands.", "link": "nylon-yarn-twine/toray/"},
    {"name": "SuperCatch", "img": "supercatch-logo.jpg", "where": "Our brand", "note": "Our own brand of nylon fishing nets and ropes — one of the most popular quality brands in Sri Lanka.", "link": "nylon-fishing-nets/super-catch/"},
    {"name": "J.P. Fernando & Sons", "img": "brand-jpfs.jpg", "where": "Our brand", "note": "Our house brand of fishing nets, made in Sri Lanka from TORAY Japan yarn.", "link": "nylon-fishing-nets/"},
    {"name": "Nitto", "img": "nitto-poster.jpg", "where": "Japanese technology", "note": "Japanese-technology fishing nets, engineered for big catch and long use.", "link": "nylon-fishing-nets/nitto/"},
    {"name": "Miracle Brand", "img": "brand-miracle.jpg", "where": "Japan", "note": "One of the world-renowned brands the company has represented as importer and distributor.", "link": None},
    {"name": "Eagle King · Youvella", "img": "brand-eagleking.jpg", "where": "In our range", "note": "Brands featured in the J.P. Fernando & Sons range.", "link": None},
]

HISTORIC_AGENCIES = ["Nichimen Corporation, Japan", "Miracle Brand, Japan", "Namayang Corporation, Korea"]
