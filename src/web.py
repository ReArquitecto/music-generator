import urllib

file_count = 0

def gen_musichtml(title:str, html_filename:str, score_filename:str, description:str=""):
    '''Given musicXml file, write HTML file to display it'''

    global file_count

    safe_score_filename = urllib.parse.quote(score_filename)
    
    with open("src/template.html", "r") as template_file:
        template = template_file.read()
    
    desc_html = f"<h2>{description}</h2>" if description else ""

    # Replace placeholders in the template
    html_content = template.replace("{{ title }}", title)\
                           .replace("{{ description }}", desc_html)\
                           .replace("{{ score_filename }}", safe_score_filename)

    # Write to the new HTML file
    with open(html_filename, "w") as f:
        f.write(html_content)
        file_count += 1

import urllib.parse
import webbrowser

def display_musicxml(title:str, html_filename:str, score_filename:str, description:str=""):
    gen_musichtml(title, html_filename, score_filename, description)
    webbrowser.open(f'http://localhost:8000/{urllib.parse.quote(html_filename)}')
