def costo_total_cursos(request):
    total=0
    if request.user.is_authenticated:
        if 'registro' in request.session:
            for key, value in request.session["registro"].items():
                total=total+float(value["precio"])
    return  {"costo_total_cursos":total}