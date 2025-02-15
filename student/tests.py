import io
import openpyxl
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Student, Grade


class UploadGradesTestCase(TestCase):
    def setUp(self):
        # You can create a student beforehand if needed
        self.student = Student.objects.create(name="John Doe", email="john@example.com")
        self.url = reverse(
            "grades:upload_grades"
        )  # Replace with the actual URL name if needed

    def create_excel_file(self):
        """Create an in-memory Excel file with student grade data."""
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(["Student Name", "Email", "Subject", "Grade"])  # headers

        # Add some test data
        sheet.append(["John Doe", "john@example.com", "Math", 90])
        sheet.append(["Jane Doe", "jane@example.com", "English", 85])

        # Save it in memory as a byte string
        excel_file = io.BytesIO()
        wb.save(excel_file)
        excel_file.seek(0)  # Go to the start of the file
        return excel_file

    def test_upload_grades_valid_file(self):
        excel_file = self.create_excel_file()

        # Simulate the POST request with the file
        response = self.client.post(
            self.url,
            {
                "excel_file": SimpleUploadedFile(
                    "grades.xlsx",
                    excel_file.read(),
                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
            follow=True,
        )

        # Check if the response is the success page
        self.assertTemplateUsed(response, "grades/uploaded_success.html")
        self.assertEqual(response.status_code, 200)

        # Check if the student data has been uploaded/updated correctly
        student = Student.objects.get(email="john@example.com")
        grade = Grade.objects.get(student=student, subject="Math")

        self.assertEqual(grade.grade, 90)

        # Check the second student's grade
        student_jane = Student.objects.get(email="jane@example.com")
        grade_jane = Grade.objects.get(student=student_jane, subject="English")

        self.assertEqual(grade_jane.grade, 85)

    def test_upload_grades_invalid_file(self):
        # Simulate uploading a request with no file (empty POST data)
        response = self.client.post(self.url, {}, follow=True)

        # Assert that the response contains the error message for missing file
        self.assertContains(
            response, "No file uploaded."
        )  # Match this to the exact error message in your template
