from django.shortcuts import render

# Create your views here.

from .models import Fréquentation

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_freqs = Fréquentation.objects.all().count()
    num_days = Fréquentation.objects.distinct().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)