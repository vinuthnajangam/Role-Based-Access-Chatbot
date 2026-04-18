import { Suspense } from "react"
import ChatInterface from "@/components/chat-interface"

function DashboardFallback() {
    return (
        <div className="flex h-screen w-full items-center justify-center bg-black">
            <div className="animate-pulse text-gray-400 text-lg">Loading Dashboard...</div>
        </div>
    )
}

export default function DashboardPage() {
    return (
        <Suspense fallback={<DashboardFallback />}>
            <ChatInterface />
        </Suspense>
    )
}
