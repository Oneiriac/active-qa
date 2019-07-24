import os
from typing import Optional

from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

from app.reformulator import FlaskReformulator

ENV_SERVER_PORT = 10000


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dfsajodskl;dfkjl;dsa'


class QuestionForm(FlaskForm):
    question = StringField('Reformulate Question')
    submit = SubmitField('Reformulate!')


class SelectMethodForm(FlaskForm):
    choices = [('active-qa', 'ActiveQA'), ('synonyms', 'Synonyms')]
    select = SelectField(label='Select Engine', choices=choices)


app = Flask(__name__)
app.config.from_object(Config)

reformulator_instance: Optional[FlaskReformulator] = None


def start_reformulator():
    global reformulator_instance
    reformulator_instance = FlaskReformulator(environment_server_address='localhost:{}'.format(ENV_SERVER_PORT))


@app.route('/', methods=['GET', 'POST'])
def submit_phrase():
    form = QuestionForm()

    if form.validate_on_submit():
        reformulations = [r for r in reformulator_instance.reformulate([form.question.data.strip()])]
    else:
        reformulations = []

    return render_template('form.html', title='Reformulate Question', form=form, reformulations=reformulations)


if __name__ == "__main__":
    start_reformulator()
    app.run(debug=True)
