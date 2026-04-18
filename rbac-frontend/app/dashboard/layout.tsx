import Sidebar from "@/components/sidebar"

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex h-screen overflow-hidden bg-black text-white">
            <Sidebar />
            <main className="flex-1 overflow-auto relative">
                <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10 pointer-events-none" />
                {children}
            </main>
        </div>
    )
}
