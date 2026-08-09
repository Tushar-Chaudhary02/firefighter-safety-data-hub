const sections = [
  {
    title: 'Structured data capture',
    body: 'Firefighter-facing workflows collect event, PPE, smoke-sampler, and location information in consistent formats instead of leaving related records scattered across separate notes or files.',
  },
  {
    title: 'Shared application backend',
    body: 'A FastAPI service validates requests, handles authentication, persists records, and provides the API contract used by both the Flutter field application and the React researcher dashboard.',
  },
  {
    title: 'Researcher access',
    body: 'Authorized researcher accounts can review supported datasets through dashboard tables and use CSV-oriented exports for later analysis workflows.',
  },
] as const

export default function AboutUsPage() {
  return (
    <div>
      <section className="bg-gradient-to-r from-primary to-primary-hover px-4 py-16 text-white sm:px-6">
        <div className="mx-auto max-w-4xl text-center">
          <h1 className="text-4xl font-bold">About the Project</h1>
          <p className="mx-auto mt-4 max-w-2xl text-blue-100">
            The Firefighter Safety Data Hub is a proof-of-concept application for organizing
            firefighter exposure-related information and making structured records easier to review.
          </p>
        </div>
      </section>

      <section className="mx-auto grid max-w-6xl gap-10 px-4 py-16 lg:grid-cols-2 lg:items-start lg:px-6">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Purpose</h2>
        <div className="space-y-6 text-gray-700 dark:text-gray-300">
          <p>
            Firefighter exposure information can span incident details, protective equipment,
            passive-sampler measurements, and location records. The project brings these related
            workflows into one system so information can be captured consistently and retrieved later.
          </p>
          <p>
            The application has two user-facing interfaces: a Flutter app for firefighter data entry
            and a React dashboard for researcher review. Both communicate with a modular FastAPI
            backend, which keeps authentication, validation, database access, and export logic out of
            the client interfaces.
          </p>
          <p>
            For course evaluation, the project is configured as a local-first demonstration. Docker
            Compose starts the backend and researcher dashboard, SQLite provides local persistence,
            and console-based verification replaces external email services so the project can be run
            without cloud credentials.
          </p>
        </div>
      </section>

      <section className="bg-gray-50 px-4 py-16 dark:bg-gray-900 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <h2 className="text-center text-3xl font-bold text-gray-900 dark:text-white">
            Core Design Goals
          </h2>
          <div className="mt-10 grid gap-6 md:grid-cols-3">
            {sections.map((section) => (
              <div
                key={section.title}
                className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-950"
              >
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  {section.title}
                </h3>
                <p className="mt-3 text-sm leading-relaxed text-gray-600 dark:text-gray-300">
                  {section.body}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
