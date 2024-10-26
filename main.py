from bottle import Bottle, static_file, run, response
from render_news_to_display import render_news_to_display

app = Bottle()

WEB_DIST_DIR = './web/dist' # Path to the directory containing the built web app'

# Route to serve the main HTML file
@app.route('/')
def serve_html():
    return static_file('index.html', root=WEB_DIST_DIR)

# Route to serve other static files (CSS, JS, images, etc.)
@app.route('/<filename:path>')
def serve_static(filename):
    return static_file(filename, root=WEB_DIST_DIR)

# API endpoint to trigger rendering of news to display
@app.route('/api/render', method='POST')
def api_render():
    try:
        render_news_to_display()  # Call the function to render and display the news
        response.content_type = 'application/json'
        return {"status": "success", "message": "Image rendered and displayed."}
    except Exception as e:
        response.status = 500
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    run(app, host='localhost', port=8080)
