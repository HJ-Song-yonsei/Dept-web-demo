# Static Export (Frozen-Flask)

## Install
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements_static.txt
```

## Build
```bash
python freeze_site.py
```
Artifacts will be in `build/`.

## Deploy
- **GitHub Pages/Netlify/S3**: point the host to the `build/` directory contents.
- Ensure your host serves `index.html` for directory paths (most do by default).
- If relative links break, set `app.config['FREEZER_RELATIVE_URLS'] = True` (already set in the script).

## Notes
- Dynamic routes: `myboard.board_view` is generated for IDs found in `data/posts.json`.
- API route `/api/board` is frozen as a file under `api/board/`. If you need `.json` extension, add an alias route like `/api/board.json` in Flask before freezing.