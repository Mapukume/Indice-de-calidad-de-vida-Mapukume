"""
Tool:               <Tool label>
Source Name:        <File name>
Version:            <ArcGIS Version>
Author:             <Author>
Usage:              <Command syntax>
Required Arguments: <parameter0>
                    <parameter1>
Optional Arguments: <parameter2>
                    <parameter3>
Description:        <Description>
"""
# -*- coding: utf-8 -*-

import arcpy

# Definir entorno
aprx = arcpy.mp.ArcGISProject("CURRENT")
aprxMap = aprx.listMaps()[0]
layers = aprxMap.listLayers()
layers = layers[0:len(layers)-2]
#Limpiar tabla de contenido, pero mantener mapa base
for layer in layers:
   aprxMap.removeLayer(layer)
#Limpiar tablas
tables = aprxMap.listTables()
for table in tables:
   aprxMap.removeTable(table)

def ScriptTool(inpFt, outDir, resum_fc_ed, resum_fc_salud, resum_fc_bibl, 
    resum_fc_mon, resum_fc_museo, tabla_seg,tabla_ingreso,tabla_dep,tabla_oficio,
    tabla_hac,tabla_servicio,areas_verdes,parque_v,antenas_com,calles_com,encuesta,pond_cl,pond_csc,pond_ve,pond_cm):
    """ScriptTool function docstring"""

    return


if __name__ == '__main__':
    # ScriptTool parameters
    ## Pedir comunas
    inpFt = arcpy.GetParameterAsText(0)
    ## Pedir GDB
    outDir = arcpy.GetParameterAsText(1)
    ## Pedir puntos de establecimientos
    resum_fc_ed = arcpy.GetParameterAsText(2)
    ## Pedir puntos de salud
    resum_fc_salud = arcpy.GetParameterAsText(3)
    ## Pedir puntos de bibliotecas
    resum_fc_bibl = arcpy.GetParameterAsText(4)
    ## Pedir puntos de monumentos
    resum_fc_mon = arcpy.GetParameterAsText(5)
    ## Pedir puntos de museos
    resum_fc_museo = arcpy.GetParameterAsText(6)
    ## Pedir tabla indice seguridad
    tabla_seg = arcpy.GetParameterAsText(7)
    ## Pedir tabla ingresos
    tabla_ingreso = arcpy.GetParameterAsText(8)
    ## Pedir tabla indice dependencia
    tabla_dep= arcpy.GetParameterAsText(9)
    ## Pedir tabla oficio por sector economico
    tabla_oficio = arcpy.GetParameterAsText(10)
    ## Pedir tabla indice hacinamiento
    tabla_hac = arcpy.GetParameterAsText(11)
    ## Pedir tabla con cantidad de serivicios
    tabla_servicio = arcpy.GetParameterAsText(12)
    ## Pedir poligonos con areas verdes
    areas_verdes = arcpy.GetParameterAsText(13)
    ## Pedir tabla con vehiculas de la comuna
    parque_v = arcpy.GetParameterAsText(14)
    ## Pedir puntos de antenas
    antenas_com = arcpy.GetParameterAsText(15)
    ## Pedir linea de calles
    calles_com = arcpy.GetParameterAsText(16)
    ## Resultados encuesta
    encuesta = arcpy.GetParameterAsText(17)
    ## Ponderaion del primer indicador
    pond_cl = arcpy.GetParameterAsText(18)
    ## Ponderaion del segundo indicador
    pond_csc = arcpy.GetParameterAsText(19)
    ## Ponderaion del tercer indicador
    pond_ve = arcpy.GetParameterAsText(20)
    ## Ponderacion del cuarto indicador
    pond_cm = arcpy.GetParameterAsText(21)

    ScriptTool(inpFt, outDir, resum_fc_ed, resum_fc_salud, resum_fc_bibl, 
    resum_fc_mon, resum_fc_museo, tabla_seg,tabla_ingreso,tabla_dep,tabla_oficio,
    tabla_hac,tabla_servicio,areas_verdes,parque_v,antenas_com,calles_com,encuesta,pond_cl,pond_csc,pond_ve,pond_cm)


 # Carga de Datos

arcpy.AddMessage("Capas habilitadas")
# CAMBIA EL FORMATO DE NUMERO QUE SE INGRESA, OSEA CAMBIA LA , POR UN .
ponderaciones = [pond_cl,pond_csc,pond_ve,pond_cm]
pond_arreglado = []
for i in ponderaciones:
    if "," in i:
        if i == "1":
            pond_arreglado.append(float(i))
        else:
            sep = i.split(",")
            numero = sep[0]+"."+sep[1]
            pond_arreglado.append(numero)
    else:
        pond_arreglado.append(i)

#############################################################################################

# DEFINICION DE FUNICONES

#############################################################################################

# FUNCION QUE APLICA EL GEOPROCESO DE RESUMIR DENTRO DE, DONDE ENTRA LA CAPA BASE, CAPA QUE SE QUIERE RESUMIR
# PIDE EL NOMBRE DE LA CAPA DE SALIDA, EL DIRECTORIO. RETORNA LA CAPA DE SALIDA.
# PIDE UNA OPERACION ARITMETICA QUE SI NO ES NECESARIO SE COLOCA None.
def resumir(capa_comuna,capa_resumen,capa_nueva,directorio,operacion,borrar):
    name_fc = capa_nueva
    out_fc = "{}\\{}".format(directorio,name_fc)
    if operacion == None:
        arcpy.analysis.SummarizeWithin(capa_comuna, capa_resumen, out_fc,"KEEP_ALL",None)
        borrar.append(name_fc)
    else:
        arcpy.analysis.SummarizeWithin(capa_comuna, capa_resumen, out_fc,"KEEP_ALL",operacion)
        borrar.append(name_fc)
    return out_fc

# FUNCION QUE RENOMBRA EL CAMPO INGRESADO, PIDE LA CAPA DONDE SE ENCUENTRA EL CAMPO, NOMBRE DEL CAMPO Y 
# A QUE NOMBRE SE CAMBIARA
def renombrarCampo(out_fc,nom_campo,nuevo_nom,alias,campo_agre):
    nuevo_camp = nuevo_nom
    arcpy.management.AlterField(out_fc, nom_campo, nuevo_camp, alias)
    campo_agre.append(nuevo_camp)
    return nuevo_camp

# FUNCION QUE AGREGA UN CAMPO O CAMPOS DESDE OTRA CAPA O TABLA
def agregarCampo(capa_comuna, out_fc, camp_inp, camp_join, alias, campo_agre):
    arcpy.management.JoinField(capa_comuna, camp_inp, out_fc, camp_join, alias)
    if  ";" in alias:
        lista = alias.split(";")
        for i in lista:
            if i not in campo_agre:
                campo_agre.append(i)
    elif ";" not in alias:
        if alias not in campo_agre:
            campo_agre.append(alias)

# FUNCION QUE CREA UN NUEVO CAMPO EN UNA CAPA
def crearCampo(capa_comuna,nombre_campo,campo_agre):
    nombre = nombre_campo
    arcpy.management.AddField(capa_comuna, nombre, "DOUBLE")
    campo_agre.append(nombre)
    return nombre

# FUNCION QUE AGREGA LA CLASE DE ENTIDAD A EL DATASET DE SALIDA
def entidadAentidad(capa_comuna,directorio,nombre,campo_agre):
    nom_ind = nombre
    arcpy.conversion.FeatureClassToFeatureClass(capa_comuna, directorio, nom_ind)
    for i in campo_agre:
        arcpy.management.DeleteField(capa_comuna, i)
    return nom_ind

# FUNCION QUE NORMALIZA LOS CAMPOS AGREGADOS PARA EL INDICADOR
def normalizar(nom_indicador,campo_agre):
    campos_norma = []
    for i in campo_agre:
        campos_norma.append(i+"_N")
        arcpy.management.AddField(nom_indicador, i+"_N", "DOUBLE")

    for i in campo_agre:
        cursor = arcpy.da.SearchCursor(nom_indicador, i)
        acum = 0
        for l in cursor:     
            acum = acum + l[0]
        if acum == 0:
            arcpy.management.CalculateField(nom_indicador, i+"_N",0, "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
        else:
            funcion = "!{}!/{}".format(i,acum)
            arcpy.management.CalculateField(nom_indicador, i+"_N",funcion, "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
        acum = 0
    return campos_norma

# FUNCION QUE APLICA UNA OPERACION ARITMETICA A UN CAMPO
def calcularCampo(capa_comuna,campo,calculo):
    arcpy.management.CalculateField(capa_comuna, campo, calculo, "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")

# FUNCION QUE OBTIENE EL PROMEDIO DE CALLES DE CADA COMUNA, POR TIPO DE CALLE
def promedioCalles(capa_comuna,capa_calles,campo_agre):
    # OBTENER TIPOS DE CALLES
    fields_c = "tipo_de_calle"
    cursor = arcpy.da.SearchCursor(capa_calles, fields_c)
    tipo_calle = [] 
    for i in cursor:    
        if i[0] not in tipo_calle:
            tipo_calle.append(i[0])
            campo_agre.append(i[0])

    # OBTENER LOS CODIGOS DE LAS COMUNAS
    codigo = "cod_comuna"
    cursor = arcpy.da.SearchCursor(capa_comuna, codigo)
    cod = [] 
    for i in cursor:    
        if i[0] not in cod:
            cod.append(i[0])

    # CREAR CAMPOS DE TIPOS DE CALLE EN LA CAPA PRINCIPAL
    for i in tipo_calle:
        arcpy.management.AddField(capa_comuna, i, "DOUBLE")

    # CALCULAR EL PROMEDIO DE DISTANCIA DE LAS CALLES POR TIPO Y SE AGREGA A LOS CAMPOS AGREGADOS POR COMUNA
    # COLOCA LAS CAPAS EN EL CONTENIDO 
    aprxMap.addDataFromPath(capa_comuna)
    aprxMap.addDataFromPath(capa_calles)
    comunas = capa_comuna.split('\\')
    calle = capa_calles.split('\\')
    ruta_gdb = "\\".join(calle[0:-2])
    for i in cod:    
        filtro = "{} = {}".format(codigo,i)
        # SELECCIONA LA COMUNA
        arcpy.management.SelectLayerByAttribute(comunas[-1], "NEW_SELECTION", filtro, None)
        # CORTA LA CAPA DE CALLES CON LA CAPA DE COMUNA PARA OBTENER SOLO LAS CALLES DE LA COMUNA SELECCIONADA
        name_fc = "recorte"
        recorte_c = "{}\\{}".format(ruta_gdb,name_fc)
        arcpy.analysis.Clip(calle[-1], comunas[-1], recorte_c, None)
        aprxMap.addDataFromPath(recorte_c)
        for j in tipo_calle:
            filtro_calle = "{} = '{}'".format(fields_c,j)
            # SUBSELECCIONA POR TIPO DE CALLE
            arcpy.management.SelectLayerByAttribute(name_fc, "ADD_TO_SELECTION", filtro_calle, None)
            distancia = "Shape_Length"
            acum = 0
            ite = 0
            cursor = arcpy.da.SearchCursor(name_fc, distancia)
            for d in cursor:
                acum = acum + d[0]
                ite = ite + 1
            if ite != 0:
                promedio = round(acum/ite,4)
            if promedio != 0:
                arcpy.management.CalculateField(comunas[-1], j, str(promedio))
            else:
                arcpy.management.CalculateField(comunas[-1], j, 0)
            promedio = 0
            # LIMPIA LA SELECCION DE CALLES
            arcpy.management.SelectLayerByAttribute(name_fc, "CLEAR_SELECTION", '', None)   
        arcpy.Delete_management(recorte_c)
    # LIMPIA LA SELECCION DE COMUNAS
    arcpy.management.SelectLayerByAttribute(comunas[-1], "CLEAR_SELECTION", '', None)

# FUNCION QUE ELIMINA LAS CAPAS TEMPORALES
def eliminar(eliminar_capas):
    for fc in eliminar_capas:    
        if arcpy.Exists(outDir):    
            arcpy.Delete_management(fc)

# FUNCION QUE LIMPIA EL CONTENIDO
def borrarContenido(aprxMap):
    layers = aprxMap.listLayers()
    layers = layers[0:len(layers)-2]
    #Limpiar tabla de contenido, pero mantener mapa base
    for layer in layers:
        aprxMap.removeLayer(layer)


#############################################################################################

######################################## CONDICION LABORAL ##################################
#
dimensiones = []
campo_comun = "cod_comuna"
# LISTA CON LOS NOMBRES DE LOS CAMPOS QUE SE VAN CREANDO
campos_agregados = []
# LISTA CON LOS NOMBRES DE LAS CAPAS TEMPORALES
eliminar_capas = []

# AGREGA EL CAMPO DE TABLA INGRESOS
ing_camp = "INM"
agregarCampo(inpFt, tabla_ingreso, campo_comun, campo_comun, ing_camp, campos_agregados)
# AGREGA EL CAMPO DE TABLA INDICE DE DEPENDENCIA
id_camp = "indice"
agregarCampo(inpFt, tabla_dep, campo_comun, campo_comun, id_camp, campos_agregados)
# AGREGA EL CAMPO DE TABLA DE SECTORES ECONOMICOS
sec_camp = "Act_primaria;Act_secundaria;Act_terciaria" 
agregarCampo(inpFt, tabla_oficio, campo_comun, campo_comun, sec_camp, campos_agregados)

# AGREGA LA CLASE DE ENTIDAD AL DATASET DE SALIDA Y BORRA LOS CAMPOS AGREGADOS
nom_cl = "C_laboral"
agrega_cl = entidadAentidad(inpFt, outDir, nom_cl, campos_agregados)

# NORMALIZA LOS CAMPOS AGREGADOS
norma_cl = normalizar(agrega_cl, campos_agregados)

# CREA UN NUEVO CAMPOS PARA CALCULAR EL INDICE
camp_cl = "icv_C_L"
icv_C_L = crearCampo(agrega_cl, camp_cl, dimensiones)

# CALCULA EL INDICE
funcion = "!{}!*0.33+!{}!*0.33+(!{}!*0.25+!{}!*0.35+!{}!*0.4)*0.33".format(norma_cl[0],norma_cl[1],norma_cl[2],norma_cl[3],norma_cl[4])
calcularCampo(agrega_cl, camp_cl, funcion)

arcpy.AddMessage("Clase de entidad agregada")
#
###################################### CONDICIONES SOCIO CULTURALES ###################
#
# LISTA CON LOS NOMBRES DE LOS CAMPOS QUE SE VAN CREANDO
campos_agregados = []

# RESUMIR LA CANTIDAD DE ESTABLECIMIENTOS EDUCACIONALES POR COMUNA
# RENOMBRA EL CAMPO CON LA CANTIDAD DE PUNTOS
# AGREGA EL CAMPO A LA CAPA DE LA COMUNA
nom_ed = "educacion_comuna"
res_ed = resumir(inpFt, resum_fc_ed, nom_ed, outDir, None, eliminar_capas)
campo_cantidad = "Point_Count"
renombre_ed = "cant_ed"
nom = renombrarCampo(res_ed, campo_cantidad, renombre_ed, renombre_ed, campos_agregados)
agregarCampo(inpFt, res_ed, campo_comun, campo_comun, nom, campos_agregados)

# RESUMIR LA CANTIDAD DE ESTABLECIMIENTOS DE SALUD POR COMUNA
# RENOMBRA EL CAMPO CON LA CANTIDAD DE PUNTOS
# AGREGA EL CAMPO A LA CAPA DE LA COMUNA
nom_salud = "salud_comuna"
res_salud = resumir(inpFt, resum_fc_salud, nom_salud, outDir, None, eliminar_capas)
renombre_salud = "cant_salud"
nom = renombrarCampo(res_salud, campo_cantidad, renombre_salud, renombre_salud, campos_agregados)
agregarCampo(inpFt, res_salud, campo_comun, campo_comun, nom, campos_agregados)

# RESUMIR LA CANTIDAD DE BIBLIOTECAS POR COMUNA
# RENOMBRA EL CAMPO CON LA CANTIDAD DE PUNTOS
# AGREGA EL CAMPO A LA CAPA DE LA COMUNA
nom_biblio = "biblio_comuna"
res_biblio = resumir(inpFt, resum_fc_bibl, nom_biblio, outDir, None, eliminar_capas)
renombre_biblio = "cant_biblio"
nom = renombrarCampo(res_biblio, campo_cantidad, renombre_biblio, renombre_biblio, campos_agregados)
agregarCampo(inpFt, res_biblio, campo_comun, campo_comun, nom, campos_agregados)

# RESUMIR LA CANTIDAD DE MONUMENTOS POR COMUNA
# RENOMBRA EL CAMPO CON LA CANTIDAD DE PUNTOS
# AGREGA EL CAMPO A LA CAPA DE LA COMUNA
nom_monum = "monum_comuna"
res_monum = resumir(inpFt, resum_fc_mon, nom_monum, outDir, None, eliminar_capas)
renombre_monum = "cant_monum"
nom = renombrarCampo(res_monum, campo_cantidad, renombre_monum, renombre_monum, campos_agregados)
agregarCampo(inpFt, res_monum, campo_comun, campo_comun, nom, campos_agregados)

# RESUMIR LA CANTIDAD DE MUSEOS POR COMUNA
# RENOMBRA EL CAMPO CON LA CANTIDAD DE PUNTOS
# AGREGA EL CAMPO A LA CAPA DE LA COMUNA
nom_museos = "museos_comuna"
res_museos = resumir(inpFt, resum_fc_museo, nom_museos, outDir, None, eliminar_capas)
renombre_museos = "cant_museos"
nom = renombrarCampo(res_museos, campo_cantidad, renombre_museos, renombre_museos, campos_agregados)
agregarCampo(inpFt, res_museos, campo_comun, campo_comun, nom, campos_agregados)

# AGREGA EL CAMPO DE LA TABLA INDICE DE SEGURIDAD
camp_join = "cod_com"
agregarCampo(inpFt, tabla_seg, campo_comun, camp_join, id_camp, campos_agregados)

# AGREGA LA CLASE DE ENTIDAD AL DATASET DE SALIDA Y BORRA LOS CAMPOS AGREGADOS
nom_csc = "C_socioCultural"
agrega_SC = entidadAentidad(inpFt, outDir, nom_csc, campos_agregados)

# NORMALIZA LOS CAMPOS AGREGADOS
norma_SC = normalizar(agrega_SC, campos_agregados)

# CREA UN NUEVO CAMPOS PARA CALCULAR EL INDICE
camp_csc = "icv_S_C"
icv_S_C = crearCampo(agrega_SC, camp_csc, dimensiones)

# CALCULA EL INDICE
funcion = "(!{}!+!{}!)*0.33+(!{}!+!{}!+!{}!)*0.33+!{}!*0.33".format(norma_SC[0],norma_SC[1],norma_SC[2],norma_SC[3],norma_SC[4],norma_SC[5])
calcularCampo(agrega_SC, camp_csc, funcion)

arcpy.AddMessage("Clase de entidad agregada")
#
################################### VIVIENDA Y ENTORNO ######################################
#
# LISTA CON LOS NOMBRES DE LOS CAMPOS QUE SE VAN CREANDO
campos_agregados = []

# AGREGA EL CAMPO DE LA TABLA INDICE DE HACINAMIENTO
comun_h = "cod_com"
camp_h = "indice_H"
agregarCampo(inpFt, tabla_hac, campo_comun, comun_h, camp_h, campos_agregados)

# AGREGA EL CAMPO DE LA TABLA DE SERVICIOS SECUNDARIOS
camp_ss = "conteo"
agregarCampo(inpFt, tabla_servicio, campo_comun, campo_comun, camp_ss, campos_agregados)

# AGREGA EL CAMPO DE LA TABLA DE DATOS OBTENIDOS DE LA ENCUESTA
campo_total = "Total"
agregarCampo(inpFt, encuesta, campo_comun, campo_comun, campo_total, campos_agregados)

# RESUMIR LA SUPERFICIE DE AREAS VERDES POR COMUNA, SUMANDO LAS AREAS
# RENONBRA EL CAMPO DE SUMA SUPERFICIE
# AGREGA EL CAMPO A LA CAPA DE LA COMUNA
# CREA UN NUEVO CAMPO
nom_areav = "areaV_comuna"
opera = "SUPERFICIE Sum"
res_sup = resumir(inpFt,areas_verdes, nom_areav, outDir, opera, eliminar_capas)
campo_renom = "sum_superficie"
renombre_sup = "superficie"
nom = renombrarCampo(res_sup, campo_renom, renombre_sup, renombre_sup, campos_agregados)
agregarCampo(inpFt,res_sup, campo_comun, campo_comun, nom, campos_agregados)
nuevo_campo = "disponible"
campo_areav = crearCampo(inpFt, nuevo_campo, campos_agregados)

# REALIZA UN CALCULO EN EL CAMPO CREADO
calculo = "!{}!/!{}!".format(nom,"Shape_Area")
calcularCampo(inpFt,campo_areav,calculo)

# AGREGA LA CLASE DE ENTIDAD AL DATASET DE SALIDA Y BORRA LOS CAMPOS AGREGADOS
nom_ve = "V_entorno"
agrega_VE = entidadAentidad(inpFt, outDir, nom_ve, campos_agregados)

# NORMALIZA LOS CAMPOS AGREGADOS
norma_VE = normalizar(agrega_VE, campos_agregados)

# CREA UN NUEVO CAMPOS PARA CALCULAR EL INDICE
camp_VE = "icv_V_E"
icv_V_E = crearCampo(agrega_VE, camp_VE, dimensiones)

# CALCULA EL INDICE
funcion = "!{}!*0.30+!{}!*0.30+!{}!*0.1+!{}!*0.30".format(norma_VE[0],norma_VE[1],norma_VE[2],norma_VE[3])
calcularCampo(agrega_VE, camp_VE, funcion)

arcpy.AddMessage("Clase de entidad agregada")
#
########################### CONECTIVIDAD Y MOVILIDAD ############################
#
# LISTA CON LOS NOMBRES DE LOS CAMPOS QUE SE VAN CREANDO
campos_agregados = []

# AGREGAS LOS CAMPOS DEL PARQUE VEHICULAR A LA CAPA DE LA COMUNA
camp_pv = "TOTAL_TAXI;TOTAL_BUS;TOTAL_METRO"
agregarCampo(inpFt, parque_v, campo_comun, campo_comun, camp_pv, campos_agregados)

# RESUMIR LA CANTIDAD DE ANTENAS POR COMUNA
# RENOMBRA EL CAMPO CON LA CANTIDAD DE PUNTOS
# AGREGA EL CAMPO A LA CAPA DE LA COMUNA
nom_antenas = "antenas_comunas"
res_antenas = resumir(inpFt, antenas_com, nom_antenas, outDir, None, eliminar_capas)
renombre_ant = "cant_ant"
nom = renombrarCampo(res_antenas, campo_cantidad, renombre_ant,renombre_ant, campos_agregados)
agregarCampo(inpFt, res_antenas, campo_comun, campo_comun, nom, campos_agregados)

# OBTIENE LOS PROMEDIOS DE DISTANCIA DE LAS CALLES POR SU TIPO DE CADA COMUNA
promedioCalles(inpFt, calles_com, campos_agregados)
borrarContenido(aprxMap)

# AGREGA LA CLASE DE ENTIDAD AL DATASET DE SALIDA Y BORRA LOS CAMPOS AGREGADOS
nom_CM = "C_movilidad"
agrega_CM = entidadAentidad(inpFt, outDir, nom_CM, campos_agregados)

# NORMALIZA LOS CAMPOS AGREGADOS
norma_CM = normalizar(agrega_CM, campos_agregados)

# CREA UN NUEVO CAMPOS PARA CALCULAR EL INDICE
camp_CM = "icv_C_M"
icv_C_M = crearCampo(agrega_CM, camp_CM, dimensiones)

# CALCULA EL INDIE
funcion = "(!{}!*2+!{}!*4+!{}!*3)*0.33+!{}!*0.33+(!{}!*2+!{}!*3+!{}!*1+!{}!*4)*0.33".format(norma_CM[0],norma_CM[1],norma_CM[2],norma_CM[3],
    norma_CM[4],norma_CM[5],norma_CM[6],norma_CM[7])
calcularCampo(agrega_CM, camp_CM, funcion)

arcpy.AddMessage("Clase de entidad agregada")

###################################################################################
# CALCULAR INDICE DE CALIDAD DE VIDA POR COMUNA

# AGREGA EL CAMPO DE LOS INDICES A LA CAPA DE LA COMUNA
agregarCampo(inpFt, agrega_cl, campo_comun, campo_comun, dimensiones[0], campos_agregados)
agregarCampo(inpFt, agrega_SC, campo_comun, campo_comun, dimensiones[1], campos_agregados)
agregarCampo(inpFt, agrega_VE, campo_comun, campo_comun, dimensiones[2], campos_agregados)
agregarCampo(inpFt, agrega_CM, campo_comun, campo_comun, dimensiones[3], campos_agregados)

# CREA UN NUEVO CAMPO
campo_final = "ICV"
crearCampo(inpFt,campo_final,dimensiones)

# CALCULA EL INDICE DE CALIDAD DE VIDA DE ACUERDOA LOS CAMPOS AGREGADOS
funcion = funcion = "(!{}!*{}+!{}!*{}+!{}!*{}+!{}!*{})*100".format(dimensiones[0],pond_arreglado[0],dimensiones[1],pond_arreglado[1],dimensiones[2],pond_arreglado[2],
    dimensiones[3],pond_arreglado[3])
calcularCampo(inpFt,campo_final,funcion)

# # AGREGA LA CLASE DE ENTIDAD AL DATASET DE SALIDA Y BORRA LOS CAMPOS AGREGADOS

nom_final = "ICV_comuna"

agrega_ICV = entidadAentidad(inpFt, outDir, nom_final, dimensiones)

# ELIMINA LAS CAPAS TEMPORALES CREADAS
eliminar(eliminar_capas)

capas_importantes = [nom_cl,nom_CM,nom_csc,nom_ve,nom_final]
for i in capas_importantes:
    lugar = "{}\\{}".format(outDir,i)
    aprxMap.addDataFromPath(lugar)
###################################################################################