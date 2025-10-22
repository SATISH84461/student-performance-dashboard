from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from collections import defaultdict
from . import serializers, models, forms
# Create your views here.

# test post drf view
class TeacherList(APIView):
    def post(self, request):
        # Handle POST request
        file_path = request.FILES.get('file_path')
        file_extension = file_path.name.split('.')[-1]
        if file_extension == 'xlsx':
            dataframe = pd.read_excel(file_path)
        elif file_extension == 'csv':
            dataframe = pd.read_csv(file_path)
        else:
            return Response({"status": "error","status_code": 400 , "message": "Unsupported file type"}, status=400)
        if dataframe.columns.size < 2:
            return Response({"status": "error","status_code": 400 , "message": "Insufficient columns in the file"}, status=400)
        if 'Name' not in dataframe.columns:
            return Response({"status": "error","status_code": 400 , "message": "Missing 'Name' column"}, status=400)
        response = []
        for _, row in dataframe.iterrows():
            testdata = {
                "name": row['Name'],
                "subjects": []
            }
            for col in dataframe.columns[1:]:
                testdata['subjects'].append({
                    "subject_name": col,
                    "marks": row[col]
                })
            response.append(testdata)
        return Response({"status": "success","status_code": 200 , "data": response})

class Performance(APIView):
    def post(self, request):
        serializer_data = serializers.ResultFileUploadSerializer(data=request.data)
        if not serializer_data.is_valid():
            return Response({"status": "error","status_code": 400 , "message": "Data insertion failed!", "errors": serializer_data.errors}, status=400)
        serializer_data.save()  # inserts multiple rows
        print("Data inserted successfully!")
        return Response({"status": "success","status_code": 200 , "message": "Data inserted successfully!"})

# test post drf view
class TeacherList2(APIView):
    def post(self, request):
        # Handle POST request
        file_path = request.FILES.get('file')
        file_extension = file_path.name.split('.')[-1]
        if file_extension == 'xlsx':
            dataframe = pd.read_excel(file_path)
        elif file_extension == 'csv':
            dataframe = pd.read_csv(file_path)
        else:
            return Response({"status": "error","status_code": 400 , "message": "Unsupported file type"}, status=400)
        if dataframe.columns.size < 2:
            return Response({"status": "error","status_code": 400 , "message": "Insufficient columns in the file"}, status=400)
        if 'Name' not in dataframe.columns and 'Marks' not in dataframe.columns:
            return Response({"status": "error","status_code": 400 , "message": "Missing 'Name' or 'Marks' column"}, status=400)
        dataframe.columns = dataframe.columns.str.lower().str.replace(' ', '_')
        return Response({"status": "success","status_code": 200 , "message": "Data processed successfully","data": dataframe.head().to_dict(orient='records')})

class Performance2(APIView):
    def post(self, request):
        print("Received data:", request.data)
        serializer_data = serializers.ResultFileUploadSerializer2(data=request.data)
        if not serializer_data.is_valid():
            return Response({"status": "error","status_code": 400 , "message": "Data insertion failed!", "errors": serializer_data.errors}, status=400)
        serializer_data.save()  # inserts multiple rows
        print("Data inserted successfully!")
        return Response({"status": "success","status_code": 200 , "message": "Data inserted successfully!"})
    
class StudentSubjectListAPIView(APIView):
    def get(self, request):
        class_name = request.query_params.get('class_name')
        section = request.query_params.get('section')
        student_name = request.query_params.get('student_name')
        exam_name = request.query_params.get('exam_name')
        subject_name = request.query_params.get('subject_name', None)

        # Validate inputs
        if not all([class_name, section, exam_name, student_name]):
            return Response(
                {"error": "class_name, section, exam_name, and student_name are required parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        filters = {
            "class_name": class_name,
            "section": section,
            "exam_name": exam_name,
            "student_name": student_name
        }
        if subject_name:
            filters["subject_name"] = subject_name

        # Filter records
        results = models.ResultFileUpload.objects.filter(**filters).order_by('student_name', 'subject_name')
        
        if not results.exists():
            return Response(
                {"status": "Not Found","status_code": 404,"message": "No subjects found for the given student."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = serializers.StudentSubjectMarksSerializer(results, many=True)
        return Response({
            "status": "success",
            "status_code": 200,
            "message": "Data fetched Successfully",
            "data": {
                "student_name": student_name,
                "class_name": class_name,
                "section": section,
                'exam_name': exam_name,
                "subjects": serializer.data
            }
        }, status=status.HTTP_200_OK)
    
class TeacherClassResultsAPIView(APIView):
    def get(self, request):
        class_name = request.query_params.get('class_name')
        section = request.query_params.get('section')
        exam_name = request.query_params.get('exam_name')
        teacher_name = request.query_params.get('teacher_name')
        subject_name = request.query_params.get('subject_name', None) 

        # Validate inputs
        if not all([class_name, section, exam_name, teacher_name]):
            return Response(
                {"error": "class_name, section, exam_name, and teacher_name are required parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )
        filters = {
            "class_name": class_name,
            "section": section,
            "exam_name": exam_name,
            "teacher_name": teacher_name
        }
        if subject_name:
            filters["subject_name"] = subject_name

        # Filter records
        records = models.ResultFileUpload.objects.filter(**filters).order_by('student_name', 'subject_name')

        if not records.exists():
            return Response(
                {"message": "No records found for the given parameters."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Group by student
        grouped_data = defaultdict(list)
        for record in records:
            grouped_data[record.subject_name].append({
                "student_name": record.student_name,
                "obtained_marks": record.obtained_marks,
                "passing_marks": record.passing_marks,
                "total_marks": record.total_marks
            })

        # Format response
        grouped_response = [
            {"subject_name": subject, "student_data": students}
            for subject, students in grouped_data.items()
        ]

        serializer = serializers.TeacherResultSerializer(grouped_response, many=True)

        return Response({
                "status": "success",
                "status_code": 200,
                "message": "Data fetched Successfully",
                "data": {
                    "teacher_name": teacher_name,
                    "class_name": class_name,
                    "section": section,
                    "exam_name": exam_name,
                    "students": serializer.data
                }
            }, status=status.HTTP_200_OK)
    
def home(request):
    return render(request, 'home.html')

def student_result(request):
    return render(request, 'student_result.html')

def teacher_result(request):
    return render(request, 'teacher_result.html')

def upload_file_view(request):
    if request.method == 'POST':
        form = forms.ResultFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process file upload here
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": True, "message": "File uploaded successfully!"})
            else:
                return render(request, 'upload_results.html', {'form': form, 'success': True})
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "errors": form.errors})
    
    form = forms.ResultFileUploadForm()
    return render(request, 'upload_results.html', {'form': form})