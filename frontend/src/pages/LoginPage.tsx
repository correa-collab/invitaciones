import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import axios, { type AxiosError } from 'axios'
import toast from 'react-hot-toast'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

type LoginFormValues = {
  username: string
  password: string
}

export function LoginPage() {
  const navigate = useNavigate()
  const {
    register,
    handleSubmit,
    formState: { isSubmitting },
  } = useForm<LoginFormValues>({
    defaultValues: { username: '', password: '' },
  })

  const onSubmit = async (values: LoginFormValues) => {
    const formData = new URLSearchParams()
    formData.append('username', values.username)
    formData.append('password', values.password)

    try {
      const { data } = await axios.post(`${API_URL}/api/auth/token`, formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })

      localStorage.setItem('access_token', data.access_token)
      toast.success('Sesión iniciada correctamente')
      navigate('/dashboard')
    } catch (error) {
      const message =
        (error as AxiosError<{ detail?: string }>).response?.data?.detail ??
        'No pudimos iniciar sesión, verifica tus datos.'
      toast.error(message)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-center text-gray-900 mb-6">
          Iniciar Sesión
        </h2>
        <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Usuario o Email
            </label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="usuario"
              {...register('username', { required: true })}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Contraseña
            </label>
            <input
              type="password"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="••••••••"
              {...register('password', { required: true })}
            />
          </div>
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 transition duration-200 disabled:opacity-60"
          >
            {isSubmitting ? 'Ingresando...' : 'Iniciar Sesión'}
          </button>
        </form>
      </div>
    </div>
  )
}
