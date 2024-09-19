from marshmallow import Schema, fields
from core.models.teachers import Teacher

class TeacherSchema(Schema):
    class Meta:
        fields = ('id', 'user_id', 'created_at', 'updated_at')
