#!/usr/bin/env python2
# -*- coding: utf-8 -*-

############################################################################
# NAME:		shp_gk_2_utm
# AUTOR:	Christopher Barron
# ZWECK:	Dieses Skript transformiert Shapes von DHDN3/Gauß-Krüger 
#			nach etrs89/UTM mit Hilfe von ArcPy.
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

# Basisverzeichnis festlegen
input_dir = r"C:\gk_transform_to_utm\dhdn"

# Name der benutzerdefinierten Transformation
custum_trans = "dhdn3_utm_BW"

#Textfile
text = input_dir + "\zusammenfassung_shp.txt"
outFile = open(text,"w")

try:
	# Wandere durch Basisverzeichnis und alle seiner Sub-Verzeichnisse
	for (path, dirs, files) in os.walk(input_dir):
		
		# Schleife durch Dateien
		for shp in files:
		
			# Nur Shapfefiles berücksichtigen die zudem in DHDN3 vorliegen
			if shp.endswith(".shp") and (arcpy.Describe(path + "\\" + shp).SpatialReference).name == "DHDN_3_Degree_Gauss_Zone_3": 
				
				print "Transformiere " + shp + " unter: " + path
				shp_utm = shp.replace(".","_utm.")
				
				# ArcGIS Projektion mit spezifischer Transformationsmethode für BW
				arcpy.Project_management(path+"/"+shp,path+"/"+shp_utm,out_coor_system="PROJCS['ETRS_1989_UTM_Zone_32N',GEOGCS['GCS_ETRS_1989',DATUM['D_ETRS_1989',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',9.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",transform_method=custum_trans,in_coor_system="PROJCS['DHDN_3_Degree_Gauss_Zone_3',GEOGCS['GCS_Deutsches_Hauptdreiecksnetz',DATUM['D_Deutsches_Hauptdreiecksnetz',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',3500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',9.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]")
				
				# Erstellt einen Eintrag mit dem Pfad des Shapes in der Text-Datei
				line = str(path + "\\" + shp) + "\n" 
				outFile.write(line)

				print(arcpy.GetMessages()) + "\n"
			
			# Eintrag in Text-Datei, wenn Shapefile aufgrund einer anderen Projektion nicht transformiert wurde
			elif shp.endswith(".shp") and (arcpy.Describe(path + "\\" + shp).SpatialReference).name != "DHDN_3_Degree_Gauss_Zone_3":
				line = "NICHT TRANSFORMIERT! " + str(path + "\\" + shp) + " liegt in " + (arcpy.Describe(path + "\\" + shp).SpatialReference).name + " vor. \n" 
				outFile.write(line)
	
	print "Transformation abgeschlossen"
	
	outFile.write("\n")
	
	# Liste aller MXDs anfertigen
	print "Starte Auflistung aller MXDs"
	for (path, dirs, files) in os.walk(input_dir):
		for mxd in files:
			if mxd.endswith(".mxd"):
				line = str(path + "\\" + mxd) + "\n" 
				outFile.write(line)
	
	# Textdokument schließen
	outFile.close()
	
# Fehlermeldung
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
    
except Exception as ex:
    print(ex.args[0])
