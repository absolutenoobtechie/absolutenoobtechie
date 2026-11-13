# Deploying your desktop (beginner guide)

## 1. Create the profile repository
Go to github.com/new. Name it **exactly** `absolutenoobtechie` (same as your username), set it **Public**, and tick "Add a README" only if you plan to upload via the website (you'll replace it). A repo named like your username is what makes GitHub show its README on your profile.

## 2. Put the files there
Everything in this folder goes in the **root** of that repo, keeping the folders:
```
README.md   DEPLOY.md   .gitignore
assets/     data/       desk/       scripts/
.github/workflows/update-desktop.yml
```
**Easiest (no terminal):** on the repo page click *Add file → Upload files*, drag the contents of this folder in (hidden `.github` folder: on Windows/Mac enable "show hidden files", or use the terminal route), then *Commit changes*.

**Terminal route:**
```bash
cd absolutenoobtechie
git init -b main
git add .
git commit -m "retro desktop profile"
git remote add origin https://github.com/absolutenoobtechie/absolutenoobtechie.git
git push -u origin main
```

## 3. Enable GitHub Actions
Repo → *Settings → Actions → General* → "Allow all actions" and under *Workflow permissions* choose **Read and write permissions** → Save. Then *Actions → update desktop → Run workflow* once. This fetches your real contribution data into the activity window. It then refreshes daily by itself.

## 4. Check your profile
Open github.com/absolutenoobtechie. Hard-refresh (Ctrl/Cmd+Shift+R) if images look stale; GitHub caches images for a few minutes. Test the mobile view by narrowing your browser window.

## 5. Updating later
- **Text in windows** (intro info, learning stages, terminal, recycle bin lessons): edit `data/desktop.json` on GitHub (pencil icon) and commit. The Action rebuilds the SVGs automatically. Learning stage is a number: 0 not started, 1 started, 2 practicing, 3 building with it, 4 comfortable.
- **Project folders:** open a repo → click the gear next to *About* → add the topic `built`, `in-progress`, `experiments` or `archived`. The folder links filter your repos by those topics. No README edit needed.
- **Journal / Reading / Ideas:** edit the files in `desk/`.
- **Locally:** `python3 scripts/build_assets.py` rebuilds the SVGs.

## What's clickable vs decorative
| Element | Type |
|---|---|
| About Me, Journal, Reading, Ideas That Didn't Work icons | Link → pages in `desk/` |
| Experiments icon + Experiments folder | Link → your repos filtered by topic `experiments` |
| Built / In Progress / Archived folders | Link → your repos filtered by that topic |
| Recycle bin | Link → `desk/ideas-that-didnt-work.md` |
| Menu bar, hello.txt, now learning, terminal, About This Computer, activity monitor, taskbar | Decorative only |
