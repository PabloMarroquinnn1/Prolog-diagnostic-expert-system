% ============================================================
%  Doctor Byte - Base de Conocimiento
%  Inteligencia Artificial 1 - USAC 2026
% ============================================================
% ------------------------------------------------------------
%  SINTOMAS (15 sintomas)
% ------------------------------------------------------------
sintoma(pantalla_negra).
sintoma(pantalla_azul).
sintoma(no_enciende).
sintoma(reinicio_inesperado).
sintoma(lentitud_extrema).
sintoma(sobrecalentamiento).
sintoma(ruido_disco).
sintoma(no_detecta_disco).
sintoma(error_arranque).
sintoma(sin_imagen_monitor).
sintoma(wifi_no_conecta).
sintoma(puerto_usb_no_funciona).
sintoma(bateria_no_carga).
sintoma(pantalla_artefactos).
sintoma(memoria_insuficiente).

% ------------------------------------------------------------
%  HECHOS - sintomas por falla
% ------------------------------------------------------------
falla_sintoma(falla_ram,             [pantalla_azul, reinicio_inesperado, memoria_insuficiente]).
falla_sintoma(falla_disco_duro,      [ruido_disco, no_detecta_disco, error_arranque, lentitud_extrema]).
falla_sintoma(falla_gpu,             [pantalla_artefactos, sin_imagen_monitor, pantalla_azul]).
falla_sintoma(sobrecalentamiento_cpu,[sobrecalentamiento, reinicio_inesperado, lentitud_extrema]).
falla_sintoma(falla_fuente_poder,    [no_enciende, reinicio_inesperado, bateria_no_carga]).
falla_sintoma(falla_sistema_operativo,[pantalla_azul, error_arranque, lentitud_extrema]).
falla_sintoma(falla_tarjeta_red,     [wifi_no_conecta]).
falla_sintoma(falla_controlador_usb, [puerto_usb_no_funciona]).
falla_sintoma(falla_monitor,         [pantalla_negra, sin_imagen_monitor]).
falla_sintoma(falla_bateria,         [bateria_no_carga, no_enciende]).

% ------------------------------------------------------------
%  RECOMENDACIONES por falla
% ------------------------------------------------------------
recomendacion(falla_ram,
    'Verificar que los modulos RAM esten bien insertados. Probar con un modulo a la vez. Considerar reemplazar el modulo defectuoso.').
recomendacion(falla_disco_duro,
    'Respaldar datos inmediatamente. Ejecutar chkdsk o fsck. Evaluar reemplazo del disco por SSD.').
recomendacion(falla_gpu,
    'Limpiar la GPU y verificar conexiones. Actualizar o reinstalar drivers. Si persiste, reemplazar la tarjeta grafica.').
recomendacion(sobrecalentamiento_cpu,
    'Limpiar el sistema de refrigeracion. Reemplazar la pasta termica. Verificar que el ventilador funcione correctamente.').
recomendacion(falla_fuente_poder,
    'Probar con otra fuente de poder. Verificar el voltaje de salida con multimetro. Reemplazar la fuente si es necesario.').
recomendacion(falla_sistema_operativo,
    'Ejecutar reparacion de inicio desde medios de instalacion. Considerar reinstalacion del sistema operativo.').
recomendacion(falla_tarjeta_red,
    'Actualizar drivers de red. Verificar configuracion de red. Probar con adaptador USB externo.').
recomendacion(falla_controlador_usb,
    'Actualizar drivers USB desde el administrador de dispositivos. Verificar en otro puerto. Revisar BIOS.').
recomendacion(falla_monitor,
    'Verificar cable de video y conexiones. Probar con otro monitor. Revisar configuracion de pantalla.').
recomendacion(falla_bateria,
    'Calibrar la bateria. Si tiene mas de 2 anos considerar reemplazo. Verificar cargador con multimetro.').

% ------------------------------------------------------------
%  NOMBRES LEGIBLES por falla
% ------------------------------------------------------------
nombre_falla(falla_ram,              'Falla en memoria RAM').
nombre_falla(falla_disco_duro,       'Falla en disco duro').
nombre_falla(falla_gpu,              'Falla en tarjeta grafica (GPU)').
nombre_falla(sobrecalentamiento_cpu, 'Sobrecalentamiento de CPU').
nombre_falla(falla_fuente_poder,     'Falla en fuente de poder').
nombre_falla(falla_sistema_operativo,'Falla en sistema operativo').
nombre_falla(falla_tarjeta_red,      'Falla en tarjeta de red').
nombre_falla(falla_controlador_usb,  'Falla en controlador USB').
nombre_falla(falla_monitor,          'Falla en monitor').
nombre_falla(falla_bateria,          'Falla en bateria').

% ------------------------------------------------------------
%  NOMBRES LEGIBLES por sintoma
% ------------------------------------------------------------
nombre_sintoma(pantalla_negra,          'Pantalla negra').
nombre_sintoma(pantalla_azul,           'Pantalla azul (BSOD)').
nombre_sintoma(no_enciende,             'El equipo no enciende').
nombre_sintoma(reinicio_inesperado,     'Reinicios inesperados').
nombre_sintoma(lentitud_extrema,        'Lentitud extrema').
nombre_sintoma(sobrecalentamiento,      'Sobrecalentamiento').
nombre_sintoma(ruido_disco, 'Ruido extrano en disco').
nombre_sintoma(no_detecta_disco,        'No detecta el disco duro').
nombre_sintoma(error_arranque,          'Error al arrancar').
nombre_sintoma(sin_imagen_monitor,      'Sin imagen en monitor').
nombre_sintoma(wifi_no_conecta,         'WiFi no conecta').
nombre_sintoma(puerto_usb_no_funciona,  'Puerto USB no funciona').
nombre_sintoma(bateria_no_carga,        'Bateria no carga').
nombre_sintoma(pantalla_artefactos,     'Artefactos visuales en pantalla').
nombre_sintoma(memoria_insuficiente,    'Memoria insuficiente / errores de memoria').

% ------------------------------------------------------------
%  VALIDACION con corte (!)
% ------------------------------------------------------------

% Verifica si un sintoma existe - usa corte para evitar backtracking innecesario
sintoma_valido(S) :- sintoma(S), !.
sintoma_valido(S) :- 
    \+ sintoma(S), !,
    fail.

% Filtra solo los sintomas validos de una lista
filtrar_sintomas_validos([], []).
filtrar_sintomas_validos([S|Resto], [S|Validos]) :-
    sintoma(S), !,
    filtrar_sintomas_validos(Resto, Validos).
filtrar_sintomas_validos([_|Resto], Validos) :-
    filtrar_sintomas_validos(Resto, Validos).

% ------------------------------------------------------------
%  REGLAS DE INFERENCIA
% ------------------------------------------------------------

% Contar cuantos sintomas del paciente coinciden con los de una falla
contar_coincidencias([], _, 0).
contar_coincidencias([S|Resto], SintomasPaciente, Total) :-
    (member(S, SintomasPaciente) -> Parcial = 1 ; Parcial = 0),
    contar_coincidencias(Resto, SintomasPaciente, SubTotal),
    Total is SubTotal + Parcial.

% Calcular porcentaje de coincidencia
porcentaje(Coincidencias, Total, Porcentaje) :-
    Total > 0,
    Porcentaje is (Coincidencias * 100) // Total.

% Regla principal de diagnostico
diagnosticar(SintomasPaciente, Falla, NombreFalla, Porcentaje, Recomendacion) :-
    falla_sintoma(Falla, SintomasFalla),
    contar_coincidencias(SintomasFalla, SintomasPaciente, Coincidencias),
    Coincidencias > 0,
    length(SintomasFalla, Total),
    porcentaje(Coincidencias, Total, Porcentaje),
    recomendacion(Falla, Recomendacion),
    nombre_falla(Falla, NombreFalla).

% Obtener todos los diagnosticos ordenados por porcentaje descendente
todos_diagnosticos(Sintomas, Diagnosticos) :-
    filtrar_sintomas_validos(Sintomas, SintomasValidos),
    findall(
        diag(P, F, N, R),
        diagnosticar(SintomasValidos, F, N, P, R),
        DiagnosticosRaw
    ),
    msort(DiagnosticosRaw, Ordenados),
    reverse(Ordenados, Diagnosticos).

% Obtener lista de todos los sintomas disponibles
lista_sintomas(Sintomas) :-
    findall(S-N, nombre_sintoma(S, N), Sintomas).