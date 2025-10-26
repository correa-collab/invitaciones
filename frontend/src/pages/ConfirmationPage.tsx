import React from 'react'

export function ConfirmationPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-yellow-50 to-yellow-100">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-6 border border-yellow-200">
        <div className="text-center mb-6">
          <div className="w-16 h-16 bg-gradient-to-br from-yellow-600 to-yellow-700 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-white font-bold text-xl">UP</span>
          </div>
          <h1 className="text-2xl font-bold text-yellow-800 mb-2">
            Confirmar Asistencia
          </h1>
          <p className="text-gray-600">
            Por favor confirma tu asistencia al evento
          </p>
        </div>
        <div className="space-y-4">
          <button className="w-full bg-gradient-to-r from-yellow-600 to-yellow-700 text-white py-3 px-4 rounded-md hover:from-yellow-700 hover:to-yellow-800 font-medium transition duration-200">
            ✓ Confirmar Asistencia
          </button>
          <button className="w-full bg-gradient-to-r from-gray-500 to-gray-600 text-white py-3 px-4 rounded-md hover:from-gray-600 hover:to-gray-700 font-medium transition duration-200">
            ✗ No Podré Asistir
          </button>
        </div>
      </div>
    </div>
  )
}