from flask import Flask
from flask import render_template, request
import textattack
import textattack.run_attack as run_attack

import json
import numpy as np
import pickle

def create_app():

    # This line required for AWS Elastic Beanstalk
    # Specify the template and static folders so that AWS EB can find them!
    # On your dashboard, make sure to set the static to something like: PATH = /static/  DIRECTORY = webapp/static
    # (only then will the CSS work)
    app = Flask(__name__, template_folder='webapp/templates', static_folder='webapp/static')

    @app.route('/')
    @app.route('/index')
    def index():
      return render_template('index.html', title='TextAttack Viz')

    # Example of how to add backend model to frontend template.
    @app.route('/about')
    def about():
      return render_template('about.html',
          title='About TextAttack',
          model_name="dwb",)
      
    # Actually run the model
    @app.route('/run_textattack', methods=['POST'])
    def run_textattack():

        print('Generating adverserial sample...')

        data = request.form

        input_string = request.form['input_string']
        model = request.form['model']
        attack = request.form['attack']
        recipe = request.form['recipe']
        transformation = request.form['transformation']
        constraint_type = request.form['constraint_type']
        constraint_input = request.form['constraint_input']

        model_class = run_attack.MODEL_CLASS_NAMES[data['model']]
        #model = eval(f'{model_class}()')
        print(model_class)

        if data['recipe'] == "none":
            # Build attack from given model, attack, transformation, and constraints

            transformation_class = run_attack.TRANSFORMATION_CLASS_NAMES[data['transformation']]
            transformation = eval(f'{transformation_class}()')

            constraints = []
            if data['constraint_type'] != "none":

                constraint_class = run_attack.CONSTRAINT_CLASS_NAMES[data['constraint_type']]
                constraint = eval(f'{constraint_class}({data["constraint_input"]})')
                constraints.append(constraint)


            attack_class = run_attack.ATTACK_CLASS_NAMES[request.form['attack']]
            attack = eval(f'{attack_class}(model, transformations, ')
            print(attack_class)

        else:
            # Build attack from recipe

            pass

        ret_val = {

        }

        return json.dumps(ret_val)

    return app

# Needed for AWS EB
application = create_app()

# run the app.
if __name__ == "__main__":
    application.run(debug=True, port=9000)

