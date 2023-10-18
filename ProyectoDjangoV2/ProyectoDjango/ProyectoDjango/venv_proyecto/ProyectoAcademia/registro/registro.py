class Registro:
    def __init__(self, request):
        self.request=request
        self.session=request.session
        registro=self.session.get("registro")
        if not registro:
            registro=self.session["registro"]={}
        self.registro=registro

    def agregar(self, curso):
        if(str(curso.id) not in self.registro.keys()):
            self.registro[curso.id]={
                "curso_id":curso.id,
                "nombre":curso.nombre,
                "precio":curso.precio,
                "cantidad":1,
                "imagen":curso.imagen.url
            }
        self.guardar_registro()
    
    def guardar_registro(self):
        self.session["registro"]=self.registro
        self.session.modified=True

    def eliminar(self, curso):
        curso.id=str(curso.id)
        if curso.id in self.registro:
            del self.registro[curso.id]
            self.guardar_registro()

    def borrar_todo(self):
        self.session["registro"]={}
        self.session.modified=True