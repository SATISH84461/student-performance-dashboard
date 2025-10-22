from django.db import models

# BATCH_CHOICES = (
#     ('2021-2022', '2021-2022'),
#     ('2022-2023', '2022-2023'),
#     ('2023-2024', '2023-2024'),
#     ('2024-2025', '2024-2025'),
#     ('2025-2026', '2025-2026'),
# )

CLASSES = (('Class ' + str(i), 'Class ' + str(i)) for i in range(1, 13))

# class Teacher(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField(unique=True)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"
    
# class Student(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField(unique=True)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

# class Subject(models.Model):
#     name = models.CharField(max_length=100)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=1)
#     batch = models.CharField(max_length=9, choices=BATCH_CHOICES, default=BATCH_CHOICES[0])

#     def __str__(self):
#         return self.name

# class ExamDetails(models.Model):
#     examname = models.CharField(max_length=100)
#     examdate = models.DateField()
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     total_marks = models.IntegerField()
#     passing_marks = models.IntegerField()

#     def __str__(self):
#         return self.examname
    
# class Result(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     examdetails = models.ForeignKey(ExamDetails, on_delete=models.CASCADE, default=1)
#     final_grade = models.CharField(max_length=2)

#     def save(self, *args, **kwargs):
#         # Ensure student exists
#         if isinstance(self.student, dict):
#             self.student, _ = Student.objects.get_or_create(
#                 first_name=self.student.get('first_name'),
#                 last_name=self.student.get('last_name'),
#                 email=self.student.get('email')
#             )
#         # Ensure examdetails exists
#         if isinstance(self.examdetails, dict):
#             subject_data = self.examdetails.get('subject')
#             if isinstance(subject_data, dict):
#                 subject, _ = Subject.objects.get_or_create(
#                     name=subject_data.get('name'),
#                     teacher_id=subject_data.get('teacher_id', 1),
#                     batch=subject_data.get('batch', '2021-2022')
#                 )
#             else:
#                 subject = Subject.objects.get(name=subject_data)
#             self.examdetails, _ = ExamDetails.objects.get_or_create(
#                 examname=self.examdetails.get('examname'),
#                 examdate=self.examdetails.get('examdate'),
#                 subject=subject,
#                 total_marks=self.examdetails.get('total_marks', 100),
#                 passing_marks=self.examdetails.get('passing_marks', 40)
#             )
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.student}: {self.final_grade}"

from django.db import models

class ResultFileUpload(models.Model):
    teacher_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    exam_name = models.CharField(max_length=100)
    student_name = models.CharField(max_length=100)
    subject_name = models.CharField(max_length=100)
    total_marks = models.IntegerField()
    passing_marks = models.IntegerField()
    obtained_marks = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['teacher_name', 'class_name', 'section', 'exam_name', 'subject_name', 'student_name'],
                name='unique_result_per_student_subject'
            )
        ]

    def __str__(self):
        return f"{self.student_name} - {self.subject_name} : {self.obtained_marks}"
    