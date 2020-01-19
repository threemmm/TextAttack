from flask import Flask
from flask import render_template, request

import textattack
import textattack.run_attack as run_attack
from textattack.tokenized_text import TokenizedText

import json
import numpy as np
import pickle

label_map = {0: "negative", 1: "positive"}

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

        model_class = run_attack.MODEL_CLASS_NAMES[data['model']]
        model = eval(f'{model_class}()')

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
            attack = eval(f'{attack_class}({model}, {transformation})')
            attack.add_constraints(constraints)

        else:
            recipe_class = run_attack.RECIPE_NAMES[data['recipe']]
            attack = eval(f'{recipe_class}(model)')
        
        tokenized_input = TokenizedText(data['input_string'], model.tokenizer)

        pred = attack._call_model([tokenized_input])
        label = int(pred.argmax())

        print("Attacking...")
        attack.attack([label, data['input_string']])

        
        ret_val = {

        }

        return json.dumps(ret_val)

    return app

# Needed for AWS EB
application = create_app()

# run the app.
if __name__ == "__main__":
    application.run(debug=True, port=9000)

