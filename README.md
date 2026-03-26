# MD2PDF

**Free, unlimited markdown-to-PDF conversion. No sign-ups. No paywalls. No nonsense.**

A fast, privacy-first web app that turns your markdown into clean, professional PDFs — instantly.

[Live App](https://www.markdown2pdf.co.uk/) | Built by [Oliver Ayton](https://www.linkedin.com/in/oliverayton/)

---

## Why This Exists

I kept running into the same annoying problem: I'd write something in markdown (a proposal, a doc, session notes for my AI coaching clients) and need a quick PDF. Every time, I'd Google "markdown to PDF", land on some tool, and hit a paywall after one conversion. *Seriously?*

So one evening I sat down and thought: "How hard can this actually be?"

Turns out — not that hard. **The entire app was built in a single evening-to-morning session.** First commit at 11pm, shipped and deployed by noon the next day. 10 commits. ~13 hours wall-clock, maybe 4-5 hours of real coding. Claude did most of the heavy lifting (I run an AI coaching business, so I'd be a hypocrite if I didn't use it).

The result is a tool I actually use every day — and now you can too.

---

## Features

- **Live Preview** — see your formatted markdown update in real-time as you type
- **Instant PDF Download** — one click (or `Cmd+Enter`) and it's on your machine
- **Drag & Drop** — toss a `.md` or `.txt` file straight into the editor
- **Smart Title Detection** — auto-names your PDF from the first heading
- **Word & Section Stats** — live word count, line count, and section counter in the sidebar
- **Two PDF Styles** — clean minimal or Practical AI branded
- **Zero Data Storage** — your content hits the server only during conversion, then it's gone
- **No Account Required** — just open and go

---

## Tech Stack

| Layer | Tech |
|-------|------|
| **Frontend** | Vanilla HTML/CSS/JS + [marked.js](https://marked.js.org/) for live preview |
| **Backend** | Python + Flask |
| **MD → HTML** | Pandoc |
| **HTML → PDF** | WeasyPrint |
| **Deployment** | Docker on Railway |
| **Fonts** | Inter + Nunito (Google Fonts) |

No React. No Next.js. No webpack. No 400MB `node_modules`. Just files that do things.

---

## Run It Locally

**Prerequisites:** Python 3.10+, [Pandoc](https://pandoc.org/installing.html)

```bash
# Clone and run
git clone https://github.com/ayton-labs/markdown-to-pdf.git
cd markdown-to-pdf
./run.sh
```

The script creates a virtual environment, installs dependencies, and starts the server at `http://localhost:8787`.

**Or with Docker:**

```bash
docker build -t md2pdf .
docker run -p 8787:8787 md2pdf
```

---

## Project Structure

```
.
├── index.html            # The entire frontend (yes, one file)
├── style.css             # UI styling
├── server.py             # Flask backend + PDF conversion pipeline
├── proposal.css          # Clean PDF output style
├── proposal-branded.css  # Practical AI branded PDF style
├── requirements.txt      # Python deps (flask, weasyprint)
├── Dockerfile            # Production container
├── run.sh                # Local dev launcher
└── og-image.png          # Social preview image
```

---

## How It Works

```
Your Markdown → [Frontend: marked.js live preview]
                        ↓ (click download)
              [Flask server receives markdown]
                        ↓
              [Pandoc: markdown → HTML + CSS]
                        ↓
              [WeasyPrint: HTML → PDF]
                        ↓
              PDF downloads to your machine
```

The whole round-trip takes about a second.

---

## API

If you just want the PDF endpoint:

```bash
curl -X POST "http://localhost:8787/pdf?name=my-doc&style=proposal" \
  -H "Content-Type: text/plain" \
  -d "# Hello World\n\nThis is my document." \
  -o my-doc.pdf
```

---

## The Build Log

For the curious, here's the full commit history — this is the entire development timeline:

| Time | Commit |
|------|--------|
| 11:04 PM | Initial commit — full working app |
| 11:11 PM | Fix Docker package name |
| 11:25 PM | Railway deployment config |
| 9:26 AM | UI density tuning |
| 9:27 AM | Mobile gate (desktop-only message) |
| 9:30 AM | UI scale refinement |
| 10:05 AM | PDF title metadata |
| 10:37 AM | Fix duplicate title bug |
| 11:28 AM | Tighten PDF typography |
| 12:06 PM | Drag-and-drop file support |

One evening. One morning. One app. Ship it.

---

## Contributing

Found a bug? Want a feature? PRs welcome. The codebase is small enough to read in one sitting.

---

## License

MIT — do whatever you want with it.

---

<p align="center">
  Built with irritation at paywalls and a mass of caffeine.<br>
  <strong><a href="https://practicalai.coach">Practical AI</a></strong> — <a href="https://www.linkedin.com/in/oliverayton/">Oliver Ayton</a>
</p>
