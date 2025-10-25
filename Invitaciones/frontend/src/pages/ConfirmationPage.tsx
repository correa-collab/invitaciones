export function ConfirmationPage() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold text-center mb-6">
          Confirmar Asistencia
        </h1>
        <p className="text-gray-600 text-center mb-6">
          Por favor confirma tu asistencia al evento
        </p>
        <div className="space-y-4">
          <button className="w-full bg-green-600 text-white py-3 px-4 rounded-md hover:bg-green-700">
            ✓ Confirmar Asistencia
          </button>
          <button className="w-full bg-red-600 text-white py-3 px-4 rounded-md hover:bg-red-700">
            ✗ No Podré Asistir
          </button>
        </div>
      </div>
    </div>
  )
}