import cv2
import os
import numpy as np
from PIL import Image
from ProyectoAcademia.settings import BASE_DIR
import psycopg2
from psycopg2 import sql
from django.conf import settings


detector = cv2.CascadeClassifier(str(BASE_DIR)+'/autenticacion/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

class FaceRecognition:    

    def saveModelToDatabase(self):
        # Ruta del archivo del modelo
        model_path = str(BASE_DIR) + '/autenticacion/trainer/trainer.yml'

        # Cargar el modelo desde el archivo
        with open(model_path, 'rb') as model_file:
            model_data = model_file.read()

        # Conectar a la base de datos PostgreSQL usando las configuraciones de Django
        conn = psycopg2.connect(
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

        # Crear un cursor para interactuar con la base de datos
        cur = conn.cursor()

        # Nombre de la tabla
        table_name = 'face_model'

        # Verificar si la tabla ya existe en la base de datos
        cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s);", (table_name,))
        table_exists = cur.fetchone()[0]

        if not table_exists:
            # Si la tabla no existe, crea la estructura de la tabla
            create_table_query = sql.SQL("CREATE TABLE {} (model bytea);").format(sql.Identifier(table_name))
            cur.execute(create_table_query)

        # Actualizar o insertar el modelo en la tabla 'face_model'
        cur.execute("UPDATE {} SET model = %s;".format(table_name), (psycopg2.Binary(model_data),))
        if cur.rowcount == 0:
            # Si no se actualizó ninguna fila, insertar un nuevo registro
            cur.execute("INSERT INTO {} (model) VALUES (%s);".format(table_name), (psycopg2.Binary(model_data),))

        # Confirmar y cerrar la conexión
        conn.commit()
        conn.close()


    def loadModelFromDatabase(self):
        # Conectar a la base de datos PostgreSQL usando las configuraciones de Django
        conn = psycopg2.connect(
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

        # Crear un cursor para interactuar con la base de datos
        cur = conn.cursor()

        # Nombre de la tabla
        table_name = 'face_model'

        # Obtener el modelo desde la tabla 'face_model'
        cur.execute("SELECT model FROM {} LIMIT 1;".format(table_name))
        model_data = cur.fetchone()[0]

        # Cerrar la conexión
        conn.close()
        return model_data


    def faceDetect(self, Entry1,):
        face_id = Entry1
        cam = cv2.VideoCapture(0)
        

        count = 0

        while(True):

            ret, img = cam.read()
            # img = cv2.flip(img, -1) # flip video image vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
                count += 1

                # Save the captured image into the datasets folder
                cv2.imwrite(str(BASE_DIR)+'/autenticacion/dataset/User.' + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

                cv2.imshow('Register Face', img)

            k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 100: # Take 30 face sample and stop video
                break
    
    
        cam.release()
        cv2.destroyAllWindows()

    
    def trainFace(self):
        # Path for face image database
        path = str(BASE_DIR)+'/autenticacion/dataset'

        # function to get the images and label data
        def getImagesAndLabels(path):

            imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
            faceSamples=[]
            ids = []

            for imagePath in imagePaths:

                PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
                img_numpy = np.array(PIL_img,'uint8')

                face_id = int(os.path.split(imagePath)[-1].split(".")[1])
                print("face_id",face_id)
                faces = detector.detectMultiScale(img_numpy)

                for (x,y,w,h) in faces:
                    faceSamples.append(img_numpy[y:y+h,x:x+w])
                    ids.append(face_id)

            return faceSamples,ids

        print ("\n Training faces. It will take a few seconds. Wait ...")
        faces,ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        recognizer.save(str(BASE_DIR)+'/autenticacion/trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi


        faceRecognition = FaceRecognition()
        # Otros procesos...
        # Luego, cuando desees guardar el modelo en la base de datos:
        faceRecognition.saveModelToDatabase()

        # Print the numer of faces trained and end program
        print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))


    def recognizeFace(self):

        faceRecognition = FaceRecognition()
        model_data = faceRecognition.loadModelFromDatabase()

        # Verificar si se obtuvo el modelo
        if model_data is not None:
            # Guardar el modelo en un archivo temporal
            temp_model_path = str(BASE_DIR) + '/autenticacion/trainer/temp_model.yml'
            with open(temp_model_path, 'wb') as temp_model_file:
                temp_model_file.write(model_data)

            # Cargar el modelo en el reconocedor desde el archivo temporal
            recognizer.read(temp_model_path)

            # Borrar el archivo temporal
            os.remove(temp_model_path)

        #recognizer.read(BASE_DIR+'/Face_Detection/trainer/trainer.yml')
        
        
        
        
        cascadePath = str(BASE_DIR)+'/autenticacion/haarcascade_frontalface_default.xml'
        faceCascade = cv2.CascadeClassifier(cascadePath)

        font = cv2.FONT_HERSHEY_SIMPLEX

        confidence = 0
        cam = cv2.VideoCapture(0)

        # Define min window size to be recognized as a face
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)

        while True:

            ret, img =cam.read()

            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
            )

            for(x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

                face_id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

                # Check if confidence is less then 100 ==> "0" is perfect match 
                if (confidence < 100):
                    name = 'Detected'
                else:
                    name = "Unknown"
                
                cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
            
            cv2.imshow('Detect Face',img) 

            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
            if confidence > 50:
                break

        print("\n Exiting Program")
        cam.release()
        cv2.destroyAllWindows()
        print(face_id)
        return face_id