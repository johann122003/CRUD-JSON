import pyodbc
import json

class MashicManager:
    def __init__(self):
        """Punto 2: Inicializar conexión desde JSON"""
        try:
            with open('config.json', 'r') as archivo_config:
                config = json.load(archivo_config)
            
            # Variables de conexión desde el JSON
            n_server = config['name_server']
            db = config['database']
            u_name = config['username']
            p_word = config['password']
            c_odbc = config['driver']

            self.connection_string = f'DRIVER={c_odbc};SERVER={n_server};DATABASE={db};UID={u_name};PWD={p_word}'
            self.conexion = pyodbc.connect(self.connection_string)
            print("\n\t>>> CONEXIÓN EXITOSA: Bienvenido a MashicDb")
            
        except Exception as e:
            print("\n \t Error Crítico de Conexión: \n\n", e)

    def consultar_canciones(self):
        """Lectura de datos - Estilo Profe"""
        try:
            micursor = self.conexion.cursor()
            SENTENCIA_SQL = "{CALL Core.sp_ConsultarCanciones}" 
            micursor.execute(SENTENCIA_SQL)
        except Exception as e:
            print("\n \t Error al consultar biblioteca: \n\n", e)
        else:
            rows = micursor.fetchall()
            print("\n" + "="*60)
            print(f"{'ID':<5} | {'TÍTULO':<25} | {'ÁLBUM':<15} | {'DUR.'}")
            print("="*60)
            for row in rows:
                print(f"{row.ID_Canto:<5} | {row.Titulo:<25} | {row.Titulo_Album:<15} | {row.Duracion_Segundos}s")
            
            print("\nOk ... Proceso Culminado con Exito: \n")
        finally:
            print("\t--- Consulta finalizada ---\n")

    def crear_cancion(self):
        """Inserción de datos - Estilo Profe"""
        try:
            micursor = self.conexion.cursor()
            print("\n\t\tINSERTAR NUEVA CANCIÓN A MASHIC:\n")  
            
            l_ID_Canto = int(input("Ingrese ID de la Canción: \t"))
            l_Titulo = input("Ingrese Título de la Canción: \t")
            l_Ruta = f"/music/{l_Titulo.lower().replace(' ', '_')}.mp3"
            l_Peso = int(input("Ingrese Peso en MB (máx 20): \t"))
            l_Duracion = int(input("Ingrese Duración (seg): \t"))
            l_ID_Album = int(input("Ingrese ID del Álbum: \t\t"))
            
            SENTENCIA_SQL = "{CALL Core.sp_InsertarCancion (?,?,?,?,?,?)}"
            micursor.execute(SENTENCIA_SQL, (l_ID_Canto, l_Titulo, l_Ruta, l_Peso, l_Duracion, l_ID_Album))
            
            self.conexion.commit()
            print("\nOk ... Inserción Exitosa: \n")
        except Exception as e:
            print("\n \t Error al insertar registro: \n\n", e)
        finally:
            print("\t--- Registro terminado ---\n")
            
    def actualizar_cancion(self):
        """Método para Actualizar (Estilo Profe)"""
        try:
            micursor = self.conexion.cursor()
            print("\n\t ACTUALIZAR INFORMACIÓN DE CANCIÓN:\n")
            
            # Captura de datos con l_
            l_ID_Canto = int(input("Ingrese ID de la canción a modificar: \t"))
            l_NuevoTitulo = input("Ingrese el Nuevo Título: \t\t")
            l_NuevaDuracion = int(input("Ingrese la Nueva Duración (seg): \t"))
            
            # Llamada al procedimiento almacenado
            SENTENCIA_SQL = "{CALL Core.sp_ActualizarCancion (?,?,?)}"
            micursor.execute(SENTENCIA_SQL, (l_ID_Canto, l_NuevoTitulo, l_NuevaDuracion))
            
            self.conexion.commit()
            print("\nOk ... Actualización Exitosa: \n")
        except Exception as e:
            print("\n \t Ocurrió un error al actualizar en MashicDb: \n\n", e)
        finally:
            print("\t--- Proceso de Actualización Terminado ---\n")

    def eliminar_cancion(self):
        """Eliminación de datos - Estilo Profe"""
        try:
            micursor = self.conexion.cursor()
            print("\n\t ELIMINAR CANCIÓN DE MASHIC:\n")
            l_ID_Canto = int(input("Ingrese ID de la canción a borrar: \t"))
            
            SENTENCIA_SQL = "{CALL Core.sp_EliminarCancion (?)}"
            micursor.execute(SENTENCIA_SQL, (l_ID_Canto,))
            self.conexion.commit()   
            print("Ok ... Eliminación Exitosa: \n")
        except Exception as e:
            print("\n \t Error al eliminar registro: \n\n", e)
        finally:
            print("\t--- Eliminación terminada ---\n")

    def ejecutar_menu(self):
        """Punto 4: Menú CRUD UDEMYTEST / MASHIC"""
        while True:
            print("\n\t** SISTEMA CRUD MASHIC DB **")
            print("\t1. Crear canción ")
            print("\t2. Consultar biblioteca ")
            print("\t3. Actualizar canción ")
            print("\t4. Eliminar canción ")
            print("\t5. Salir")
            
            opcion = input("\n\tSeleccione una opción: ")

            if opcion == '1':
                self.crear_cancion()
            elif opcion == '2':
                self.consultar_canciones()
            elif opcion == '3':
                self.actualizar_cancion()
            elif opcion == '4':
                self.eliminar_cancion()
            elif opcion == '5':
                if hasattr(self, 'conexion'):
                    self.conexion.close()
                print("\nConexión Cerrada. Proceso culminado con éxito.")
                break
            else:
                print("\nOpción no válida, intente de nuevo.")

if __name__ == "__main__":
    app = MashicManager()
    app.ejecutar_menu()