from django import forms

class ResultFileUploadForm(forms.Form):
    teacher_name = forms.CharField(label="Teacher Name", max_length=100)
    class_name = forms.CharField(label="Class Name", max_length=50)
    section = forms.CharField(label="Section", max_length=10)
    exam_name = forms.CharField(label="Exam Name", max_length=100)
    subject_name = forms.CharField(label="Subject", max_length=100)
    total_marks = forms.IntegerField(label="Total Marks")
    passing_marks = forms.IntegerField(label="Passing Marks")
    file = forms.FileField(label="Upload File (.xlsx or .csv)")
