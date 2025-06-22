import os
import random
import xml.etree.ElementTree as ET
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt

# Config
kanjidic2_path = "kanjidic2.xml"
font_path = "Noto_Serif_JP/NotoSerifJP-VariableFont_wght.ttf"
image_size = 128
font_size = int(image_size * 0.8)
font = ImageFont.truetype(font_path, font_size)

# Parse KANJIDIC2
root = ET.parse(kanjidic2_path).getroot()

# Extract kanji and meanings
kanji_meanings = []
for character in root.findall("character"):
    literal = character.findtext("literal")
    freq_elem = character.find("misc/freq")
    freq = (
        int(freq_elem.text)
        if freq_elem is not None and freq_elem.text is not None
        else None
    )
    meanings = []
    for reading_meaning in character.findall("reading_meaning"):
        for rmgroup in reading_meaning.findall("rmgroup"):
            for m in rmgroup.findall("meaning"):
                if m.get("m_lang") is None:
                    meanings.append(m.text)
    if literal and meanings and freq is not None:
        kanji_meanings.append((literal, meanings[0], freq))

# Pick 8 random kanji with freq
samples = random.sample(kanji_meanings, 8)

fig, axes = plt.subplots(2, 4, figsize=(6, 4))
axes = axes.flatten()
for ax, (kanji, meaning, freq) in zip(axes, samples):
    img = Image.new("L", (image_size, image_size), color=255)
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), kanji, font=font)
    x = (image_size - (bbox[2] - bbox[0])) / 2 - bbox[0]
    y = (image_size - (bbox[3] - bbox[1])) / 2 - bbox[1]
    draw.text((x, y), kanji, fill=0, font=font)
    ax.imshow(img, cmap="gray")
    ax.set_title(f"kanji meaning {meaning}", fontsize=7, pad=16)
    ax.axis("off")
plt.tight_layout(rect=[0, 0.03, 1, 0.95], pad=3.0)
plt.savefig("sample.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved sample.png")
