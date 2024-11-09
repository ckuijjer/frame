from bottle import Bottle, static_file, run, response, request
from render_news_to_display import render_news_to_display
from render_image_on_display import render_image_on_display
from render_overscan import render_overscan

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
    data = request.json
    provider = data.get('provider', 'getimg')  # Default to 'getimg' if not specified
    try:
        render_news_to_display(provider=provider)  # Pass provider to render function
        response.content_type = 'application/json'
        return {"status": "success", "message": "Image rendered and displayed."}
    except Exception as e:
        response.status = 500
        return {"status": "error", "message": str(e)}


@app.route('/api/upload', method='POST')
def api_upload():
    upload = request.files.get('file')
    if not upload:
        response.status = 400
        return {"status": "error", "message": "No file uploaded."}
    
    try:
        file_path = f"./images/{upload.filename}"
        upload.save(file_path, overwrite=True)  # Save the file and overwrite if it exists

        # Display the uploaded image on the Inky display
        render_image_on_display(file_path)
        return {"status": "success", "message": "Image uploaded and displayed on Inky."}
    except Exception as e:
        response.status = 500
        return {"status": "error", "message": str(e)}

@app.route('/api/render_overscan', method='POST')
def api_render_overscan():
    data = request.json
    top = data.get('top')
    right = data.get('right')
    bottom = data.get('bottom')
    left = data.get('left')
    try:
        render_overscan(top, right, bottom, left)
        response.content_type = 'application/json'
        return {"status": "success", "message": "Overscan rendered and displayed."}
    except Exception as e:
        response.status = 500
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080)
