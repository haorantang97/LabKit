# Manifest Format

Use absolute paths. Crop and mask coordinates are measured in the original source image after EXIF orientation is applied.

```json
{
  "show_grid": true,
  "outputs": [
    {
      "name": "01.jpg",
      "layout": "auto",
      "sources": [
        {
          "path": "/absolute/path/source-01.jpg",
          "crop": [120, 340, 840, 1160],
          "masks": [
            [138, 382, 210, 54]
          ],
          "kind": "comment"
        }
      ]
    },
    {
      "name": "02.jpg",
      "layout": "row",
      "sources": [
        {
          "path": "/absolute/path/part-a.png",
          "crop": [70, 210, 900, 1280],
          "masks": []
        },
        {
          "path": "/absolute/path/part-b.png",
          "crop": [80, 190, 890, 1290],
          "masks": [
            [780, 240, 72, 72]
          ]
        }
      ]
    }
  ]
}
```

Fields:

- `show_grid`: Optional global boolean. Defaults to `true`.
- `outputs`: Required output-card array.
- `name`: Required output filename. `.jpg` is added when omitted.
- `layout`: Optional `auto`, `stack`, `row`, or `grid`. Defaults to `auto`.
- `sources`: Required ordered array with one or more source objects.
- `path`: Required absolute image path.
- `crop`: Optional `[x, y, width, height]`. Omit to retain the full source.
- `masks`: Optional array of `[x, y, width, height]` rectangles in original-source coordinates.
- `kind`: Optional descriptive value for review; it does not change rendering.

Use tight masks with 4-12 pixels of safety margin around identity information. Keep masks out of useful text.
