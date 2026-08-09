import { Code2, Container, Monitor } from 'lucide-react'

export default function DownloadAppPage() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-16 sm:px-6">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white">Run the Firefighter App</h1>
        <p className="mx-auto mt-3 max-w-2xl text-gray-600 dark:text-gray-300">
          The firefighter application is included in this project repository and is intended to be
          run locally for the course demonstration. No App Store or Play Store installation is
          required.
        </p>
      </div>

      <div className="mt-12 grid gap-6 md:grid-cols-3">
        <div className="rounded-2xl border border-gray-200 bg-white p-7 shadow-sm dark:border-gray-700 dark:bg-gray-900">
          <Container className="size-10 text-primary" aria-hidden />
          <h2 className="mt-4 font-semibold text-gray-900 dark:text-white">1. Start services</h2>
          <p className="mt-2 text-sm leading-relaxed text-gray-600 dark:text-gray-300">
            From the project root, run <code>docker compose up --build</code> to start the FastAPI
            backend and researcher dashboard.
          </p>
        </div>
        <div className="rounded-2xl border border-gray-200 bg-white p-7 shadow-sm dark:border-gray-700 dark:bg-gray-900">
          <Code2 className="size-10 text-primary" aria-hidden />
          <h2 className="mt-4 font-semibold text-gray-900 dark:text-white">2. Get Flutter packages</h2>
          <p className="mt-2 text-sm leading-relaxed text-gray-600 dark:text-gray-300">
            Open a second terminal in the Flutter project folder and run <code>flutter pub get</code>.
          </p>
        </div>
        <div className="rounded-2xl border border-gray-200 bg-white p-7 shadow-sm dark:border-gray-700 dark:bg-gray-900">
          <Monitor className="size-10 text-primary" aria-hidden />
          <h2 className="mt-4 font-semibold text-gray-900 dark:text-white">3. Launch in Chrome</h2>
          <p className="mt-2 text-sm leading-relaxed text-gray-600 dark:text-gray-300">
            Run <code>flutter run -d chrome</code>. The app automatically connects to the local
            backend on port 8000.
          </p>
        </div>
      </div>

      <div className="mx-auto mt-12 max-w-3xl rounded-2xl border border-gray-200 bg-gray-50 p-6 dark:border-gray-700 dark:bg-gray-900">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Local prerequisites</h2>
        <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-gray-700 dark:text-gray-300">
          <li>Docker Desktop, or Docker Engine with Docker Compose</li>
          <li>Flutter SDK with web support</li>
          <li>Google Chrome</li>
        </ul>
        <p className="mt-4 text-sm text-gray-600 dark:text-gray-300">
          See the root <code>README.md</code> for the complete quick-start instructions and local
          verification workflow.
        </p>
      </div>
    </div>
  )
}
