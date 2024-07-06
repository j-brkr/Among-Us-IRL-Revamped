from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class settingsForm(FlaskForm):
    imposter_count = IntegerField("# of Imposters", [DataRequired(), Length(min = 1, max = 10)], default = 3)
    reveal_role = BooleanField("Reveal roles on death?")
    emergency_meetings = IntegerField("# of Emergency Meetings", [DataRequired(), Length(min = 0, max = 10)], default = 3)
    discussion_time = SelectField("Discussion Time", [DataRequired()], choices=[(60,"1m"),(120,"2m"),(180,"3m"),(240,"4m"),(300,"5m"),(360,"6m"),(480,"8m"),(600,"10m"),(900,"15m"),(1200,"20m"),(86400,"all day")], default = 300)
    emergency_cooldown = SelectField("Emergency Cooldown", [DataRequired()], choices=[(0,"0s"),(5,"5s"),(10,"10s"),(15,"15s"),(30,"30s"),(45,"45s"),(60,"60s"),(300,"5m")], default = 30)
    kill_cooldown = SelectField("Kill Cooldown", [DataRequired()], choices=[(0,"0s"),(5,"5s"),(10,"10s"),(15,"15s"),(30,"30s"),(45,"45s"),(60,"60s"),(300,"5m")], default = 30)
    short_tasks = IntegerField("Short Tasks", [DataRequired(), Length(min = 0, max = 10)], default = 2)
    long_tasks = IntegerField("Long Tasks", [DataRequired(), Length(min = 0, max = 10)], default = 2)
    common_tasks = IntegerField("Common Tasks", [DataRequired(), Length(min = 0, max = 3)], default = 1)
    submit = SubmitField("Start Game")