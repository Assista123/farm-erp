import os

template_dir = r'core\templates\core'

for filename in os.listdir(template_dir):
    if filename.endswith('_list.html'):
        filepath = os.path.join(template_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'table-responsive' not in content:
            content = content.replace(
                '<div class="card-body p-0">\n        <table',
                '<div class="card-body p-0">\n        <div class="table-responsive">\n        <table'
            )
            content = content.replace(
                '        </table>\n    </div>\n</div>',
                '        </table>\n        </div>\n    </div>\n</div>'
            )
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Updated: {filename}')
        else:
            print(f'Skipped: {filename}')