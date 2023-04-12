import os
import sys
import ast
from flask import request,jsonify,make_response

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "common",
    )
)
from app_constants import AppConstants
from string_table import AppMessages
from app_response import AppResponse
from app_blueprint import AppBP
from models import Session, Todomodel, SampleUser
from auth_middleware import token_required, tokenid_required


def serialize(row):
    return {
        "id": str(row.id),
        "Description": row.description,
        "Completed": row.completed,
    }


todo_app = AppBP("todoapi", __name__)


@todo_app.route("/", methods=["GET"])
@tokenid_required
def default_api(data):
    """Home Page
    ---
    tags:
     - name: Default Task Page
    security:
     - APIKeyHeader: ['x-access-token']
    responses:
        200:
            description: Testing Task Home Page

    """
    app_response=AppResponse()

    session = Session()
    todo_all = session.query(Todomodel).filter_by(createdby_id=data).all()
    if todo_all:
        app_response.set_response(AppConstants.CODE_OK, {"todo": [serialize(x) for x in todo_all]}, AppMessages.OPERATION_SUCCESS,AppConstants.SUCCESSFULL_STATUS_CODE)
        return make_response(jsonify(app_response), app_response["code"])
    else:
        app_response.set_response(
            AppConstants.CODE_INVALID_REQUEST,
            {"Failed": f"No Task for id {data}"},
            AppMessages.OPERATION_FAILED,
            AppConstants.CODE_INVALID_REQUEST,
        )
        return make_response(jsonify(app_response), app_response["code"])


# get all completed task
@todo_app.route("/completedtask", methods=["GET"])
@tokenid_required
def completedtask_api(data):
    """Completed Task Page
    ---
    tags:
        - name: Completed Task 
    security:
     - APIKeyHeader: ['x-access-token']
    responses:
        200:
            description: Get all completed task
        404:
            description: No Completed Task

    """
    app_response=AppResponse()
    session = Session()
    todo_all = (
        session.query(Todomodel).filter_by(completed=True, createdby_id=data).all()
    )
    if todo_all:
        app_response.set_response(AppConstants.CODE_OK, {"todo": [serialize(x) for x in todo_all]}, AppMessages.OPERATION_SUCCESS,AppConstants.SUCCESSFULL_STATUS_CODE)
        return make_response(jsonify(app_response), app_response["code"])
    else:                        
        app_response.set_response(
            AppConstants.CODE_INVALID_REQUEST,
            {"Failed": f"No Completed Task for id {data}"},
            AppMessages.OPERATION_FAILED,
            AppConstants.CODE_INVALID_REQUEST,
        )
        return make_response(jsonify(app_response), app_response["code"])


# Add a new Todo
@todo_app.route("/addtask", methods=["POST"])
@tokenid_required
def todoadd_request(data):
    """New Todo Creation
    ---
    tags:
     - name: Todo Create POST
    security:
     - APIKeyHeader: ['x-access-token']
    parameters:
      - name: Description
        in: formData
        type: string
        required: true
    responses:
        200:
            description: Todo is created Successfully
        404:
            description: Todo is not created successfully
    """
    app_response=AppResponse()
    description = request.form.get("Description")
    if description is None:
        app_response.set_response(
                    AppConstants.CODE_INVALID_REQUEST,
                    {"Failed": f"Description Should not be empty"},
                    AppMessages.OPERATION_FAILED,
                    AppConstants.CODE_INVALID_REQUEST,
                )
        return make_response(
                            jsonify(app_response), app_response["code"]
                        )
    session = Session()
    todo = (
        session.query(Todomodel)
        .filter_by(description=description, createdby_id=data)
        .first()
    )
    if todo:
        app_response.set_response(
            AppConstants.CODE_INVALID_REQUEST,
            {"Failed": f"Todo with similar description {description} is already available"},
            AppMessages.OPERATION_FAILED,
            AppConstants.CODE_INVALID_REQUEST,
        )
        return make_response(jsonify(app_response), app_response["code"])
    if len(description.strip()) < 5:
        app_response.set_response(
            AppConstants.CODE_INVALID_REQUEST,
            {"Failed": "description should have length greater than 5"},
            AppMessages.OPERATION_FAILED,
            AppConstants.CODE_INVALID_REQUEST,
        )
        return make_response(jsonify(app_response), app_response["code"])
    newtodo = Todomodel(
        description=description,
        completed=False,
        createdby_id=data,
    )
    try:
        session.add(newtodo)
        session.commit()
    finally:
        session.close()
    app_response.set_response(AppConstants.CODE_OK, {"Success": f"Todo is created with given description as {description} for user {data}"}, AppMessages.OPERATION_SUCCESS,AppConstants.SUCCESSFULL_STATUS_CODE)
    return make_response(jsonify(app_response), app_response["code"])


# delete a task
@todo_app.route("/deletetask/<id>", methods=["DELETE"])
@tokenid_required
def deletetask_api(data, id):
    """Delete a Task
    ---
    tags:
     - name: Delete Task
    parameters:
     - name: id
       in: path
       type: string
       required: true
    security:
     - APIKeyHeader: ['x-access-token']
    responses:
        200:
            description: Delete a task
        404:
            description: Delete a Todo is not created successfully

    """
    app_response=AppResponse()
    session = Session()
    todo_id = session.query(Todomodel).filter_by(id=id, createdby_id=data).first()
    if todo_id:
        try:
            session.delete(todo_id)
            session.commit()
            app_response.set_response(AppConstants.CODE_OK, {"Success": f"Todo with id {id} is deleted Successfully"}, AppMessages.OPERATION_SUCCESS,AppConstants.SUCCESSFULL_STATUS_CODE)
            return make_response(jsonify(app_response), app_response["code"])
        finally:
            session.close()

    else:
        app_response.set_response(
            AppConstants.CODE_INVALID_REQUEST,
            {"Failed": "Todo is not deleted as it is not available"},
            AppMessages.OPERATION_FAILED,
            AppConstants.CODE_INVALID_REQUEST,
        )
        return make_response(jsonify(app_response), app_response["code"])


# update a task
@todo_app.route("/updatetask/<id>", methods=["PUT"])
@tokenid_required
def updatetask_api(data, id):
    """Update a Task
    ---
    tags:
     - name: Update Task
    parameters:
     - name: id
       in: path
       type: string
       required: true
     - name: Description
       in: formData
       type: string
       required: false
     - name: Completed
       in: formData
       type: string
       required: false
    security:
     - APIKeyHeader: ['x-access-token']
    responses:
        200:
            description: Update a todo Successfully
        404:
            description: Update a Todo is not done successfully

    """
    app_response=AppResponse()
    description = request.form.get("Description")
    completed = request.form.get("Completed")
    session = Session()
    todo_id = session.query(Todomodel).filter_by(id=id, createdby_id=data).first()
    if todo_id:
        try:
            if description is not None:
                todo_id.description = description
            if completed is not None:
                todo_id.completed = ast.literal_eval(completed)
            session.commit()
            app_response.set_response(AppConstants.CODE_OK, {"Success": "Todo is Updated Successfully"}, AppMessages.OPERATION_SUCCESS,AppConstants.SUCCESSFULL_STATUS_CODE)
            return make_response(jsonify(app_response), app_response["code"])
        finally:
            session.close()
    else:
        app_response.set_response(
            AppConstants.CODE_INVALID_REQUEST,
            {"Failed": "Todo is not updated as it is not available"},
            AppMessages.OPERATION_FAILED,
            AppConstants.CODE_INVALID_REQUEST,
        )
        return make_response(jsonify(app_response), app_response["code"])
