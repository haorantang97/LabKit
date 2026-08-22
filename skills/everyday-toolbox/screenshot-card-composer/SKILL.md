---
name: screenshot-card-composer
description: Turn raw or pre-cropped private-message and comment-section screenshots into 1080x1440 black 3:4 cards with a 4x4 positioning grid, semantic content cropping, questioner-identity removal, privacy masks, exact centering, and readable one-to-three-image layouts. Use when the user asks to整理、裁切、打码、居中、拼接或批量导出私信截图、抖音评论截图、问答截图或聊天记录卡片。
---

# Screenshot Card Composer

Create publishable screenshot cards while preserving the complete useful exchange and hiding the questioner's identity.

## Workflow

1. Enumerate the supplied images and inspect every source visually.
2. Classify each source as `private_message`, `comment`, or `other`.
3. Decide the valuable content boundary before composing:
   - Keep the complete question and the answer needed to understand it.
   - Remove status bars, navigation, keyboards, unrelated comments, and empty app chrome.
   - Keep timestamps or system messages only when they explain the conversation sequence.
4. Protect the questioner's identity:
   - Crop away the avatar, username, account ID, or profile header when doing so leaves the useful text complete.
   - If cropping would remove or truncate useful text, preserve the text and add a tight solid-black mask over identity information only.
   - Never treat the question text itself as identity information.
   - Do not hide the content author's own account label unless the user requests it.
   - Preserve coarse province/city and time metadata by default, matching the reference style. Hide a location only when it is precise enough to identify the person or the user requests stricter privacy.
5. Group sources:
   - Use one source per output by default.
   - Group two or three sources only when they belong to the same exchange or one source continues another.
   - Preserve reading order.
6. Write a JSON manifest using [references/manifest.md](references/manifest.md).
7. Run:

   ```bash
   python3 scripts/compose_cards.py manifest.json --output-dir /absolute/output/path
   ```

8. Inspect every generated card and revise the manifest until all checks pass.

## Composition Rules

- Output exactly `1080 x 1440`.
- Use a pure black background.
- Draw vertical grid lines at `x=270, 540, 810` and horizontal grid lines at `y=360, 720, 1080`.
- Render the center grid lines brighter than the others.
- Center the complete material group horizontally and vertically by its outer bounding box.
- For one source, use the central `540 px` content band between `x=270` and `x=810`. If its height would exceed `1152 px`, reduce it proportionally while keeping it centered.
- For multiple sources, select among:
  - `stack`: Use for short or wide screenshots that remain readable at up to `540 px` width.
  - `row`: Use for two tall screenshots when side-by-side placement gives greater readable width.
  - `grid`: Use for three or four screenshots when two columns improve the smallest readable width.
- Keep `18 px` gaps between sources.
- Prefer the layout with the largest minimum displayed source width. Prefer `stack` when its minimum width is at least `430 px` or within 92% of the best candidate.
- Never shift a composition up or down for visual taste; exact geometric centering is the default.

## Content Rules

### Private messages

- Keep the question bubble, the author's response, and only the sequence markers required to understand their order.
- Crop away conversation headers and message-composer controls.
- Mask the other person's avatar or account name when visible.
- Keep multiple reply bubbles together when separating them changes meaning.

### Comment sections

- Keep the question text and the directly relevant author reply chain.
- Remove unrelated neighboring comments.
- Crop username-only margins when possible.
- Mask a questioner's username/avatar when it shares a row with useful text.
- Preserve reply indentation or author badges when they clarify who answered whom.

## Quality Checks

- Confirm every output is `1080 x 1440`.
- Confirm a single source touches or fits inside the two central vertical lines.
- Confirm the material group's bounding-box center is `(540, 720)` within one pixel.
- Confirm all text is readable at full output size.
- Confirm no questioner avatar, username, account ID, or profile header remains visible.
- Confirm no useful question or answer text was removed by a privacy crop.
- Report any identity area that is ambiguous instead of guessing it is safe.
