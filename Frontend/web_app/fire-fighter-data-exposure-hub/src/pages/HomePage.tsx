import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ChevronDown } from 'lucide-react'
import { ROUTES } from '@/constants/routes'
import { cn } from '@/utils/cn'

const faqs = [
  {
    q: 'What is the Firefighter Safety Data Hub?',
    a: 'It is a proof-of-concept platform for collecting structured firefighter exposure-related information and making that data available for researcher review and export.',
  },
  {
    q: 'What data does the platform handle?',
    a: 'The current application supports firefighter accounts, fire-event records, PPE information, smoke-sampler measurements, location history, and researcher-facing tables and CSV exports.',
  },
  {
    q: 'Who uses the researcher dashboard?',
    a: 'The dashboard is designed for authorized researcher accounts that need to review structured records submitted through the firefighter application.',
  },
  {
    q: 'Does the local demo require AWS?',
    a: 'No. The evaluation setup runs locally with Docker Compose, SQLite, console-based email verification, and local file storage. No AWS account or cloud credentials are required.',
  },
  {
    q: 'Can researchers export data?',
    a: 'Yes. The dashboard includes CSV-oriented export endpoints for supported datasets so records can be used in later analysis workflows.',
  },
  {
    q: 'How do I run the firefighter app?',
    a: 'Start the backend and dashboard with Docker Compose, then run the included Flutter application in Chrome. The exact commands are documented in the project README.',
  },
] as const

export default function HomePage() {
  const [openId, setOpenId] = useState<number | null>(0)

  const scrollToFaq = () => {
    document.getElementById('faq')?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    if (window.location.hash === '#faq') {
      scrollToFaq()
    }
  }, [])

  return (
    <div>
      <section className="flex min-h-[calc(100svh-4rem)] flex-col justify-center bg-gradient-to-b from-blue-50 to-white px-4 py-16 dark:from-gray-900 dark:to-gray-800">
        <div className="mx-auto max-w-4xl text-center">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl dark:text-white">
            Firefighter exposure data, organized for research
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-lg text-gray-600 dark:text-gray-300">
            Review structured firefighter event, PPE, smoke-sampler, and location data through a
            researcher-facing dashboard connected to the same FastAPI backend used by the field app.
          </p>
          <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
            <Link
              to={ROUTES.register}
              className="rounded-lg bg-primary px-6 py-3 font-semibold text-white hover:bg-primary-hover"
            >
              Researcher Registration
            </Link>
            <button
              type="button"
              onClick={scrollToFaq}
              className="rounded-lg border border-gray-300 bg-white px-6 py-3 font-semibold text-gray-800 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-900 dark:text-gray-100 dark:hover:bg-gray-800"
            >
              Learn More
            </button>
          </div>
        </div>
      </section>

      <section id="faq" className="mx-auto max-w-3xl px-4 py-16 sm:px-6">
        <h2 className="text-center text-3xl font-bold text-gray-900 dark:text-white">
          Frequently asked questions
        </h2>
        <div className="mt-10 space-y-3">
          {faqs.map((item, index) => {
            const open = openId === index
            return (
              <div
                key={item.q}
                className="overflow-hidden rounded-xl border border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-900"
              >
                <button
                  type="button"
                  className="flex w-full items-center justify-between gap-4 px-4 py-4 text-left text-base font-semibold text-gray-900 dark:text-white"
                  aria-expanded={open}
                  onClick={() => setOpenId(open ? null : index)}
                >
                  {item.q}
                  <ChevronDown
                    className={cn(
                      'size-5 shrink-0 text-gray-500 transition-transform duration-300',
                      open && 'rotate-180'
                    )}
                    aria-hidden
                  />
                </button>
                <div
                  className={cn(
                    'grid transition-all duration-300',
                    open ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0'
                  )}
                >
                  <div className="min-h-0 overflow-hidden">
                    <p className="px-4 pb-4 text-sm leading-relaxed text-gray-600 dark:text-gray-300">
                      {item.a}
                    </p>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </section>
    </div>
  )
}
