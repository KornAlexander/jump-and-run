# 🎮 Jump & Run — Fabric for Kids

A vibe-coded jump & run game that runs inside a Microsoft Fabric notebook.

## The Story

My kids and I built this game over the weekend. It started as a **Python/Pygame** script, but I wanted to embed it into Microsoft Fabric — so I switched to **HTML5 Canvas**. Embedding was one line:

```python
displayHTML(open("./builtin/jump_and_run.html").read())
```

Upload the HTML to Lakehouse → `displayHTML()` → game runs inside the notebook.

Since we were already in Fabric, I took it further: the game tracks stats (score, deaths, coins, jumps, duration) as JSON after each round. A second notebook cell saves them to a **Delta table** — turning a kids' game into a full analytics pipeline.

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys / WASD | Move |
| Space / Up / W | Jump |
| F | Attack (Lightning / Sonic Wave) |
| Stomp | Land on enemies from above |

## Files

| File | Description |
|------|-------------|
| `jump_and_run python game basis.py` | Original Python/Pygame version |
| `jump_and_run.html` | HTML5 Canvas version (embeddable in Fabric) |
| `jump_and_run_v2.html` | V2 with audio, particles & smooth camera |
| `Jump and Run.ipynb` | Fabric notebook — play, save stats, view summary |

## Stats Pipeline

The notebook has 3 cells:
1. **Play** — renders the HTML game via `displayHTML()`
2. **Save** — paste the game-over JSON, click Save → appends to `game_stats` Delta table
3. **Summary** — shows all games, win rate, high score, total playtime, and more
