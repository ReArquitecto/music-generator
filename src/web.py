def display_musicxml(title, html_filename, score_filename, description=""):
    '''Given musicXml file, write HTML file to display it'''

    if description is not None:
        desc = f'<h3>{description}</h3>'

    html = '''
        <!DOCTYPE html>
        <HEAD>
        <TITLE>%s</TITLE>
        </HEAD>
        <body bgcolor=#000000" style="color:white;">
        <center><h2>%s</h2>%s</center><br>
        <div id="osmdContainer" style="width:25%%; margin:0 auto;"> <!-- FIXME: works but not well -->
        <script src="https://cdn.jsdelivr.net/npm/opensheetmusicdisplay@1.4.1/build/opensheetmusicdisplay.min.js"></script>
        <script>
        var osmd = new opensheetmusicdisplay.OpenSheetMusicDisplay("osmdContainer");
        osmd.setOptions({
            backend: "svg",
            drawTitle: false, // default title is "Muxi21 Fragment" -- maybe later we put what we want
            darkMode: true, // TODO make it a parameter
            drawingParameters: "compacttight" // don't display composer etc., smaller margins
        });
        osmd
            .load("http://localhost:8000/%s")
            .then(
            function() {
                osmd.render();
            }
            );
        </script>
        </div>
        </body>

    '''
    html = html % (title, title, desc, score_filename)
    with open(html_filename, 'w') as f:
        f.write(html)

    # open it in the browser
    # NOTE: before running, open a webserver using `python -m http.server` in this directory
    import webbrowser
    webbrowser.open(f'http://localhost:8000/{html_filename}')