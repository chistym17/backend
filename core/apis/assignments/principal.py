from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema,AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_assignments(p):
    """Returns all assignments"""
    assignments = Assignment.query.all()
    all_assignments = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=all_assignments)


@principal_assignments_resources.route('/assignments/regrade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def regrade_assignment(p, incoming_payload):
    """Regrade a graded assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment = Assignment.query.get(grade_assignment_payload.id)
    
    if assignment is None:
        return APIResponse.respond(message="Assignment not found", status=404)

    assignment.grade = grade_assignment_payload.grade
    
    db.session.commit()

    updated_assignment_dump = AssignmentSchema().dump(assignment)

    return APIResponse.respond(data=updated_assignment_dump)