# -*- coding: utf-8 -*-
"""Extra validations module"""
import re


def validate_cedula_ruc(cedula_ruc, tipo=None):
    """Validate the CI/RUC of a partner

    Args:
        cedula_ruc (char): [the CI/RUC to validate]

    Returns:
        True: if name is correct
        False: Otherwise
    """
    if tipo:
        tipo=tipo.replace('Cédula','cedula')
        tipo=tipo.replace('RUC','ruc')
        if cedula_ruc=='9999999999999': #CFINAL
            return True
        if tipo == 'cedula':
            if len(cedula_ruc) != 10:
                return False
            elif tipo=='ruc':
                if len(cedula_ruc) != 13:
                    return False                
    pattern = re.compile('^[0-9a-zA-Z]{3,13}$')
    if not bool(re.match(pattern, cedula_ruc)):
        return False
    if len(cedula_ruc) == 13 and cedula_ruc[-3:] != '001':
        return False
    numero_provincias = 30
    if cedula_ruc == '' or not cedula_ruc or not cedula_ruc or cedula_ruc in ['0000000000', '0000000000000']:
        return False
    if int(cedula_ruc[0:2]) > numero_provincias:
        return False
    # primero verifico que sean numeros de 10 0 13 de tamanio
    if cedula_ruc and cedula_ruc.isdigit() and (len(cedula_ruc) == 10 or len(cedula_ruc) == 13):
        if len(cedula_ruc) == 13:  # si es un ruc el utlimo numero de 001 no puede ser 0
            sucursal = cedula_ruc[10:]
            if int(sucursal[2]) <= 0:
                return False
        # separo la parte de la cedula en una lista
        ced_ruc = []
        for index in range(len(cedula_ruc)):
            ced_ruc.append(int(cedula_ruc[index]))
        cedula_ruc = ced_ruc
        resultado = 0
        if cedula_ruc[2] == 9:  # extranjero
            coeficientes = [4, 3, 2, 7, 6, 5, 4, 3, 2]
            pos_verificador = 9
            cedula = list(cedula_ruc[:9])
            modulo = 11
            for j in range(0, len(coeficientes)):
                resultado += int(cedula[j]) * coeficientes[j]
        elif cedula_ruc[2] == 6 and len(cedula_ruc) == 13:  # RUC PUBLICO
            coeficientes = [3, 2, 7, 6, 5, 4, 3, 2]
            pos_verificador = 8
            cedula = list(cedula_ruc[:8])
            modulo = 11
            for j in range(0, len(coeficientes)):
                resultado += int(cedula[j]) * coeficientes[j]
        elif cedula_ruc[2] < 6 or (cedula_ruc[2] == 6 and len(ced_ruc) == 10):  # PERSONA NATURAL o JURIDICA
            coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
            pos_verificador = 9
            cedula = list(cedula_ruc[:9])
            modulo = 10
            for j in range(0, len(coeficientes)):
                valor = int(cedula[j]) * coeficientes[j]
                if valor >= 10:
                    str1 = str(valor)
                    suma = int(str1[0]) + int(str1[1])
                    resultado += suma
                else:
                    resultado += valor
        else:
            return False
        # ahora comprubo segun los algoritmos
        residuo = resultado % modulo
        if residuo != 0:
            verificador = modulo - residuo
        else:
            verificador = residuo
        if verificador == int(cedula_ruc[pos_verificador]):
            return True
        else:
            if cedula_ruc[2] in [6, 9]:  # hay que hacer una validacion adicional por la descordinacion de numeros entre registro civil y SRI
                if len(cedula_ruc) in [10, 13]:
                    return True
            return False
    elif not cedula_ruc.isdigit():
        if cedula_ruc[0] == 'P':
            return True
        else:
            return False
    else:
        return False
    return True
