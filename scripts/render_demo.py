"""Render an explicitly illustrative walkthrough of demo.py's verified notes-server flow.

Optional tooling: Pillow and ffmpeg. This does not pretend to be a Claude screen recording.
"""

from __future__ import annotations

import pathlib
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "demo-illustrated.mp4"
FONT = pathlib.Path("/System/Library/Fonts/Supplemental/Arial.ttf")
BOLD = pathlib.Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")


def font(size, bold=False):
    path = BOLD if bold else FONT
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default()


def draw_slide(stage: int, output: pathlib.Path):
    image = Image.new("RGB", (1280, 720), "#0c1220")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((35, 30, 1245, 690), radius=24, fill="#151f31", outline="#35455c", width=2)
    draw.text((75, 65), "MCP  /  APPROVAL GATE", font=font(28, True), fill="#e6edf7")
    draw.text((75, 112), "SCRIPTED LOCAL DEMO  ·  FILE-WRITING MCP SERVER  ·  NOT A CLAUDE RECORDING",
              font=font(17), fill="#9aaec9")
    draw.line((75, 157, 1205, 157), fill="#35455c", width=2)
    allowed = stage < 2
    action = "notes_write"
    request_id = 1 if allowed else 2
    draw.text((85, 190), f"REQUEST  {request_id:02d}", font=font(19, True), fill="#65cced")
    draw.text((85, 235), "Server: private notes", font=font(25), fill="#e6edf7")
    draw.text((85, 279), f"Tool: {action}", font=font(32, True), fill="#e6edf7")
    draw.text((85, 331), f'Arguments: {{ "name": "{"approved" if allowed else "blocked"}" }}', font=font(23), fill="#adbed5")
    draw.rounded_rectangle((780, 206, 1170, 508), radius=18, fill="#202e43")
    draw.text((815, 237), "INTERCEPTION", font=font(22, True), fill="#9fb3cc")
    draw.text((815, 286), "Client  →  Gate", font=font(26), fill="#e6edf7")
    draw.text((815, 336), "Gate  →  Popup", font=font(26), fill="#e6edf7")
    if stage in (0, 2):
        draw.text((815, 390), "Server: waiting", font=font(25, True), fill="#f0bf68")
        draw.rounded_rectangle((85, 425, 270, 490), radius=10, fill="#3a4a62")
        draw.text((136, 444), "BLOCK", font=font(24, True), fill="#f4f6fb")
        draw.rounded_rectangle((293, 425, 478, 490), radius=10, fill="#2a9189")
        draw.text((348, 444), "ALLOW", font=font(24, True), fill="#ffffff")
        draw.text((85, 547), "Pending: this request has not reached the server.",
                  font=font(24), fill="#f0bf68")
    else:
        decision = "ALLOW" if allowed else "BLOCK"
        color = "#62dcb5" if allowed else "#ff8a91"
        draw.text((815, 390), f"Decision: {decision}", font=font(25, True), fill=color)
        draw.text((85, 432), "approved.txt saved; JSON-RPC result returned." if allowed else
                  "blocked.txt absent; denial -32001 returned.", font=font(23, True), fill=color)
        draw.text((85, 493), 'Result: { "text": "Note saved" }' if allowed else
                  'Error: code -32001 (request blocked)', font=font(23), fill="#e6edf7")
        draw.text((85, 557), "Verified by demo.py and tests/test_real_use.py", font=font(20), fill="#9fb3cc")
    draw.text((85, 642), "Configured MCP endpoints only · automatic timeout denial · no transparent interception",
              font=font(19), fill="#99abc1")
    image.save(output)


def main():
    with tempfile.TemporaryDirectory(prefix="mcp-video-") as directory:
        folder = pathlib.Path(directory)
        manifest = folder / "frames.txt"
        lines = []
        for stage in range(4):
            path = folder / f"phase-{stage}.png"
            draw_slide(stage, path)
            lines += [f"file '{path}'", "duration 3.5"]
        lines.append(f"file '{folder / 'phase-3.png'}'")
        manifest.write_text("\n".join(lines) + "\n")
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
                        "-i", str(manifest), "-vf", "fps=24,format=yuv420p", "-c:v", "libx264", "-movflags", "+faststart",
                        str(OUTPUT)], check=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
