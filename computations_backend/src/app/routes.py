from os import path

from flask import request, jsonify
from app import app, speech_to_text_service, plots_generator, classification_service
import jsonpickle

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@app.route('/process_audio', methods=['GET'])
def process_audio():
    file_path = request.args.get('file_path')

    if not path.exists(file_path):
        return app.response_class(
            response=jsonpickle.encode({'reason': f"File {file_path} doesnt exists"}, make_refs=False,
                                       unpicklable=False),
            status=500,
            mimetype='application/json'
        )

    text_statistics = speech_to_text_service.process(file_path)
    plot_image = str(plots_generator.generate_plot(text_statistics, 30 * 1000))
    plot_image = plot_image[2:-1]

    response_body = {'results': text_statistics,
                     'plot': plot_image}

    response = app.response_class(
        response=jsonpickle.encode(response_body, make_refs=False, unpicklable=False),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/process_image', methods=['GET'])
def process_image():
    file_path = request.args.get('file_path')

    if not path.exists(file_path):
        return app.response_class(
            response=jsonpickle.encode({'reason': f"File {file_path} doesnt exists"}, make_refs=False,
                                       unpicklable=False),
            status=500,
            mimetype='application/json'
        )

    label_statistics = classification_service.process_image_file(file_path)
    response_body = {'results': label_statistics,
                     'plot': str(plots_generator.generate_plot(label_statistics, 30 * 1000))}

    response = app.response_class(
        response=jsonpickle.encode({'labels': response_body}, make_refs=False, unpicklable=False),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/process_video', methods=['GET'])
def process_video():
    file_path = request.args.get('file_path')

    if not path.exists(file_path):
        return app.response_class(
            response=jsonpickle.encode({'reason': f"File {file_path} doesnt exists"}, make_refs=False,
                                       unpicklable=False),
            status=500,
            mimetype='application/json'
        )

    label_statistics = classification_service.process_video_file(file_path)
    plot_image = str(plots_generator.generate_plot(label_statistics, 30 * 1000))
    plot_image = plot_image[2:-1]

    response_body = {'results': label_statistics,
                     'plot': plot_image}

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
