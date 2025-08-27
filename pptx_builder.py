from pptx import Presentation


for idx, s in enumerate(slides):
title = s.get("title", "")
bullets = s.get("bullets", []) or []
notes = s.get("notes", None)
layout_hint = s.get("layout", "auto")


# Decide layout
need_body = len(bullets) > 0
layout = _find_best_layout(prs, need_title=True, need_body=need_body)
slide = prs.slides.add_slide(layout)


# Title
try:
if slide.shapes.title:
slide.shapes.title.text = title
except Exception:
pass


# Body placeholder (bullets)
try:
body = None
for shape in slide.placeholders:
if shape.placeholder_format.type == 1: # TITLE
continue
if shape.has_text_frame:
body = shape
break
if body is not None and len(bullets) > 0:
add_bullets(body.text_frame, bullets)
except Exception:
pass


# Reuse a decorative image from template on content slides
try:
if image_cycle:
blob = image_cycle[idx % len(image_cycle)]
# Place near bottom-right with a modest size
left = slide.slide_width - Inches(3)
top = slide.slide_height - Inches(2)
slide.shapes.add_picture(io.BytesIO(blob), left, top, width=Inches(2.5))
except Exception:
pass


# Speaker notes
if notes:
try:
slide.notes_slide.notes_text_frame.text = notes
except Exception:
# Some layouts may not have a notes slide yet
try:
_ = slide.notes_slide
slide.notes_slide.notes_text_frame.text = notes
except Exception:
pass


return prs
