from rest_framework import serializers
from .models import ResultFileUpload

class ResultFileUploadSerializer(serializers.ModelSerializer):
    data = serializers.ListField(write_only=True)  # extra nested field

    class Meta:
        model = ResultFileUpload
        fields = [
            'teacher_name', 'class_name', 'section',
            'total_marks', 'passing_marks', 'data'
        ]

    def create(self, validated_data):
        # Extract nested data
        students_data = validated_data.pop('data', [])
        teacher_name = validated_data.get('teacher_name')
        class_name = validated_data.get('class_name')
        section = validated_data.get('section')
        total_marks = validated_data.get('total_marks')
        passing_marks = validated_data.get('passing_marks')

        instances = []
        for student in students_data:
            student_name = student.get('name')
            for subject in student.get('subjects', []):
                instance = ResultFileUpload.objects.create(
                    teacher_name=teacher_name,
                    class_name=class_name,
                    section=section,
                    student_name=student_name,
                    subject_name=subject.get('subject_name'),
                    obtained_marks=subject.get('marks'),
                    passing_marks=passing_marks,
                    total_marks=total_marks
                )
                instances.append(instance)
        return instances

class ResultFileUploadSerializer2(serializers.ModelSerializer):
    data = serializers.ListField(write_only=True)  # extra nested field

    class Meta:
        model = ResultFileUpload
        fields = [
            'teacher_name', 'class_name', 'section', 'exam_name', 'subject_name',
            'total_marks', 'passing_marks', 'data'
        ]

    def create(self, validated_data):
        students_data = validated_data.pop('data', [])
        teacher_name = validated_data.get('teacher_name')
        class_name = validated_data.get('class_name')
        section = validated_data.get('section')
        total_marks = validated_data.get('total_marks')
        passing_marks = validated_data.get('passing_marks')
        subject_name = validated_data.get('subject_name')
        exam_name = validated_data.get('exam_name')

        instances = []

        for student in students_data:
            student_name = student.get('name')
            student_marks = student.get('marks')

            # Update or create based on composite key
            instance, created = ResultFileUpload.objects.update_or_create(
                teacher_name=teacher_name,
                class_name=class_name,
                section=section,
                subject_name=subject_name,
                student_name=student_name,
                exam_name=exam_name,
                defaults={
                    'total_marks': total_marks,
                    'passing_marks': passing_marks,
                    'obtained_marks': student_marks
                }
            )
            instances.append(instance)

        return instances
    

class StudentSubjectMarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultFileUpload
        fields = [
            'subject_name',
            'teacher_name',
            'obtained_marks',
            'total_marks',
            'passing_marks'
        ]

class TeacherSubjectMarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultFileUpload
        fields = ['student_name', 'obtained_marks', 'passing_marks', 'total_marks']


class TeacherResultSerializer(serializers.Serializer):
    subject_name = serializers.CharField()
    student_data = TeacherSubjectMarksSerializer(many=True)
