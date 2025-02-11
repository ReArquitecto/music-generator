def display_musicxml(title, html_filename, score_filename, description=""):
    '''Given musicXml file, write HTML file to display it'''
    
    with open("src/template.html", "r") as template_file:
        template = template_file.read()
    
    desc_html = f"<h2>{description}</h2>" if description else ""

    # Replace placeholders in the template
    html_content = template.replace("{{ title }}", title)\
                           .replace("{{ description }}", desc_html)\
                           .replace("{{ score_filename }}", score_filename)

    # Write to the new HTML file
    with open(html_filename, "w") as f:
        f.write(html_content)

    # Open in the browser
    import webbrowser
    webbrowser.open(f'http://localhost:8000/{html_filename}')