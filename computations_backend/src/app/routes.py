from os import path

from flask import request, jsonify
from app import app, speech_to_text_service, plots_generator
import jsonpickle

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@app.route('/process_audio', methods=['GET'])
def process_audio():
    file_path = request.args.get('file_path')

    if not path.exists(file_path):
        return app.response_class(
            response=jsonpickle.encode({'reason': f"File {file_path} doesnt exists"}, make_refs=False, unpicklable=False),
            status=500,
            mimetype='application/json'
        )

    text_statistics = speech_to_text_service.process(file_path)

    response_body = {'results': text_statistics,
                     'plot': plots_generator.generate_plot(text_statistics, 30 * 1000)}

    response = app.response_class(
        response=jsonpickle.encode(response_body, make_refs=False, unpicklable=False),
        status=200,
        mimetype='application/json'
    )

    return response


def handle_exception(message, status_code):
    response = jsonify({'message': message})
    response.status_code = status_code
    return response
