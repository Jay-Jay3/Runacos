from marshmallow import Schema, fields, validates_schema, ValidationError, validate
from werkzeug.datastructures import FileStorage
from datetime import datetime, timezone
from flask_smorest.fields import Upload


class PostSchema(Schema):
    title = fields.Str(required=True)
    createdAt = fields.DateTime(load_default=lambda: datetime.now(timezone.utc))
    content = fields.Str(required=True)
    authorName = fields.Str(required=True)
    authorId = fields.Str(required=True)
    fileUrl = fields.Str(required=False)

class postPostSchema(Schema):
    title = fields.Str(required=True)
    createdAt = fields.DateTime(load_default=lambda: datetime.now(timezone.utc))
    content = fields.Str(required=True)
    authorName = fields.Str(required=True)
    authorId = fields.Str(required=True)
    fileUrl = fields.Raw(required=False)


class ImagesSchema(Schema):
    file = fields.Raw(
        required=True, 
        metadata={
            "type":"string",
            "format":"binary",
            "description":"Select a file for upload"
            })
    @validates_schema
    def validate(self, data, **kwargs):
        file = data.get("file")
        if not isinstance(file, FileStorage):
            raise ValidationError("not a valid file.")
        if not file.filename.lower().endswith(('png', 'jpeg', 'jpg', 'gif')):
            raise ValidationError("Only PNG/JPG/JPEG allowed")

class EventSchema(Schema):
    title = fields.Str(required=True)
    eventType = fields.Str(required=True)
    studentId = fields.Str(required=True)
    status = fields.Str(required=True)
    response = fields.Str(required=True)
    eventTime = fields.DateTime(required=True)
    description = fields.Str(required=True, validate=lambda x: len(x) < 1000)
    fileUrl = fields.Str(required=False)

class postEventSchema(Schema):
    title = fields.Str(required=True)
    eventType = fields.Str(required=True)
    studentId = fields.Str(required=True)
    status = fields.Str(required=True)
    response = fields.Str(required=True)
    eventTime = fields.DateTime(required=True)
    description = fields.Str(required=True, validate=lambda x: len(x) < 1000)

class FaqsSchema(Schema):
    title = fields.Str(required=True)
    sentAt = fields.DateTime(load_default=lambda: datetime.now(timezone.utc))
    content = fields.Str(required=True)

class FaultreportingSchema(Schema):
    title = fields.Str(required=True)
    studentId = fields.Str(required=True)
    status = fields.Str(load_default="in-progress")
    response = fields.Str(required=True)
    description = fields.Str(required=True)

class JobsSchema(Schema):
    title = fields.Str(required=True)
    jobType = fields.Str(required=True)
    postedByName = fields.Str(required=True)
    postedById = fields.Str(required=True)
    description = fields.Str(required=True)
    deadLine = fields.DateTime(required=True)
    company = fields.Str(required=True)

class MentorshipSchema(Schema):
    studentId = fields.Str(required=True)
    status = fields.Str(load_default="in-progress")
    message = fields.Str(required=True)
    alumniId = fields.Str(required=True)



class ResourcesSchema(Schema):
    uploadedBy = fields.Str(required=True)
    resourceType = fields.Str(required=True)
    title = fields.Str(required=True)
    courseCode = fields.Str(required=True)
    fileUrl = fields.Str(required=True)

class ImagesResourcesSchema(Schema):
    file = fields.Raw(
        required=True, 
        metadata={
            "type":"string",
            "format":"binary",
            "description":"Select a file for upload"
            })
    @validates_schema
    def validate(self, data, **kwargs):
        file = data.get("file")
        if not isinstance(file, FileStorage):
            raise ValidationError("not a valid file.")
        if not file.filename.lower().endswith(('png', 'jpeg', 'jpg', 'gif', 'ppt', 'pptx', 'doc', 'docx', 'md', 'pages', 'zip', 'txt', 'docx', 'pdf')):
            raise ValidationError("Only Academic Files are allowed")
        


class AlumniInfoSchema(Schema):
    currentCompany = fields.Str(load_default="")
    graduationYear = fields.DateTime(load_default=lambda: datetime.year(timezone.utc))
    isStar = fields.Bool(load_default=False)
    jobTitle = fields.Str(load_default="")


class StudentInfoSchema(Schema):
    department = fields.Str(required=True)
    matricNumber = fields.Str(required=True)

class userSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Regexp(
            '[A-Z][a-z]{1,20} [A-Z][a-z]{1,20}',
            error="Invalid User Name.\n Use the Format: 'John Doe'"
        )
        )
    createdAt = fields.DateTime(load_default=lambda: datetime.now(timezone.utc))
    role = fields.Str(
        load_default="student"
        )
    email = fields.Str(
        required=True, 
        validate=validate.Regexp(
            '[a-zA-Z]{3,20}1[0-9]{4}@run.edu.ng',
            error="Invalid School Email."
        )
        )
    password = fields.Str(required=False)

    studentInfo = fields.Nested(StudentInfoSchema)
    alumniInfo = fields.Nested(AlumniInfoSchema, allow_none=True)

class loginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    
class SubscribersEmail(Schema):
    email = fields.Str(required=True, 
        validate=validate.Regexp(
            '[a-z]{3,20}1[0-9]{4}@run.edu.ng',
            error="Invalid School Email."
        ))



