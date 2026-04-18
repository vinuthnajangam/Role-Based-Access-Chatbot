"use client"

import { useState, useEffect } from "react"
import { useSearchParams, useRouter } from "next/navigation"
import api from "@/lib/api"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Send, Bot, User, FileText, BarChart3, Zap, FileSearch } from "lucide-react"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface Metrics {
    documents_retrieved: number
    avg_similarity: number
    llm_enabled: boolean
    model: string | null
    context_tokens: number
}

interface Message {
    role: "user" | "bot"
    content: string
    sources?: any[]
    metrics?: Metrics
}

export default function ChatInterface() {
    const [query, setQuery] = useState("")
    const [messages, setMessages] = useState<Message[]>([
        { role: "bot", content: "Hello! I am your RBAC-secured assistant. Select a department context and ask me anything." }
    ])
    const [loading, setLoading] = useState(false)
    const [dept, setDept] = useState("general")
    const [username, setUsername] = useState<string | null>(null)
    const [userRole, setUserRole] = useState<string | null>(null)
    const searchParams = useSearchParams()
    const router = useRouter()

    // Sync dept with URL query param
    useEffect(() => {
        const queryDept = searchParams.get("dept")
        if (queryDept) {
            setDept(queryDept)
        }
    }, [searchParams])

    // Suggested questions per department - organized by access type
    const suggestedQuestions: Record<string, { authorized: string[], testUnauthorized: string[] }> = {
        finance: {
            authorized: [
                "What is the Q4 2024 revenue?",
                "What was the gross margin in 2024?",
                "What are the vendor costs breakdown?"
            ],
            testUnauthorized: [
                "❌ Test: What is the leave policy?", // HR question
                "❌ Test: What is the weather today?" // Unrelated
            ]
        },
        hr: {
            authorized: [
                "What is the leave policy?",
                "What are the employee benefits?",
                "How does the performance review process work?"
            ],
            testUnauthorized: [
                "❌ Test: What was the Q4 2024 revenue?", // Finance question
                "❌ Test: Tell me a joke" // Unrelated
            ]
        },
        marketing: {
            authorized: [
                "What was the marketing ROI in 2024?",
                "How many new customers were acquired?",
                "What digital campaigns were launched?"
            ],
            testUnauthorized: [
                "❌ Test: What is the employee exit policy?", // HR question
                "❌ Test: Who won the football match?" // Unrelated
            ]
        },
        engineering: {
            authorized: [
                "What is the system architecture?",
                "What technologies are used in production?",
                "What is the deployment process?"
            ],
            testUnauthorized: [
                "❌ Test: What is the marketing budget?", // Marketing question
                "❌ Test: How to cook pasta?" // Unrelated
            ]
        },
        general: {
            authorized: [
                "What is FinSolve Technologies?",
                "What are the company values?",
                "What is the work from home policy?"
            ],
            testUnauthorized: [
                "❌ Test: What is the Q4 revenue?", // Finance question (general users can't access)
                "❌ Test: Give me investment advice" // Unrelated
            ]
        }
    }

    useEffect(() => {
        if (typeof window !== "undefined") {
            setUsername(localStorage.getItem("username"))
            setUserRole(localStorage.getItem("user_role"))
        }
    }, [])

    // Get display name based on role and department
    const getDisplayName = () => {
        if (!userRole) return username || "User"

        const roleMap: Record<string, string> = {
            "c-level": "Admin",
            "finance": "Finance",
            "hr": "HR",
            "marketing": "Marketing",
            "engineering": "Engineering"
        }

        const baseRole = roleMap[userRole.toLowerCase()] || userRole

        // For C-level, show department context
        if (userRole.toLowerCase() === "c-level") {
            const deptMap: Record<string, string> = {
                "finance": "Admin (Finance)",
                "hr": "Admin (HR)",
                "marketing": "Admin (Marketing)",
                "engineering": "Admin (Engineering)",
                "general": "Admin"
            }
            return deptMap[dept] || "Admin"
        }

        return baseRole
    }

    const handleSuggestedClick = (question: string) => {
        setQuery(question)
    }

    const handleSend = async () => {
        if (!query.trim()) return

        const userMsg = { role: "user" as const, content: query }
        setMessages(prev => [...prev, userMsg])
        setQuery("")
        setLoading(true)

        try {
            const res = await api.post(`/query/${dept}`, { query: userMsg.content })
            let { response, results, metrics } = res.data

            // Clean up markdown bolding stars if present (Simple fix for "stars" issue)
            if (response) {
                // Replace **text** with just text to remove the "star star star" appearance
                // The user complained about seeing stars, so we remove the markdown bolding
                response = response.replace(/\*\*/g, '')
            }

            const botMsg = {
                role: "bot" as const,
                content: response || "I couldn't find any relevant documents that you have access to.",
                sources: results || [],
                metrics: metrics
            }
            setMessages(prev => [...prev, botMsg])

        } catch (err: any) {
            console.error(err)
            if (err.response?.status === 403) {
                setMessages(prev => [...prev, { role: "bot", content: "🚫 Access Denied: You do not have permission to search in this department." }])
            } else if (err.response?.status === 401) {
                setMessages(prev => [...prev, { role: "bot", content: "🔐 Session expired. Please log in again." }])
            } else {
                setMessages(prev => [...prev, { role: "bot", content: "❌ Error connecting to server." }])
            }
        } finally {
            setLoading(false)
        }
    }

    // Role-based department access
    const getVisibleDepartments = () => {
        const allDepts = ["finance", "hr", "marketing", "engineering", "general"]
        if (!userRole) return ["general"]

        const role = userRole.toLowerCase()
        if (role === "c-level") return allDepts
        if (role === "employees") return ["general"]

        // Return context specific department + general
        return [role, "general"]
    }

    return (
        <div className="flex flex-col h-full max-w-5xl mx-auto p-4 md:p-8">
            {/* Welcome Header */}
            <div className="mb-6">
                <h1 className="text-2xl md:text-3xl font-bold tracking-tight">
                    Welcome back, <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">{getDisplayName()}</span>
                </h1>
                <p className="text-gray-500 mt-1">What can I help you find across your secure documents today?</p>
                <div className="mt-2 text-xs text-gray-600 bg-blue-500/10 border border-blue-500/20 rounded-lg p-2">
                    💡 <span className="text-blue-400 font-semibold">Note:</span> Admin users have access to ALL departments. Other roles can only access their own department.
                    <span className="text-gray-500"> "General" contains company-wide policies accessible to everyone.</span>
                </div>
            </div>

            {/* Header / Dept Selector */}
            <div className="flex flex-col md:flex-row justify-between items-center mb-4 p-4 bg-white/5 rounded-xl border border-white/10 gap-4">
                <h2 className="text-lg font-semibold flex items-center gap-2">
                    <Bot className="text-blue-500" /> Secure RAG Chat
                </h2>
                <div className="flex gap-2 flex-wrap justify-center">
                    {getVisibleDepartments().map(d => (
                        <Badge
                            key={d}
                            variant={dept === d ? "default" : "outline"}
                            className={`cursor-pointer capitalize hover:bg-blue-600/50 transition-all ${dept === d ? 'bg-blue-600 shadow-lg shadow-blue-500/20' : 'text-gray-400 border-gray-700 hover:border-gray-500'}`}
                            onClick={() => router.push(`/dashboard?dept=${d}`)}
                        >
                            {d}
                        </Badge>
                    ))}
                </div>
            </div>

            {/* Suggested Questions */}
            <div className="mb-4 space-y-3">
                {/* Authorized Questions */}
                <div>
                    <p className="text-xs text-green-400 mb-2 flex items-center gap-1">
                        ✅ Try these authorized questions:
                    </p>
                    <div className="flex flex-wrap gap-2">
                        {suggestedQuestions[dept]?.authorized.map((q, idx) => (
                            <button
                                key={idx}
                                onClick={() => handleSuggestedClick(q)}
                                className="text-xs px-3 py-1.5 bg-green-500/10 hover:bg-green-500/20 border border-green-500/30 hover:border-green-500/50 rounded-full text-green-300 hover:text-green-200 transition-all"
                            >
                                {q}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Test Unauthorized Questions */}
                <div>
                    <p className="text-xs text-red-400 mb-2 flex items-center gap-1">
                        🔒 Test access control (these should be denied):
                    </p>
                    <div className="flex flex-wrap gap-2">
                        {suggestedQuestions[dept]?.testUnauthorized.map((q, idx) => (
                            <button
                                key={idx}
                                onClick={() => handleSuggestedClick(q.replace('❌ Test: ', ''))}
                                className="text-xs px-3 py-1.5 bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 hover:border-red-500/50 rounded-full text-red-300 hover:text-red-200 transition-all"
                            >
                                {q}
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            {/* Chat Area */}
            <ScrollArea className="flex-1 bg-white/5 rounded-xl border border-white/10 p-4 mb-4 backdrop-blur-sm min-h-[400px]">
                <div className="space-y-6">
                    {messages.map((m, i) => (
                        <div key={i} className={`flex gap-3 ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                            {m.role === "bot" && <Avatar className="w-8 h-8"><AvatarFallback className="bg-gradient-to-br from-blue-500 to-indigo-600 text-white text-xs"><Bot size={14} /></AvatarFallback></Avatar>}

                            <div className={`max-w-[85%] space-y-3`}>
                                <div className={`p-4 rounded-2xl shadow-lg ${m.role === "user"
                                    ? "bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-br-sm"
                                    : "bg-white/10 text-gray-100 rounded-bl-sm border border-white/5"
                                    }`}>
                                    <p className="leading-relaxed whitespace-pre-wrap">{m.content}</p>
                                </div>

                                {/* Metrics Panel */}
                                {m.metrics && (
                                    <div className="flex flex-wrap gap-2 px-1">
                                        <div className="flex items-center gap-1.5 text-[10px] text-gray-500 bg-white/5 px-2 py-1 rounded-full">
                                            <FileSearch size={10} className="text-blue-400" />
                                            {m.metrics.documents_retrieved} docs
                                        </div>
                                        <div className="flex items-center gap-1.5 text-[10px] text-gray-500 bg-white/5 px-2 py-1 rounded-full">
                                            <BarChart3 size={10} className="text-green-400" />
                                            {(m.metrics.avg_similarity * 100).toFixed(0)}% match
                                        </div>
                                        {m.metrics.llm_enabled && (
                                            <div className="flex items-center gap-1.5 text-[10px] text-gray-500 bg-white/5 px-2 py-1 rounded-full">
                                                <Zap size={10} className="text-yellow-400" />
                                                {m.metrics.model?.split('/')[1] || 'AI'}
                                            </div>
                                        )}
                                    </div>
                                )}

                                {/* Sources */}
                                {m.sources && m.sources.length > 0 && (
                                    <div className="grid grid-cols-1 gap-2">
                                        {m.sources.slice(0, 3).map((s: any, idx: number) => (
                                            <Card key={idx} className="bg-black/40 border-white/10 p-3 hover:bg-black/60 transition-all hover:border-white/20 cursor-default">
                                                <div className="flex items-center gap-2 mb-1.5">
                                                    <FileText size={12} className="text-blue-400" />
                                                    <span className="text-[10px] font-mono text-blue-300 uppercase tracking-wider">{s.metadata?.department || 'Document'}</span>
                                                    <span className="text-[10px] text-gray-600 ml-auto">
                                                        {((1 - (s.score || 0.5)) * 100).toFixed(0)}% relevant
                                                    </span>
                                                </div>
                                                <p className="text-xs text-gray-400 line-clamp-2 leading-relaxed">{s.content}</p>
                                            </Card>
                                        ))}
                                        {m.sources.length > 3 && (
                                            <p className="text-[10px] text-gray-600 text-center">+{m.sources.length - 3} more sources</p>
                                        )}
                                    </div>
                                )}
                            </div>

                            {m.role === "user" && <Avatar className="w-8 h-8"><AvatarFallback className="bg-gradient-to-br from-purple-500 to-pink-600 text-white text-xs"><User size={14} /></AvatarFallback></Avatar>}
                        </div>
                    ))}
                    {loading && (
                        <div className="flex gap-3">
                            <Avatar className="w-8 h-8"><AvatarFallback className="bg-gradient-to-br from-blue-500 to-indigo-600"><Bot size={14} /></AvatarFallback></Avatar>
                            <div className="bg-white/10 p-4 rounded-2xl rounded-bl-sm text-gray-400 text-sm flex items-center gap-3 border border-white/5">
                                <div className="flex gap-1">
                                    <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                    <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                    <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                </div>
                                Searching & Generating...
                            </div>
                        </div>
                    )}
                </div>
            </ScrollArea>

            {/* Input */}
            <div className="flex gap-2 bg-white/5 p-2 rounded-xl border border-white/10 shadow-lg">
                <Input
                    value={query}
                    onChange={e => setQuery(e.target.value)}
                    onKeyDown={e => e.key === "Enter" && !loading && handleSend()}
                    placeholder={`Ask about ${dept.toUpperCase()} documents...`}
                    className="bg-transparent border-0 text-white focus-visible:ring-0 focus-visible:ring-offset-0 placeholder:text-gray-500 h-11"
                />
                <Button onClick={handleSend} disabled={loading || !query.trim()} className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 rounded-lg h-11 px-4 shadow-lg shadow-blue-500/20">
                    <Send size={18} />
                </Button>
            </div>
        </div>
    )
}
