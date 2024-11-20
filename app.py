from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, IntegerField, SelectField, validators

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Data storage for simplicity (use a database for real-world apps)
schedule = {day: [] for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']}


# Form for adding farmers
class FarmerForm(Form):
    name = StringField('Farmer Name', [validators.DataRequired()])
    unique_number = IntegerField('Unique Number', [validators.DataRequired()])
    region = SelectField('Region', choices=[
        ('Region A', 'Region A'),
        ('Region B', 'Region B'),
        ('Region C', 'Region C'),
        ('Region D', 'Region D'),
    ], validators=[validators.DataRequired()])
    day = SelectField('Day', choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ], validators=[validators.DataRequired()])


@app.route('/')
def home():
    return render_template('home.html', schedule=schedule)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = FarmerForm(request.form)
    if request.method == 'POST' and form.validate():
        day = form.day.data
        if len(schedule[day]) < 7:  # Limit 7 farmers per day
            farmer = {
                'name': form.name.data,
                'unique_number': form.unique_number.data,
                'region': form.region.data
            }
            schedule[day].append(farmer)
            return redirect(url_for('home'))
        else:
            return f"Cannot add more farmers to {day}. Limit reached.", 400
    return render_template('add.html', form=form)


@app.route('/clear')
def clear():
    for day in schedule:
        schedule[day] = []
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
