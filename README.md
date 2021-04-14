## Toggle hiding all windows upon idle

- Hide windows after idle for 10 minutes, intended for usage with wallpaper engine backgrounds, but will work with other screensavers.
- Any interaction (keyboard usage, mouse movement) will bring windows back.

### Python3 Script Usage:
```python
py toggle_desktop.py
```
OR

```python
python toggle_desktop.py
```


### TODO:

- [x] Set any interaction to bring windows back
- [x] Run on startup with windows hidden
- [ ] Hide desktop icons when minimizing
- [ ] Remember how desktop icons were set before minimizing (no point bringing them back if the user had them hidden before)
