export function EventsPage() {
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Mis Eventos</h1>
        <button className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
          Nuevo Evento
        </button>
      </div>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <p className="text-gray-500 text-center py-8">
          No hay eventos creados aún. ¡Crea tu primer evento!
        </p>
      </div>
    </div>
  )
}