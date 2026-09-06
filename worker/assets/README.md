# PDF fonts (Noto Sans SC)

ReportLab needs **TrueType** (`.ttf` / compatible `.ttc`), not CFF/PostScript `.otf`.

Place files here (preferred):

- `NotoSansSC-Regular.ttf`
- `NotoSansSC-Bold.ttf`

Fallback order in code: asset TTFs → macOS STHeiti/Songti → Linux `NotoSansCJK*.ttc`.

Do not commit huge variable fonts unless subsetted. Offline CI on macOS can use system fonts.
