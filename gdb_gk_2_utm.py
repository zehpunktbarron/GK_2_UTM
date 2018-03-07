#!/usr/bin/env python2
# -*- coding: utf-8 -*-

############################################################################
# NAME:		gdb_gk_2_utm
# AUTOR:	Christopher Barron
# ZWECK:	Dieses Skript transformiert Feature-Classes innerhalb einer Geodatabase
#			von DHDN3/Gauß-Krüger nach etrs89/UTM mit Hilfe von ArcPy.
#
#			BEDINGUNG: 
# 			Das NTv2 Transformations-File für BW von
#			https://www.lgl-bw.de/lgl-internet/opencms/de/05_Geoinformation/Liegenschaftskataster/ETRS89-UTM/index.html
#			muss wie hier beschrieben https://support.esri.com/en/technical-article/000010151
#			vorhanden sein.
#			Ein Basisverzeichnis muss angegeben sein.
#
#			*.gtf: C:\Users\barronc\AppData\Roaming\ESRI\Desktop10.2\ArcToolbox\CustomTransformations -->  %appdata%
#			*.gsb: C:\Program Files (x86)\ArcGIS\Desktop10.2\pedata\ntv2\germany
#############################################################################


# Import der Module
import arcpy, string, os
from arcpy import env

arcpy.env.overwriteOutput = False

# Basisverzeichnis festlegen
input_dir = r"C:\gk_transform_to_utm\dhdn"

# Name der benutzerdefinierten Transformation
custum_trans = "dhdn3_utm_BW"

#Textfile
text = input_dir + "\zusammenfassung_gdb.txt"
outFile = open(text,"w")

try:
	# Wandere durch Basisverzeichnis und alle seiner Sub-Verzeichnisse
	for (path, dirs, files) in os.walk(input_dir):
		
		# Schleife durch Ordner um alle GDBs zu finden
		for gdb in dirs:
			if gdb.endswith(".gdb"):
			
				# GDBs(_utm) neu erstellen
				utm_gdb = gdb.replace(".","_utm.")
				arcpy.CreateFileGDB_management(path, utm_gdb)
				
				# Workspace immer auf die aktuell gefundene GDB setzen 
				arcpy.env.workspace = os.path.join(path, gdb)
				
				try:
					# ListFeatureClasses nutzen um eine Liste aller fcs zu haben 
					for infc in arcpy.ListFeatureClasses():

						# Nur fcs berücksichtigen die in DHDN3 vorliegen
						dsc = arcpy.Describe(infc)
						if dsc.spatialReference.Name != "DHDN_3_Degree_Gauss_Zone_3":
							line = "NICHT TRANSFORMIERT! " + str(arcpy.env.workspace + "\\" + infc) + " liegt in " + (arcpy.Describe(arcpy.env.workspace + "\\" + infc).SpatialReference).name + " vor. \n" 
							outFile.write(line)
							
						else:
							# Pfad zur output fc festlegen
							outfc = os.path.join(path, utm_gdb, infc)
							
							print "\n Transformiere fc " + infc + " unter: " + arcpy.env.workspace
							
							# ArcGIS Projektion mit spezifischer Transformationsmethode für BW
							arcpy.Project_management(infc,outfc,out_coor_system="PROJCS['ETRS_1989_UTM_Zone_32N',GEOGCS['GCS_ETRS_1989',DATUM['D_ETRS_1989',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',9.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",transform_method=custum_trans,in_coor_system="PROJCS['DHDN_3_Degree_Gauss_Zone_3',GEOGCS['GCS_Deutsches_Hauptdreiecksnetz',DATUM['D_Deutsches_Hauptdreiecksnetz',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',3500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',9.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]")
				
							# Erstellt einen Eintrag mit dem Pfad der fc in der Text-Datei
							line = arcpy.env.workspace + "\\" + infc + "\n" 
							outFile.write(line)
							
							# check messages
							print(arcpy.GetMessages())

				# Fehlermeldungen Ebene Feature Class
				except arcpy.ExecuteError:
					print(arcpy.GetMessages(2))
					
				except Exception as ex:
					print(ex.args[0])
			
		# Textdokument schließen
		outFile.close()
				
# Fehlermeldung Ebene GDB
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
    
except Exception as ex:
    print(ex.args[0])