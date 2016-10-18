from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from blog.models import *
import time
from calendar import month_name

from django.forms import ModelForm
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect

class FormularioComentario(ModelForm):
	class Meta:
		model = Comentario
		exclude = ["identificada"]

def poncomentario(request, pk):
	p = request.POST

	if 'mensaje' in p:
		autor = "Anonimous"
		if p["autor"]: autor = p["autor"]

		comentario = Comentario(identrada=Entrada.objects.get(pk=pk))
		cf = FormularioComentario(p, intance=comentario)
		cf.fields["autor"].required =  false

		comentario = sf.save(commit.false)
		comentario.autor = autor
		comentario.save()

	return HttpResponseRedirect(reverse("entrada",args=[pk]))

def mkmonth_lst():
	if not Entrada.objects.count(): return[]

	year, month = time.localtime()[:2]
	first = Entrada.objects.order_by("fecha")[0]
	fyear = first.fecha.year
	fmonth = first.fecha.month
	months = []

	for y in range(year, fyear-1, -1):
		start, end = 12, 0
		if y == year: start = month
		if y == fyear: end = fmonth - 1
		for m in range(start, end,-1):
			months.append((y,m,month_name[m]))
	return months

def month(request, year, month):
	identrada=Entrada.objects.filter(fecha__year=year, fecha__month=month)
	comentario = Comentario.objects.filter(identrada=identrada)
	d = dict(entrada=identrada, comentario=comentario, form=FormularioComentario())
	d.update(csrf(request))
	return render_to_response("entrada.html",d)

# Create your views here.
def entrada(request, pk):
	identrada = Entrada.objects.get(pk=int(pk))
	return render_to_response("entrada.html",dict(elemento=identrada))

def main(request):
	entrada = Entrada.objects.all().order_by("-fecha")
	paginator = Paginator(entrada,3)

	try: pagina = int(request.GET.get("page","1"))
	except ValueError: pagina = 1

	try:
		entrada = paginator.page(pagina)
	except(InvalidPage, EmptyPage):
		entrada = Paginator.page(Paginator.num_pages)

	return render_to_response("listado.html",dict(entrada=entrada, months=mkmonth_lst()))