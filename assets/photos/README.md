# Adding photos

1. Put the image files in this folder (`assets/photos/`). Keep them around 2000px on the long edge, JPG or WebP.
2. Add one entry per photo to `photos.json`, in the order you want them shown:

```json
[
  {
    "file": "lake-erie-sunset.jpg",
    "title": "Sunset over Lake Erie",
    "alt": "Orange sunset over calm water with a pier in silhouette",
    "category": "Landscape",
    "location": "Erie, PA"
  }
]
```

Only `file` is required. `alt` describes the photo for screen readers. `category` adds filter buttons once there are two or more categories. An optional `thumb` field points at a smaller version for the grid.
