# Static Site Generator

A static site generator built from scratch in Python, as part of the [boot.dev](https://boot.dev) course.

Converts Markdown content into a fully static HTML site using a template, with support for headings, paragraphs, bold/italic, links, images, code blocks, blockquotes, and ordered/unordered lists.

## Live Demo

Deployed on Vercel [here](https://static-site-generator-theta.vercel.app/).

## Usage

Make scripts executable (first time only):
```bash
chmod +x dev.sh main.sh
```

**Development** (builds and serves on port 8888):
```bash
./dev.sh
```

**Production build** (outputs to `./public`):
```bash
./main.sh
```

## Project Structure

- `src/` — generator source code
- `content/` — Markdown source files
- `static/` — static assets (CSS, images) copied as-is to output
- `template.html` — HTML template with `{{ Title }}` and `{{ Content }}` placeholders
- `public/` — generated output (not committed)
