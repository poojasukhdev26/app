import os

folder = "templates"
target = "url_for('menu')"
replacement = "url_for('show_menu')"

for root, _, files in os.walk(folder):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            if target in content:
                new_content = content.replace(target, replacement)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ Replaced with: {path}")