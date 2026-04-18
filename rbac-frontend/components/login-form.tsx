"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import api from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardHeader, CardContent, CardTitle, CardDescription, CardFooter } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { toast } from "sonner"
import { Loader2, User, Shield, Briefcase, Users } from "lucide-react"

const DEMO_CREDENTIALS = [
    { username: "arshad@rbac.com", password: "admin123", role: "C-Level", icon: Shield, color: "from-purple-500 to-indigo-500" },
    { username: "priyanshu@rbac.com", password: "pass123", role: "Finance", icon: Briefcase, color: "from-green-500 to-emerald-500" },
    { username: "kanak@rbac.com", password: "pass123", role: "HR", icon: Users, color: "from-blue-500 to-cyan-500" },
    { username: "shirisha@rbac.com", password: "pass123", role: "Marketing", icon: User, color: "from-orange-500 to-amber-500" },
]

export default function LoginForm() {
    const router = useRouter()
    const [loading, setLoading] = useState(false)
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        try {
            const res = await api.post("/auth/login", { username, password })
            const { access_token, role, username: returnedUsername } = res.data

            localStorage.setItem("access_token", access_token)
            localStorage.setItem("username", returnedUsername || username)
            localStorage.setItem("user_role", role) // Store user role

            // Map role to display name
            const roleDisplay: Record<string, string> = {
                "c-level": "Admin",
                "finance": "Finance Manager",
                "hr": "HR Manager",
                "marketing": "Marketing Manager",
                "engineering": "Engineering Manager"
            }
            const displayName = roleDisplay[role?.toLowerCase() || ""] || role

            toast.success("Login successful", {
                description: `Welcome back, ${displayName}!`
            })
            router.push("/dashboard")
        } catch (err: any) {
            console.error(err)
            toast.error("Invalid credentials", {
                description: "Please check your username and password."
            })
        } finally {
            setLoading(false)
        }
    }

    const fillCredentials = (user: typeof DEMO_CREDENTIALS[0]) => {
        setUsername(user.username)
        setPassword(user.password)
        toast.info(`Demo: ${user.role}`, {
            description: `Credentials filled for ${user.username}`
        })
    }

    return (
        <Card className="border-white/10 bg-black/40 text-white backdrop-blur-xl shadow-2xl">
            <CardHeader className="text-center pb-2">
                <div className="mx-auto mb-4 w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
                    <Shield className="w-8 h-8 text-white" />
                </div>
                <CardTitle className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                    Secure Access
                </CardTitle>
                <CardDescription className="text-gray-400">
                    Enterprise RBAC Authentication Portal
                </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
                {/* Quick Fill Demo Credentials */}
                <div className="space-y-2">
                    <Label className="text-xs text-gray-500 uppercase tracking-wider">Quick Demo Access</Label>
                    <div className="grid grid-cols-2 gap-2">
                        {DEMO_CREDENTIALS.map((cred) => (
                            <Button
                                key={cred.username}
                                type="button"
                                variant="outline"
                                size="sm"
                                onClick={() => fillCredentials(cred)}
                                className={`border-white/10 bg-gradient-to-r ${cred.color} bg-opacity-10 hover:bg-opacity-20 text-white text-xs h-9 justify-start gap-2 transition-all hover:scale-[1.02] active:scale-[0.98]`}
                                suppressHydrationWarning
                            >
                                <cred.icon className="w-3 h-3" />
                                {cred.role}
                            </Button>
                        ))}
                    </div>
                </div>

                <div className="relative">
                    <div className="absolute inset-0 flex items-center">
                        <span className="w-full border-t border-white/10" />
                    </div>
                    <div className="relative flex justify-center text-xs uppercase">
                        <span className="bg-black/40 px-2 text-gray-500">or enter manually</span>
                    </div>
                </div>

                <form onSubmit={handleLogin} className="space-y-4" suppressHydrationWarning>
                    <div className="space-y-2">
                        <Label htmlFor="username" className="text-sm">Username</Label>
                        <Input
                            id="username"
                            placeholder="Enter username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="border-white/10 bg-white/5 text-white placeholder:text-gray-600 focus:border-blue-500/50 focus:ring-blue-500/20 h-11"
                            suppressHydrationWarning
                        />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="password" className="text-sm">Password</Label>
                        <Input
                            id="password"
                            type="password"
                            placeholder="Enter password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="border-white/10 bg-white/5 text-white placeholder:text-gray-600 focus:border-blue-500/50 focus:ring-blue-500/20 h-11"
                            suppressHydrationWarning
                        />
                    </div>
                    <Button
                        type="submit"
                        className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white border-0 h-11 text-base font-medium shadow-lg shadow-blue-500/20 transition-all hover:shadow-blue-500/30"
                        disabled={loading || !username || !password}
                        suppressHydrationWarning
                    >
                        {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : "Sign In Securely"}
                    </Button>
                </form>
            </CardContent>
            <CardFooter className="justify-center text-[10px] text-gray-600 border-t border-white/5 pt-4">
                Protected by Enterprise RBAC • AES-256 Encryption
            </CardFooter>
        </Card>
    )
}
