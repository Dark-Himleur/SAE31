#!/usr/bin/python3

###
# Léo Desmarescaux
# 04/10/2022
###

#   Lit les noms d'un fichier et les enregistre au format d'import LDAP

import csv
import unidecode    # Nécessite l'installation de

with open("random_names_fossbytes.csv") as fichierNomsBruts:
	uidNumber = 1500  # Premier uidNumber utilisé
	for nomBrut in csv.reader(fichierNomsBruts):
		try:
			prenom = nomBrut[0].split(" ")[0]
			nom = nomBrut[0].split(" ")[1:]
			nom = " ".join(nom)
            # print("prenom : " + prenom)
            # print("nom : " + nom + "\n")

			with open("utilisateurs.ldif", "a") as fichierUtilisateurs:
                # Nom d'utilisateur au format ldesm par ex
				uid = unidecode.unidecode(
				(prenom[0] + nom[:4]).replace(" ", "").lower())
                # Mot de passe S5CUR1ZÉ de la session : Ldesm1
				mdp = uid[0].upper() + uid[1:5] + "1"

                # print(uid)
                # print(mdp)
                # print()
                # uid : ldesm, ou : groupe, dc : nom entreprise
				donnees = "dn: ou=Employe,dc=polyled,dc=com\n"
				donnees += "objectClass: organizationalUnit\n"
				donnees += "ou: Employe\n"
				donnees += "\n"
				donnees += "dn: uid=" + uid + ",ou=Employe,dc=polyled,dc=com\n"
				donnees += "objectClass: inetOrgPerson\n"
				donnees += "objectClass: posixGroup\n"
				donnees += "objectClass: shadowAccount\n"
				donnees += "sn: "+ nom + "\n"
				donnees += "givenName: "+ prenom + "\n"
				donnees += "cn: " + prenom + " " + nom + "\n"
				donnees += "displayName: " + prenom + " " + nom + "\n"
				donnees += "gecos: " + unidecode.unidecode(prenom) + " " + unidecode.unidecode(nom) + "\n"
				donnees += "uid: " + uid + "\n"
				donnees += "uidNumber: " + str(uidNumber) + "\n"
				donnees += "gidNumber: 100\n"
				donnees += "homeDirectory: /home/" + uid + "\n"     # Répertoire utilisateur : /home/ldesm
				donnees += "loginShell: /bin/bash\n"
				donnees += "userPassword: " + mdp + "\n"    # Écriture du mot de passe en clair
				donnees += "\n"
				fichierUtilisateurs.write(donnees)
			uidNumber += 1  # UidNumber de d'utilisateur suivant
		except:
			print("Erreur : L'utilisateur " + nom + " n'a pas été ajouté.")
