from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Sum
from datetime import datetime
from .models import Expense, Budget, Category
from .forms import UserRegistrationForm, ExpenseForm, BudgetForm
from .ml_engine import analyze_user_finances
from .utils import generate_csv_report

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST.get('password'))
            user.save()
            for c in ['Food', 'Travel', 'Shopping', 'Education', 'Bills', 'Other']:
                Category.objects.get_or_create(name=c)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'finance_app/register.html', {'form': form})

@login_required
def dashboard_view(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0.00
    m_sum = expenses.filter(date__month=datetime.now().month).aggregate(Sum('amount'))['amount__sum'] or 0.00
    cat_summary = expenses.values('category__name').annotate(total=Sum('amount'))
    return render(request, 'finance_app/dashboard.html', {
        'total': total, 'monthly': m_sum,
        'labels': [i['category__name'] or 'Other' for i in cat_summary],
        'data': [float(i['total']) for i in cat_summary],
        'recent': expenses[:5]
    })

@login_required
def expense_list_view(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'finance_app/expense_list.html', {'expenses': expenses})

@login_required
def expense_add_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            e = form.save(commit=False)
            e.user = request.user
            e.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'finance_app/expense_form.html', {'form': form})

@login_required
def ai_insights_view(request):
    analysis = analyze_user_finances(request.user)
    return render(request, 'finance_app/ai_insights.html', {'analysis': analysis})

@login_required
def reports_view(request):
    expenses = Expense.objects.filter(user=request.user)
    if request.GET.get('export') == 'csv':
        return generate_csv_report(expenses)
    return render(request, 'finance_app/reports.html')
