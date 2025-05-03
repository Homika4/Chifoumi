from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to DataBase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///points.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Point(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    point: Mapped[int] = mapped_column(Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    requested_score = db.session.execute(db.select(Point).where(Point.id == 1)).scalar()
    points = requested_score.point
    return render_template("index.html", result=result, points=points)

@app.route('/reset')
def reset():
    requested_score = db.session.execute(db.select(Point).where(Point.id == 1)).scalar()
    if requested_score:
        requested_score.point = 0
        db.session.commit()
    return render_template("index.html", points=0)

@app.route('/result.html')
def result():
    choices = ["Paper","Rock","Scissor"]
    random_choice = random.choice(choices)
    pick_id = request.args.get('pick_id')
    requested_score = db.session.execute(db.select(Point).where(Point.id == 1)).scalar()
    # Update points based on the game result
    if pick_id == random_choice:
        pass  # Draw, no change in points
    elif (pick_id == "Rock" and random_choice == "Scissor") or \
            (pick_id == "Paper" and random_choice == "Rock") or \
            (pick_id == "Scissor" and random_choice == "Paper"):
        requested_score.point += 1  # Win -> Increase points
    else:
        requested_score.point -= 1  # Loss -> Decrease points
    db.session.commit()
    print(requested_score.point)
    return render_template("result.html", pick_id=pick_id, result=result, random_choice=random_choice)

if __name__ == "__main__":
    app.run()
