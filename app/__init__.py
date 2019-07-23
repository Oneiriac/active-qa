import os
from typing import Optional

from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from app.reformulator import FlaskReformulator

ENV_SERVER_PORT = 10000


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dfsajodskl;dfkjl;dsa'


class QuestionForm(FlaskForm):
    question = StringField('Question')
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config.from_object(Config)

reformulator_instance: Optional[FlaskReformulator] = None
@app.before_first_request
def start_services():
    global reformulator_instance
    reformulator_instance = FlaskReformulator(environment_server_address='localhost:{}'.format(ENV_SERVER_PORT))


@app.route('/', methods=['GET', 'POST'])
def submit_phrase():
    if not reformulator_instance:
        start_services()

    form = QuestionForm()
    if form.validate_on_submit():
        for r in reformulator_instance.reformulate([form.question.data.strip()]):
            flash(r)
    return render_template('form.html', title='Reformulate Question', form=form)


if __name__ == "__main__":
    app.run(debug=True)
