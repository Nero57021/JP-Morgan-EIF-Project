from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm, forms
from .models import *
from match.fetch import get_match_info
from match.matching.matching import match
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def index(request):
    return HttpResponse("Hello, match")

def companies(request):
    companies = Company.objects.order_by('company_name')
    context = {'companies': companies}
    return render(request, 'match/companies.html', context)

class StudentRankForm(ModelForm):
    class Meta:
        model = StudentJob
        fields = ('job', 'rank', 'student')

def student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    student_ranks = StudentJob.objects.filter(student=student.id).order_by('rank')
    job_rank_names = []
    for student_rank in student_ranks:
        job_rank_names.append(student_rank.job.name)
    print(job_rank_names)
    return render(request, 'match/student.html', {'student': student, 'job_rank_names': job_rank_names})

def student_rank(request):
    form = StudentRankForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data.get("job"))
        print(form.cleaned_data.get("rank"))
        print(form.cleaned_data.get("student"))
        form.save()
        messages.success(request, f'Rank added!')
        return HttpResponseRedirect(reverse("match-student", args=(student_id,)))
    return render(request, 'match/student_rank.html', {"form": form})

def student_rank_individual(request, student_id):
    form = StudentRankForm(request.POST or None, initial={'student': student_id})
    if form.is_valid():
        print(form.cleaned_data.get("job"))
        print(form.cleaned_data.get("rank"))
        print(form.cleaned_data.get("student"))
        form.save()
        messages.success(request, f'Rank added!')
        return HttpResponseRedirect(reverse("match-student", args=(student_id,)))
    return render(request, 'match/student_rank.html', {"form": form})

    # return render(request, 'match/student_rank.html')
    # student = get_object_or_404(Student, pk=student_id)
    # form = StudentRankForm(request.POST or None, initial={'student': student_id})
    # if form.is_valid():
    #      = form.cleaned_data.get("name")
    #     form.save()
    #     messages.success(request, f'Club name changed to {new_name}!')
    #     return redirect("club_list")
    # return render(request, template_name, {"form": form, "club": club})

def students(request):
    students = Student.objects.order_by('last_name')
    context = {'students': students}
    return render(request, 'match/students.html', context)

def jobs(request):
    jobs = Job.objects.order_by('name')
    companies = Company.objects.order_by('company_name')
    context = {'jobs': jobs, 'companies': companies}
    return render(request, 'match/job-descriptions.html', context)


def match_interviews(request):
    # Get the data
    # Loop through the students
    # This is the dictionary students rank
    students_dict = {}
    students = Student.objects.order_by('id')
    for student in students:
        # Get their job rankings
        students_dict[student.id] = []
        student_ranks = StudentJob.objects.filter(student=student.id).order_by('rank')
        for rank in student_ranks:
            students_dict[student.id].append(rank.job.id)
    # This is the dictionary jobs rank
    jobs_dict = {}
    jobs = Job.objects.order_by('id')
    for job in jobs:
        jobs_dict[job.id] = []
        job_ranks = CompanyStudent.objects.filter(job=job.id).order_by('rank')
        for rank in job_ranks:
            jobs_dict[job.id].append(rank.student.id)
    # jobs, students = get_match_info()
    # 2 is max number of students that can be interviewed for a position
    match_results_dict = match(jobs_dict, students_dict, 2)
    print(match_results_dict)

    # Construct a new dict with objects instead of keys
    match_results_converted = {}
    for job, student_array in match_results_dict.items():
        job_object = get_object_or_404(Job, pk=job)
        match_results_converted[job_object] = []
        for student in student_array:
            student_object = get_object_or_404(Student, pk=student)
            match_results_converted[job_object].append(student_object)
    print(match_results_converted)

    for job in match_results_converted:
        print(match_results_converted[job])

    context = {'jobs': match_results_converted.items()}

    return render(request, 'match/match_results.html', context)
