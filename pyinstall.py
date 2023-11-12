import PyInstaller.__main__

PyInstaller.__main__.run([
    'ui_app.py',
    # '-i', 'icon.ico',
    '--onefile',
    # '--noconsole'
])
