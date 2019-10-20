from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('students/<int:student_id>', views.student, name = 'match-student'),
    path('students', views.students, name='match-students'),
    path('companies', views.companies, name='match-companies'),
    path('job_descriptions', views.jobs, name='job-descriptions'),
    path('match_for_interviews', views.match_interviews, name='match-match'),
    path('student_rank', views.student_rank, name='add-student-rank'),
    path('students/add/<int:student_id>', views.student_rank_individual, name='add-student-rank-individual')
]
