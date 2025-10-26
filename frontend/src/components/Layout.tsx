import React, { ReactNode } from 'react'

interface LayoutProps {
  children: ReactNode
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <div className="w-10 h-10 bg-gradient-to-br from-yellow-600 to-yellow-700 rounded-lg flex items-center justify-center mr-3">
                <span className="text-white font-bold text-lg">UP</span>
              </div>
              <h1 className="text-xl font-semibold text-yellow-800">
                Sistema de Invitaciones
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <a href="/dashboard" className="text-yellow-700 hover:text-yellow-800 font-medium">
                Dashboard
              </a>
              <a href="/events" className="text-yellow-700 hover:text-yellow-800 font-medium">
                Eventos
              </a>
              <a href="/login" className="bg-gradient-to-r from-yellow-600 to-yellow-700 text-white px-4 py-2 rounded-md hover:from-yellow-700 hover:to-yellow-800 font-medium">
                Login
              </a>
            </div>
          </div>
        </div>
      </nav>
      
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  )
}