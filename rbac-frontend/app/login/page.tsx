import LoginForm from "@/components/login-form"

export default function LoginPage() {
    return (
        <div className="flex min-h-screen w-full items-center justify-center bg-black relative overflow-hidden">
            {/* Background Gradients */}
            <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-slate-900 via-zinc-900 to-black z-0" />
            <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-blue-600/20 blur-[120px]" />
            <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-purple-600/20 blur-[120px]" />

            {/* Content */}
            <div className="relative z-10 w-full max-w-md p-4 animate-in fade-in zoom-in duration-500">
                <LoginForm />
            </div>

            {/* Floating Info Button */}
            <a
                href="/presentation.html"
                target="_blank"
                rel="noopener noreferrer"
                className="absolute bottom-6 right-6 z-50 flex items-center gap-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white px-5 py-3 rounded-full shadow-lg shadow-blue-500/30 transition-all hover:scale-105 hover:shadow-blue-500/50"
            >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10" /><path d="M12 16v-4" /><path d="M12 8h.01" /></svg>
                <span className="font-semibold text-sm">Detailed Info</span>
            </a>
        </div>
    )
}
