from flask import Blueprint, render_template, request
from .controller import MainController


main_bp = Blueprint('main', __name__)
main_controller = MainController()
@main_bp.route('/', methods=['GET'])
def index():
    page = main_controller.index()
    return render_template("index.html", page=page)


@main_bp.route('/fuzzy', methods=['POST'])
def fuzzy_result():
    soil_moisture = float(request.form.get('soil_moisture', 0))
    temperature = float(request.form.get('temperature', 0))
    humidity = float(request.form.get('humidity', 0))
    rain_chance = float(request.form.get('rain_chance', 0))

    result = main_controller.irrigation_fuzzy(
        soil_moisture=soil_moisture,
        temperature=temperature,
        humidity=humidity,
        rain_chance=rain_chance,
    )
    return render_template('result.html', mode='fuzzy', result=result)


@main_bp.route('/expert', methods=['POST'])
def expert_result():
    symptoms = request.form.getlist('symptoms')
    result = main_controller.expert_diagnosis(symptoms)
    return render_template('result.html', mode='expert', result=result)
      