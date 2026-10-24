# EduAakashaa UCEED Mock Test Centre — portal package

A members-only mock-test page for UCEED Part A:

- 9 official papers (2018–2026, 613 questions) with the official answers
- 5 original EduAakashaa practice papers (2026 format, 285 questions)

It includes:

- a timed mock mode and a practice mode
- each year's own marking scheme, including partial marks for MSQ
- a question palette in the style of the real exam
- confidence rating (Guess / Low / Medium / High) on every answer
- a report showing scores by section, by topic and by confidence level, with "sure but wrong" risk flags
- step-by-step explanations for every question

## What is in this folder

| Path | What it is |
|---|---|
| `index.html` | The whole application: one file with its HTML, CSS and JavaScript. |
| `data/2018.json` … `data/2026.json` | The official papers. Question images are embedded as WebP (1.5–3.3 MB each). |
| `data/M1.json` … `data/M5.json` | The five original practice papers (about 0.2 MB each). |
| `tools/` | The build scripts used to make the data (see "Updating the content"). They are not needed on the server. |

## Putting it on the portal

1. **Upload the folder.** Upload `index.html` and the `data/` folder together, keeping `data/` next to `index.html`. For example: `https://www.eduaakashaa.com/members/uceed-mock/`. Do not upload `tools/`.
2. **Serve it over https from a web server.** The page loads each paper with `fetch()`, which does not work if `index.html` is opened from disk (`file://`).
3. **Keep it members-only.** Put the folder behind the portal's login, using the same rule you use for other member pages. The page has no login of its own.
4. **Set the content types.** Make sure the server sends `.json` as `application/json`; most servers do this by default. Turning on gzip or brotli compression for `.json` cuts download size by about 25%.
5. **Optional: embed it in a page.** You can put it inside an existing member page with an iframe:
   ```html
   <iframe src="/members/uceed-mock/index.html" style="width:100%;height:100vh;border:0" title="UCEED mock tests"></iframe>
   ```
   If you do, add `allow="clipboard-write"` only if you need it. Nothing else is required.

## Connecting it to member accounts (optional)

Define `window.EA_CONFIG` before the main script. The simplest way is to edit the small `<script>` line near the top of `index.html`. The cleaner way is to have the portal render that line server-side for the logged-in member.

```html
<script>
window.EA_CONFIG = {
  memberName: "Aisha Rahman",        // fills the name on the score card
  memberId: "EA1024",                // keeps each member's progress separate on shared devices
  resultsEndpoint: "/api/mock-results", // POST each finished attempt here (leave "" to disable)
  dataPath: "data/"                  // change if the JSON files live elsewhere (e.g. a CDN path)
};
</script>
```

**Without any settings**, everything works. The member types their name, and progress and best scores are kept in that browser's local storage only.

**With `resultsEndpoint`**, every submitted test is sent as JSON with `POST` and `credentials: "include"`, so the portal session cookie goes with it. The score card then shows "saved to your member account", or a gentle note if saving failed. If saving fails, the result stays on the device. Example payload:

```json
{
  "memberId": "EA1024", "name": "Aisha Rahman",
  "paper": "2026", "paperTitle": "UCEED 2026", "mode": "mock",
  "score": 142.58, "max": 200,
  "sections": [{"type":"NAT","score":48,"max":56,"right":12,"partial":0,"wrong":1,"blank":1}],
  "startedAt": "2026-10-24T10:00:00.000Z", "finishedAt": "2026-10-24T11:58:12.000Z", "autoSubmitted": false,
  "questions": { "1": {"type":"NAT","topic":"OBS","answer":"6","official":"6","status":"right","marks":4,"confidence":"H"} }
}
```

- `status` is one of `right`, `part`, `wrong`, `blank` or `bonus`.
- `confidence` is one of `G`, `L`, `M`, `H` or `null`.
- Topic codes are: `OBS` observation, `NUM` numbers & logic, `SPA` 3D & spatial, `PAT` patterns, `SCI` everyday science, `VIS` visual design, `CUL` art & culture.

With this data the portal can build a mentor dashboard, for example to list members with many "sure but wrong" answers.

## Updating the content

### Data format (one file per paper)

```json
{ "year": "2026", "mins": 120,
  "sections": [{"type":"NAT","lo":1,"hi":14,"right":4,"wrong":0,"partial":false}, ...],
  "qs": [{
    "n": 1, "t": "NAT|MSQ|MCQ", "cat": "OBS",
    "img": "data:image/webp;base64,...", "w": 900, "h": 400,    // official papers: question as printed
    "stem": "...", "fig": "<svg>…</svg>", "opts": ["…","…","…","…"], "layout": "list|grid",  // original papers
    "disp": "A, C",                       // answer shown to students
    "acc": {"ranges": [[0.17, 0.19]]} | {"sets": ["AC", "C"]} | {"bonus": true},  // what is accepted
    "steps": ["…"], "svg": "<svg>…</svg>", "trap": "common mistake", "note": ""
  }]
}
```

Scoring follows `sections`:

- A wrong answer scores `wrong`.
- Partial MSQ scores one mark per correct option ticked when no wrong option is ticked.
- `bonus` gives full marks to everyone.

To add a new paper, add its JSON file and add one line to the `YEARS` list (official) or the `MOCKS` list (original) in `index.html`.

### Adding a new official year

1. Crop each question from the official PDF:
   ```
   python3 tools/qcrop.py 2027 UCEED_2027_paper.pdf 57
   ```
   This writes `qimg/2027/qNN.jpg`.
2. Write the explanations. The EduAakashaa solved-paper guide workflow already produces them.
3. Convert to JSON with `tools/extract_official.py`, after editing its year table.
4. Check every answer against IIT Bombay's final answer key before publishing.

### Making more original practice papers

```
python3 tools/generator/build.py 2028        # any seed gives a fresh, reproducible set of 5 papers
```

This writes `M1.json` … `M5.json` into `data/`. Set `EA_DATA_DIR` to write somewhere else.

- The topic blueprint per section is in `make_papers()`. It is based on the 2024–26 papers.
- Generated questions compute their own answers.
- Knowledge questions come from the banks in `sci.py`, `vis.py` and `cul.py`. Each bank item is used only once per set.
- Review a new set before publishing. The shipped set has already been reviewed.

## Notes

- Question images in the official papers are reproduced from IIT Bombay's UCEED papers. The explanations are EduAakashaa's own. The practice papers are original and are not IIT Bombay papers.
- The page uses Google Fonts (Fraunces, Plus Jakarta Sans, JetBrains Mono). If the fonts are blocked, it falls back to system fonts.
- Contact: EduAakashaa, Coimbatore · +91 80157 22706 · info@eduaakashaa.com · www.eduaakashaa.com
