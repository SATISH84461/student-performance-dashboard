from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import ResultFileUpload

@admin.register(ResultFileUpload)
class ResultFileUploadAdmin(ImportExportModelAdmin):
    pass

# @admin.register(Teacher)
# class TeacherAdmin(ImportExportModelAdmin):
#     pass

# @admin.register(Subject)
# class SubjectAdmin(ImportExportModelAdmin):
#     pass

# @admin.register(Student)
# class StudentAdmin(ImportExportModelAdmin):
#     pass

# class ResultResource(resources.ModelResource):
#     student_first_name = fields.Field(column_name='student_first_name', attribute='student', widget=ForeignKeyWidget(Student, 'first_name'))
#     student_last_name = fields.Field(column_name='student_last_name', attribute='student', widget=ForeignKeyWidget(Student, 'last_name'))
#     student_email = fields.Field(column_name='student_email', attribute='student', widget=ForeignKeyWidget(Student, 'email'))
#     exam_name = fields.Field(column_name='exam_name', attribute='examdetails', widget=ForeignKeyWidget(ExamDetails, 'examname'))
#     exam_date = fields.Field(column_name='exam_date', attribute='examdetails', widget=ForeignKeyWidget(ExamDetails, 'examdate'))
#     exam_total_marks = fields.Field(column_name='exam_total_marks', attribute='examdetails', widget=ForeignKeyWidget(ExamDetails, 'total_marks'))
#     exam_passing_marks = fields.Field(column_name='exam_passing_marks', attribute='examdetails', widget=ForeignKeyWidget(ExamDetails, 'passing_marks'))
#     subject_name = fields.Field(column_name='subject_name', attribute='examdetails__subject', widget=ForeignKeyWidget(Subject, 'name'))

#     class Meta:
#         model = Result
#         fields = ('id', 'student_first_name', 'student_last_name', 'student_email', 'exam_name', 'exam_date', 'exam_total_marks', 'exam_passing_marks', 'subject_name', 'final_grade')
#         export_order = ('student_first_name', 'student_last_name', 'exam_name', 'subject_name',  'final_grade', 'exam_total_marks', 'exam_passing_marks', 'exam_date', 'student_email')
    
# @admin.register(Result)
# class ResultAdmin(ImportExportModelAdmin):
#     resource_class = ResultResource

# @admin.register(ExamDetails)
# class ExamDetailsAdmin(ImportExportModelAdmin):
#     pass

