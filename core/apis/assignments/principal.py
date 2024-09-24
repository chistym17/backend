from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse,StatusCodeResponse
from core.models.assignments import Assignment,AssignmentStateEnum,GradeEnum
from .schema import AssignmentSchema,AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_assignments(p):
    """Returns all assignments"""
    assignments = Assignment.query.all()
    all_assignments = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=all_assignments)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or regrade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment = Assignment.query.get(grade_assignment_payload.id)

    if assignment is None:
        return StatusCodeResponse.respond(404)

    if assignment.state == AssignmentStateEnum.DRAFT:
        return StatusCodeResponse.respond(400)

    assignment.grade = grade_assignment_payload.grade
    assignment.state = AssignmentStateEnum.GRADED

    db.session.commit()

    updated_assignment_dump = AssignmentSchema().dump(assignment)

    return APIResponse.respond(data=updated_assignment_dump)
