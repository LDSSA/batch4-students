import os
import json
import pickle
import joblib
import pandas as pd
from flask import Flask, jsonify, request
from peewee import (
    SqliteDatabase, PostgresqlDatabase, Model, IntegerField,
    FloatField, TextField, IntegrityError
)
from playhouse.shortcuts import model_to_dict


########################################
# Begin database stuff

DB = SqliteDatabase('predictions.db')


class Prediction(Model):
    observation_id = IntegerField(unique=True)
    observation = TextField()
    proba = FloatField()
    true_class = IntegerField(null=True)

    class Meta:
        database = DB


DB.create_tables([Prediction], safe=True)

# End database stuff
########################################

########################################
# Unpickle the previously-trained model


with open(os.path.join('data', 'baseline_model_columns.json')) as fh:
    columns = json.load(fh)


with open(os.path.join('data', 'baseline_model_pipeline.pickle'), 'rb') as fh:
    pipeline = joblib.load(fh)


with open(os.path.join('data', 'baseline_model_dtypes.pickle'), 'rb') as fh:
    dtypes = pickle.load(fh)


# End model un-pickling
########################################

########################################
# Input validation functions


def check_request(request):
    """
        Validates that our request is well formatted
        
        Returns:
        - assertion value: True if request is ok, False otherwise
        - error message: empty if request is ok, False otherwise
    """
    
    if "id" not in request:
        error = "Field `id` missing from request: {}".format(request)
        return False, error
    
    if "observation" not in request:
        error = "Field `observation` missing from request: {}".format(request)
        return False, error
    
    return True, ""



def check_valid_column(observation):
    """
        Validates that our observation only has valid columns
        
        Returns:
        - assertion value: True if all provided columns are valid, False otherwise
        - error message: empty if all provided columns are valid, False otherwise
    """
    
    valid_columns = {
      "SubjectRaceCode",
      "SubjectSexCode",
      "SubjectEthnicityCode",
      "StatuteReason", 
      "InterventionReasonCode", 
      "ResidentIndicator", 
      "SearchAuthorizationCode",
      "SubjectAge",
      "hour",
      "day_of_week",
    }
    
    keys = set(observation.keys())
    
    if len(valid_columns - keys) > 0: 
        missing = valid_columns - keys
        error = "Missing columns: {}".format(missing)
        return False, error
    
    if len(keys - valid_columns) > 0: 
        extra = keys - valid_columns
        error = "Unrecognized columns provided: {}".format(extra)
        return False, error    

    return True, ""



def check_categorical_values(observation):
    """
        Validates that all categorical fields are in the observation and values are valid
        
        Returns:
        - assertion value: True if all provided categorical columns contain valid values, 
                           False otherwise
        - error message: empty if all provided columns are valid, False otherwise
    """
    
    valid_category_map = {
        "InterventionReasonCode": ["V", "E", "I"],
        "SubjectRaceCode": ["W", "B", "A", "I"],
        "SubjectSexCode": ["M", "F"],
        "SubjectEthnicityCode": ["H", "M", "N"],
        "SearchAuthorizationCode": ["O", "I", "C", "N"],
        "ResidentIndicator": [True, False],
        "StatuteReason": [
            'Stop Sign', 'Other', 'Speed Related', 'Cell Phone', 'Traffic Control Signal', 'Defective Lights', 
            'Moving Violation', 'Registration', 'Display of Plates', 'Equipment Violation', 'Window Tint', 
            'Suspended License', 'Seatbelt', 'Other/Error', 'STC Violation', 'Administrative Offense', 'Unlicensed Operation'], 
        "day_of_week": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    }
    
    for key, valid_categories in valid_category_map.items():
        if key in observation:
            value = observation[key]
            if value not in valid_categories:
                error = "Invalid value provided for {}: {}. Allowed values are: {}".format(
                    key, value, ",".join(["'{}'".format(v) for v in valid_categories]))
                return False, error
        else:
            error = "Categorical field {} missing"
            return False, error

    return True, ""


def check_hour(observation):
    """
        Validates that observation contains valid hour value 
        
        Returns:
        - assertion value: True if hour is valid, False otherwise
        - error message: empty if hour is valid, False otherwise
    """
    
    hour = observation.get("hour")
        
    if not hour:
        error = "Field `hour` missing"
        return False, error

    if not isinstance(hour, int):
        error = "Field `hour` is not an integer"
        return False, error
    
    if hour < 0 or hour > 24:
        error = "Field `hour` is not between 0 and 24"
        return False, error

    return True, ""


def check_age(observation):
    """
        Validates that observation contains valid hour value 
        
        Returns:
        - assertion value: True if hour is valid, False otherwise
        - error message: empty if hour is valid, False otherwise
    """
    
    age = observation.get("SubjectAge")
        
    if not age: 
        error = "Field `SubjectAge` missing"
        return False, error

    if not isinstance(age, int):
        error = "Field `SubjectAge` is not an integer"
        return False, error
    
    if age < 10 or age > 100:
        error = "Field `SubjectAge` is not between 10 and 100"
        return False, error

    return True, ""


# End input validation functions
########################################

########################################
# Begin webserver stuff

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    obs_dict = request.get_json()
  
    request_ok, error = check_request(obs_dict)
    if not request_ok:
        response = {'error': error}
        return jsonify(response)

    _id = obs_dict['id']
    observation = obs_dict['observation']

    columns_ok, error = check_valid_column(observation)
    if not columns_ok:
        response = {'error': error}
        return jsonify(response)

    categories_ok, error = check_categorical_values(observation)
    if not categories_ok:
        response = {'error': error}
        return jsonify(response)

    hour_ok, error = check_hour(observation)
    if not hour_ok:
        response = {'error': error}
        return jsonify(response)

    age_ok, error = check_age(observation)
    if not age_ok:
        response = {'error': error}
        return jsonify(response)

    obs = pd.DataFrame([observation], columns=columns).astype(dtypes)
    proba = pipeline.predict_proba(obs)[0, 1]
    prediction = pipeline.predict(obs)[0]
    response = {'prediction': bool(prediction), 'proba': proba}
    p = Prediction(
        observation_id=_id,
        proba=proba,
        observation=request.data,
    )
    try:
        p.save()
    except IntegrityError:
        error_msg = "ERROR: Observation ID: '{}' already exists".format(_id)
        response["error"] = error_msg
        print(error_msg)
        DB.rollback()
    return jsonify(response)

    
@app.route('/update', methods=['POST'])
def update():
    obs = request.get_json()
    try:
        p = Prediction.get(Prediction.observation_id == obs['id'])
        p.true_class = obs['true_class']
        p.save()
        return jsonify(model_to_dict(p))
    except Prediction.DoesNotExist:
        error_msg = 'Observation ID: "{}" does not exist'.format(obs['id'])
        return jsonify({'error': error_msg})


    
if __name__ == "__main__":
    app.run()
