import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation } from '@tanstack/react-query'
import { z } from 'zod'
import toast from 'react-hot-toast'
import { Container, Database, Terminal } from 'lucide-react'
import { submitContact } from '@/api/contact.api'
import { LoadingSpinner } from '@/components/shared/LoadingSpinner'
import { cn } from '@/utils/cn'

const schema = z.object({
  name: z.string().min(1, 'Required'),
  email: z.string().min(1, 'Required').email('Valid email'),
  subject: z.string().min(1, 'Required'),
  message: z.string().min(1, 'Required'),
})

type Values = z.infer<typeof schema>

export default function ContactPage() {
  const [sent, setSent] = useState(false)
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<Values>({
    resolver: zodResolver(schema),
    defaultValues: { name: '', email: '', subject: '', message: '' },
  })

  const mutation = useMutation({
    mutationFn: submitContact,
    onSuccess: () => setSent(true),
    onError: () => toast.error('Could not send message. Please try again.'),
  })

  if (sent) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6">
        <div className="rounded-2xl border border-gray-200 bg-white p-10 text-center shadow-sm dark:border-gray-700 dark:bg-gray-900">
          <p className="text-lg font-semibold text-gray-900 dark:text-white">
            Request submitted to the local demo backend.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="mx-auto grid max-w-6xl gap-10 px-4 py-16 lg:grid-cols-2 lg:px-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Contact us</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Use this form to exercise the project&apos;s local contact-request API.
        </p>
        <form
          onSubmit={handleSubmit((v) => mutation.mutate(v))}
          className="mt-8 flex flex-col gap-4"
          noValidate
        >
          <div className="flex flex-col gap-2">
            <label htmlFor="c-name" className="text-sm font-medium text-gray-700 dark:text-gray-200">
              Name
            </label>
            <input
              id="c-name"
              className={cn(
                'rounded-lg border px-3 py-2 dark:bg-gray-900 dark:text-white',
                errors.name ? 'border-danger' : 'border-gray-300 dark:border-gray-600'
              )}
              {...register('name')}
            />
            {errors.name && <p className="text-sm text-danger">{errors.name.message}</p>}
          </div>
          <div className="flex flex-col gap-2">
            <label htmlFor="c-email" className="text-sm font-medium text-gray-700 dark:text-gray-200">
              Email
            </label>
            <input
              id="c-email"
              type="email"
              className={cn(
                'rounded-lg border px-3 py-2 dark:bg-gray-900 dark:text-white',
                errors.email ? 'border-danger' : 'border-gray-300 dark:border-gray-600'
              )}
              {...register('email')}
            />
            {errors.email && <p className="text-sm text-danger">{errors.email.message}</p>}
          </div>
          <div className="flex flex-col gap-2">
            <label htmlFor="c-subject" className="text-sm font-medium text-gray-700 dark:text-gray-200">
              Subject
            </label>
            <input
              id="c-subject"
              className={cn(
                'rounded-lg border px-3 py-2 dark:bg-gray-900 dark:text-white',
                errors.subject ? 'border-danger' : 'border-gray-300 dark:border-gray-600'
              )}
              {...register('subject')}
            />
            {errors.subject && <p className="text-sm text-danger">{errors.subject.message}</p>}
          </div>
          <div className="flex flex-col gap-2">
            <label htmlFor="c-msg" className="text-sm font-medium text-gray-700 dark:text-gray-200">
              Message
            </label>
            <textarea
              id="c-msg"
              rows={5}
              className={cn(
                'rounded-lg border px-3 py-2 dark:bg-gray-900 dark:text-white',
                errors.message ? 'border-danger' : 'border-gray-300 dark:border-gray-600'
              )}
              {...register('message')}
            />
            {errors.message && <p className="text-sm text-danger">{errors.message.message}</p>}
          </div>
          <button
            type="submit"
            disabled={mutation.isPending}
            className="inline-flex items-center justify-center gap-2 rounded-lg bg-primary px-4 py-2.5 font-medium text-white hover:bg-primary-hover disabled:opacity-60"
          >
            {mutation.isPending && <LoadingSpinner className="size-4 border-white border-t-transparent" />}
            Send message
          </button>
        </form>
      </div>
      <div className="space-y-4">
        <div className="flex gap-4 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-700 dark:bg-gray-900">
          <Container className="mt-1 size-6 shrink-0 text-primary" aria-hidden />
          <div>
            <p className="font-semibold text-gray-900 dark:text-white">Local demonstration</p>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              The default course setup runs locally through Docker Compose and does not send this form to an external service.
            </p>
          </div>
        </div>
        <div className="flex gap-4 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-700 dark:bg-gray-900">
          <Terminal className="mt-1 size-6 shrink-0 text-primary" aria-hidden />
          <div>
            <p className="font-semibold text-gray-900 dark:text-white">Request visibility</p>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Successful contact requests are accepted by the FastAPI endpoint and summarized in the backend console for testing.
            </p>
          </div>
        </div>
        <div className="flex gap-4 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-700 dark:bg-gray-900">
          <Database className="mt-1 size-6 shrink-0 text-primary" aria-hidden />
          <div>
            <p className="font-semibold text-gray-900 dark:text-white">No external dependency</p>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              AWS credentials, cloud email, and external support systems are not required for the local evaluator workflow.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
