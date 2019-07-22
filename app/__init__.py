import os

from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from app.reformulator import FlaskReformulator


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dfsajodskl;dfkjl;dsa'


class QuestionForm(FlaskForm):
    question = StringField('Question')
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config.from_object(Config)

reformulator_instance = FlaskReformulator()


@app.route('/', methods=['GET', 'POST'])
def submit_phrase():
    form = QuestionForm()
    if form.validate_on_submit():
        for r in reformulator_instance.reformulate([form.question.data.strip()]):
            flash(r)
    return render_template('form.html', title='Reformulate Question', form=form)


if __name__ == "__main__":
    app.run(debug=True)
