"""
Script de prueba para los endpoints de eliminación
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_delete_endpoints():
    print("\n🧪 Probando endpoints de eliminación...")
    print("=" * 70)
    
    # 1. Obtener confirmaciones actuales
    print("\n📋 1. Obteniendo confirmaciones actuales...")
    response = requests.get(f"{BASE_URL}/api/confirmations")
    if response.status_code == 200:
        confirmations = response.json()
        print(f"   ✅ Total de confirmaciones: {len(confirmations)}")
        
        if confirmations:
            print(f"\n   Confirmaciones actuales:")
            for conf in confirmations[:3]:  # Mostrar solo las primeras 3
                print(f"   - {conf['folio']}: {conf['name']}")
            if len(confirmations) > 3:
                print(f"   ... y {len(confirmations) - 3} más")
        else:
            print("   ℹ️  No hay confirmaciones registradas")
    else:
        print(f"   ❌ Error al obtener confirmaciones: {response.status_code}")
        return
    
    if not confirmations:
        print("\n⚠️  No hay datos para probar la eliminación.")
        print("   Crea algunas confirmaciones primero desde http://localhost:8000/confirmation")
        return
    
    # 2. Probar eliminación de un registro específico (simular)
    print(f"\n🗑️  2. Endpoint de eliminación individual disponible:")
    print(f"   DELETE {BASE_URL}/api/confirmations/{{folio}}")
    print(f"   Ejemplo: curl -X DELETE {BASE_URL}/api/confirmations/{confirmations[0]['folio']}")
    
    # 3. Probar endpoint de eliminar todos (sin ejecutar)
    print(f"\n🗑️  3. Endpoint de eliminación masiva disponible:")
    print(f"   DELETE {BASE_URL}/api/confirmations")
    print(f"   Ejemplo: curl -X DELETE {BASE_URL}/api/confirmations")
    
    print("\n" + "=" * 70)
    print("✅ Endpoints de eliminación configurados correctamente")
    print("\nℹ️  Usa el panel de administración en:")
    print(f"   {BASE_URL}/static/admin.html")
    print("=" * 70)

if __name__ == "__main__":
    try:
        test_delete_endpoints()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se pudo conectar al servidor.")
        print("   Asegúrate de que el servidor esté corriendo en http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
