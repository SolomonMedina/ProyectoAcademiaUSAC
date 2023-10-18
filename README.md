# ProyectoAcademiaUSAC
Proyecto de Academia USAC de Proyectos de computación aplicados a Ingenieria Electronica

ENUNCIADO

La “Academia USAC” es una institución que ofrece una amplia variedad de cursos
especializados en el área de ingeniería. Actualmente cuentan con un sistema no
muy convencional. Por ello, se requiere de sus servicios como ingeniero con
conocimientos en programación para que desarrolle una nueva aplicación en la que
se tenga un mejor control de los cursos en los que se inscriben los estudiantes.
Se requiere que el sistema pueda ser utilizado por el administradores,
profesores y estudiantes, esto implica que la solución deberá tener un diseño
agradable e intuitivo de acorde a los requerimientos de la academia.

ESPECIFICACIONES DEL PROGRAMA

Página Principal
Al iniciar el sitio web se presentará la página principal en la que se mostrará
información sobre la Academia USAC, los servicios que ofrecen y algunos precios.
Iniciar Sesión - Registro
Al iniciar el programa se presentará una ventana para iniciar sesión, los datos
ingresados deberán consultarse en la base de datos para ver si el usuario existe.
En la base de datos está almacenado el tipo de usuario que está ingresando al
sistema (Administrador, catedrático o alumno). Por lo que, si el usuario es
Administrador, se debe abrir la vista de Administración, si es Catedrático, se
debe abrir la vista solo para Catedráticos o si el usuario es alumno, se deberá
abrir la vista de alumno. Si un usuario no posee una cuenta tendrá que registrarse
primero en la opción de Registrarse, en esta opción solo podrán registrarse
usuarios de tipo alumno, el usuario catedrático tendrá que ser registrado por el
ADMINISTRADOR. Tomar en cuenta que se debe contar con la opción de poder
cerrar sesión cuando se desee. Adicionalmente, se deberá de poder iniciar sesión
por medio de reconocimiento facial, para lo cual al momento de registrarse se
deberán de tomar las fotografías necesarias para crear un modelo de OpenCV
en su inicio de sesión.
Los datos que se deberán solicitar al usuario para el registro, según su rol son
los siguientes:

Estudiante:
• Nombre
• Apellido
• DPI
• Fecha de nacimiento
• Teléfono
• Nombre de usuario (deberá de ser único)
• Dirección de correo electrónico
• Contraseña
• Confirmación de contraseña
Catedrático:
• Nombre
• Apellido
• DPI
• Contraseña
• Confirmación de contraseña

Durante el inicio de sesión el usuario podrá recuperar su contraseña en dado
caso la haya olvidado, para lo cual se enviará un correo con un enlace único para
realizar dicho proceso. Si un usuario ingresa de forma incorrecta su contraseña
más de 3 veces el sistema deberá de bloquear la cuenta de manera automática y
mandar un correo al usuario indicando que su cuenta ha sido bloqueada, por lo
que deberá solicitar al administrador que la desbloquee.
Asignación de cursos
En la página de asignación de cursos el estudiante podrá seleccionar los cursos
a los que desea asignarse y realizar su proceso de inscripción. Una vez el
estudiante se haya registrado tendrá su cupo reservado y podrá acceder al
mismo, adicionalmente se enviará un correo electrónico a la dirección registrada
por el usuario confirmando su inscripción. En caso de que el cupo de un curso se
encuentre lleno deberá de mostrar un mensaje que su inscripción no ha sido
posible.
Cursos
Los cursos podrán ser creados únicamente por el administrador, el cual asignara
el costo, horario, código, cupo y catedrático; Cada vez que se cree un nuevo curso
deberá de ser visible automáticamente por los estudiantes en la página de

asignación de cursos. Cada uno de los cursos deberá contar con su propia página,
a la cual podrán acceder solo los estudiantes inscritos, dicha página deberá
poder ser administrada por el catedrático, por simplicidad se recomienda que
únicamente pueda editar una imagen tipo banner y un mensaje de bienvenida.
Administrador
El administrador deberá de poder acceder a un panel de administración, desde
el cual podrá registrar a nuevos profesores. Además, deberá de poder crear
nuevos cursos con sus respectivas propiedades, ver el listado de profesores
registrados y los cursos que imparten, y ver los listados de notas de cada curso.
Cada uno de los listados deberá de poderse descargar en formato .xlsx.
Finalmente, el administrador deberá de poder desbloquear las cuentas de
usuarios que hayan intentado iniciar sesión más de 3 veces con datos incorrectos.
Profesor
El profesor podrá acceder a un panel de administración desde donde podrá
editar cada uno de sus cursos, así mismo ver el registro de notas de cada
estudiante y poderlas editar. Adicionalmente se deberá de contar con la opción
de descargar el registro de notas en un documento de extensión .xlsx.
Estudiante
Todos los estudiantes deberán de poder ver los listados de cursos, sin embargo,
para registrase a un curso se deberá de tener sesión iniciada. Los estudiantes
deberán de poder ver los cursos disponibles, asignarse, ingresar las páginas de
los cursos a los que se encuentren inscritos, y desasignarse los cursos que ellos
deseen. Adicionalmente, si su nota es mayor o igual que 61 deberá de poder
descargar un certificado que contenga el nombre del curso y los datos del
estudiante.
Base de datos
Se deberá de utilizar únicamente PostgreSQL como gestor de base de datos.
Todos los datos sensibles (principalmente las contraseñas) deberán de
encontrarse encriptadas.
