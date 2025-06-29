from .models import *
from .serializers import *


from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view
import requests 
from django.core import serializers
from django.shortcuts import render

from requests.exceptions import HTTPError


@api_view(['GET'])
def listar_productosTercero(request):    
    listaProductosTercero = ProductosTerceros.objects.all()
    serializer = ProductoTerceroSerializer(listaProductosTercero, many=True)
    return Response(serializer.data)


@api_view(['GET']) 
def obtener_producto(request,producto_id):
    productos = ProductosTerceros.objects.all()
    producto = productos.get(id=producto_id)   
    serializer = ProductoTerceroSerializer(producto)
    return Response(serializer.data)



@api_view(['POST'])
def crear_producto_tercero(request):
    
    productoTercero = ProductoTerceroCreateSerializer(data=request.data)
    
    if productoTercero.is_valid():
        try:
            productoTercero.save()
            return Response("Creado producto tercero")
        
        except serializers.ValidationError as error:
            return Response(
                error, status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as error:
            return Response(
                error, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        
        
        
    else:
        return Response(
            productoTercero.errors, status=status.HTTP_400_BAD_REQUEST
        )
        
@api_view(["PATCH"])   
def editar_nombre_producto_tercero(request, producto_id):
    producto = ProductosTerceros.objects.get(id=producto_id)
    
    productoSerializer = ProductoTerceroActualizarSerializer(
        producto, data=request.data, partial=True #partial: permite que puedas cambiar el valor de un atributo
    )
    if productoSerializer.is_valid():
        try:
            productoSerializer.save()
            return Response("Producto editado correctamente")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(
            productoSerializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
        


# @api_view(["DELETE"])
# def eliminar_producto(request, producto_id):
#     producto = ProductosTerceros.objects.get(id=producto_id)
#     try:
#         producto.delete()
#         return Response("producto eliminado")
#     except Exception as error:
#         return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def eliminar_producto(request, producto_id):
    producto = ProductosTerceros.objects.get(id=producto_id)
    # Verifica si el usuario autenticado es el creador
    if producto.vendedor != request.user:
        return Response(
            {"error": "No tienes permiso para eliminar este producto."},
            status=status.HTTP_403_FORBIDDEN
        )
    try:
        producto.delete()
        return Response("producto eliminado")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)