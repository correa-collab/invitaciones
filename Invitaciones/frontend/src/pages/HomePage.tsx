export function HomePage() {
  return (
    <div className="text-center">
      <div className="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Bienvenido al Sistema de Invitaciones
        </h1>
        <p className="text-gray-600 mb-6">
          Gestiona tus eventos y confirmaciones de manera fácil y eficiente
        </p>
        <div className="space-y-4">
          <a 
            href="/dashboard"
            className="block w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 transition duration-200"
          >
            Ir al Dashboard
          </a>
          <a 
            href="/login"
            className="block w-full border border-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-50 transition duration-200"
          >
            Iniciar Sesión
          </a>
        </div>
      </div>
    </div>
  )
}